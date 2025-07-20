import os
import math
from pathlib import Path
from pyspark.sql import SparkSession

# --- Configuração ---
BASE_CSV_PATH = Path(__file__).parent / "data/raw/state_of_data_2023.csv"
PROCESSED_DATA_PATH = Path(__file__).parent / "data/processed"
TARGET_SIZES_GB = [1, 10]
FORMATS_TO_GENERATE = ["parquet", "csv", "json", "orc", "delta"]


def create_spark_session():
    """
    Cria e configura uma sessão Spark com suporte para Delta Lake.
    A biblioteca delta-spark, quando instalada via pip, cuida da configuração
    dos JARs necessários para o modo local.
    """
    print("Iniciando a sessão Spark com suporte a Delta Lake...")
    try:
        spark = SparkSession.builder \
            .appName("POCDataGenerator") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .config("spark.driver.memory", "4g") \
            .getOrCreate()
        print("✅ Sessão Spark criada com sucesso.")
        return spark
    except Exception as e:
        print(f"❌ Falha ao criar a sessão Spark: {e}")
        print("   Verifique sua instalação do PySpark e do Java.")
        exit(1)


def generate_datasets():
    """
    Lê o dataset base e gera versões maiores em múltiplos formatos.
    """
    if not BASE_CSV_PATH.exists():
        print(f"❌ Erro: Arquivo base não encontrado em '{BASE_CSV_PATH}'")
        print("   Por favor, execute o script 'download_dataset.py' primeiro.")
        return

    spark = create_spark_session()

    print(f"\nLendo o dataset base de: {BASE_CSV_PATH}")
    base_df = spark.read.csv(str(BASE_CSV_PATH), header=True, inferSchema=True, multiLine=True, escape='"')
    base_df.cache()
    base_df_count = base_df.count()
    print(f"Dataset base lido com {base_df_count} linhas.")

    # Estima o tamanho em bytes do DataFrame base para calcular replicações
    # Esta é uma aproximação, o tamanho real em disco varia por formato.
    base_df_size_bytes = sum(row.__sizeof__() for row in base_df.take(100)) / 100 * base_df_count

    for size_gb in TARGET_SIZES_GB:
        target_size_bytes = size_gb * (1024 ** 3)
        replication_factor = math.ceil(target_size_bytes / base_df_size_bytes)
        size_label = f"{size_gb}GB"

        print(f"\n--- Gerando dataset de aproximadamente {size_label} ---")
        print(f"Fator de replicação necessário: {replication_factor}")

        # Cria um DataFrame para replicar os dados através de um cross join
        replicator_df = spark.range(replication_factor).withColumnRenamed("id", "replication_id")
        large_df = base_df.crossJoin(replicator_df).drop("replication_id")

        # O repartition controla o número de arquivos de saída.
        # Um número maior é melhor para paralelismo em datasets grandes.
        num_partitions = 32 if size_gb > 5 else 8
        large_df = large_df.repartition(num_partitions)

        for data_format in FORMATS_TO_GENERATE:
            output_path = PROCESSED_DATA_PATH / size_label / data_format
            print(f"  -> Escrevendo formato '{data_format}' em '{output_path}'...")

            try:
                writer = large_df.write.mode("overwrite")
                if data_format == "csv":
                    writer.option("header", "true").csv(str(output_path))
                elif data_format == "delta":
                    writer.format("delta").save(str(output_path))
                else:
                    # Parquet, JSON, ORC
                    writer.save(str(output_path), format=data_format)
                print(f"     ✅ Concluído.")
            except Exception as e:
                print(f"     ❌ Falha ao escrever o formato {data_format}: {e}")

    base_df.unpersist()
    spark.stop()
    print("\nProcesso de geração de dados finalizado.")


if __name__ == "__main__":
    generate_datasets()