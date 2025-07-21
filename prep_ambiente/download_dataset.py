import os
import sys
from pathlib import Path
import zipfile

# --- Verifica instalação da lib do kaggle ---
try:
    import kaggle
    print(f"✅ lib kaggle library importada com sucesso.")
except ImportError:
    print("❌ Error: The 'kaggle' library is not installed.")
    print("Please run: pip install -r requirements.txt --upgrade --force-reinstall")
    sys.exit(1)
# --- Fim da Verificação da Lib ---


def download_sod_2023_dataset(download_path="./data/raw"):
    """
    Baixa e descompacta o dataset 'State of Data - Brazil 2023' do Kaggle.

    Este script usa a biblioteca oficial 'kaggle' que é mais estável.
    Requer autenticação prévia (arquivo `~/.kaggle/kaggle.json`).

    Args:
        download_path (str): O diretório local para salvar os arquivos do dataset.
                             Por padrão, salva em './data/raw'.
    """
    handle = "datahackers/state-of-data-brazil-2023"
    destination = Path(download_path)
    destination.mkdir(parents=True, exist_ok=True)

    print(f"\nIniciando o download do dataset: {handle}")
    print(f"Os arquivos serão salvos e descompactados em: {destination.resolve()}")

    try:
        # Autentica usando o arquivo kaggle.json
        kaggle.api.authenticate()

        # Baixa os arquivos do dataset, descompactando-os no processo
        kaggle.api.dataset_download_files(
            handle,
            path=destination,
            unzip=True,  # A biblioteca cuida da descompactação
            quiet=False  # Mostra uma barra de progresso
        )

        print("\n✅ Download e descompactação concluídos com sucesso!")

        # Renomeia o arquivo para um nome mais simples
        original_file = destination / "State_of_data_BR_2023_Kaggle - df_survey_2023.csv"
        new_file = destination / "state_of_data_2023.csv"

        if original_file.exists():
            original_file.rename(new_file)
            print(f"Arquivo renomeado para: {new_file.name}")

    except Exception as e:
        print(f"\n❌ Ocorreu um erro durante o processo.")
        print(f"   Tipo de Erro: {type(e).__name__}")
        print(f"   Mensagem: {e}")
        print("\n   Por favor, verifique os seguintes pontos:")
        print("   1. Você aceitou os termos do dataset na página do Kaggle?")
        print("   2. Seu arquivo `~/.kaggle/kaggle.json` está configurado corretamente?")
        print("   3. As permissões do seu arquivo `kaggle.json` estão seguras? (Execute 'chmod 600 /caminho/para/seu/kaggle.json')")

if __name__ == "__main__":
    download_sod_2023_dataset()