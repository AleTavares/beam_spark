import os
import math
import re
from pathlib import Path
import shutil
import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws

# --- Configuração ---
BASE_CSV_PATH = Path(__file__).parent / "data/raw/state_of_data_2023.csv"
PROCESSED_DATA_PATH = Path(__file__).parent / "data/processed"
TARGET_SIZES_GB = [1, 10]


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


def clean_spark_column_names(df):
    """
    Limpa os nomes das colunas do DataFrame para serem compatíveis com formatos como Delta Lake.
    Substitui caracteres inválidos por underscores.
    """
    print("Limpando nomes de colunas para compatibilidade...")
    new_columns = []
    for col_name in df.columns:
        # Substitui qualquer caractere no conjunto ' ,;{}()\n\t=' por um underscore
        clean_name = re.sub(r'[ ,;{}()\n\t=]', '_', col_name)
        new_columns.append(clean_name)
    
    return df.toDF(*new_columns)


def parse_arguments():
    """Analisa os argumentos da linha de comando."""
    parser = argparse.ArgumentParser(description="Gera datasets de teste em vários formatos e tamanhos.")
    parser.add_argument(
        '--formats',
        nargs='+',
        choices=['parquet', 'csv', 'json', 'orc', 'delta'],
        default=['parquet', 'csv', 'json', 'orc', 'delta'],
        help="Lista de formatos de arquivo para gerar. Exemplo: --formats parquet json"
    )
    return parser.parse_args()


def generate_datasets(formats_to_generate):
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
    
    # Higieniza os nomes das colunas antes de qualquer processamento
    cleaned_df = clean_spark_column_names(base_df)
    
    cleaned_df.cache()
    base_df_count = cleaned_df.count()
    print(f"Dataset base lido com {base_df_count} linhas.")

    # Estima o tamanho em bytes do DataFrame base para calcular replicações
    # Esta é uma aproximação, o tamanho real em disco varia por formato.
    base_df_size_bytes = sum(row.__sizeof__() for row in cleaned_df.take(100)) / 100 * base_df_count

    for size_gb in TARGET_SIZES_GB:
        target_size_bytes = size_gb * (1024 ** 3)
        replication_factor = math.ceil(target_size_bytes / base_df_size_bytes)
        size_label = f"{size_gb}GB"

        print(f"\n--- Gerando dataset de aproximadamente {size_label} ---")
        print(f"Fator de replicação necessário: {replication_factor}")

        # Cria um DataFrame para replicar os dados
        replicator_df = spark.range(replication_factor)
        large_df_replicated = cleaned_df.crossJoin(replicator_df)

        # Gera um ID único para cada linha, usando a primeira coluna como base.
        id_col_name = cleaned_df.columns[0]
        print(f"  -> Gerando IDs únicos para as linhas na coluna '{id_col_name}'...")
        large_df_unique = large_df_replicated.withColumn(
            id_col_name,
            concat_ws("-", col(id_col_name), col("id"))
        ).drop("id")

        # Define o número de partições para o formato Delta (que permanece particionado)
        num_partitions = 32 if size_gb > 5 else 8
        large_df_repartitioned = large_df_unique.repartition(num_partitions)

        # Coalesce para uma única partição para gerar um arquivo único para os outros formatos
        single_partition_df = large_df_unique.coalesce(1)

        output_dir = PROCESSED_DATA_PATH / f"{size_gb}GB"
        output_dir.mkdir(parents=True, exist_ok=True)

        for data_format in formats_to_generate:
            print(f"  -> Escrevendo formato '{data_format}'...")

            try:
                if data_format == "delta":
                    # Delta Lake é sempre um diretório, então usamos o DF reparticionado
                    delta_path = output_dir / "delta"
                    large_df_repartitioned.write.mode("overwrite").format("delta").save(str(delta_path))
                    print(f"     ✅ Diretório Delta Lake gerado em: {delta_path}")
                else:
                    # Para outros formatos, geramos um arquivo único
                    temp_path = output_dir / f"{data_format}_temp"
                    writer = single_partition_df.write.mode("overwrite")
                    if data_format == "csv":
                        writer.option("header", "true").csv(str(temp_path))
                    else:  # parquet, json, orc
                        writer.format(data_format).save(str(temp_path))

                    # Encontra o arquivo gerado, move para o destino final e limpa o temp
                    part_file = next(temp_path.glob("part-*"))
                    final_file_path = output_dir / f"dataset.{data_format}"
                    part_file.rename(final_file_path)
                    shutil.rmtree(temp_path)
                    print(f"     ✅ Arquivo único gerado em: {final_file_path}")
            except Exception as e:
                print(f"     ❌ Falha ao escrever o formato {data_format}: {e}")

    cleaned_df.unpersist()
    spark.stop()
    print("\nProcesso de geração de dados finalizado.")


if __name__ == "__main__":
    args = parse_arguments()
    generate_datasets(formats_to_generate=args.formats)