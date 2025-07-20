# Ambiente Docker para Spark

Este diretório contém a configuração para criar um ambiente Docker conteinerizado com Spark e todas as dependências do projeto Python já instaladas. Usar o Docker garante um ambiente consistente e reprodutível, eliminando a necessidade de instalar Java, Python e as bibliotecas manualmente na sua máquina local.

## Como Usar

Você pode usar o Docker Compose para uma experiência mais simples ou os comandos manuais do Docker.

### Opção 1: Usar Docker Compose (Recomendado)

O arquivo `docker-compose.yml` na raiz do projeto simplifica todo o processo.

1.  **Construir e Iniciar o Container:**
    A partir da **raiz do projeto**, execute:
    ```bash
    docker-compose up --build
    ```
    Este comando irá construir a imagem (se ainda não existir) e iniciar o container, já com os volumes configurados. Você será levado diretamente para o shell `bash` dentro do container.

2.  **Executar os Scripts:**
    Uma vez dentro do shell do container, navegue até a pasta `prep_ambiente` e execute os scripts:
    ```bash
    cd prep_ambiente
    python3 download_dataset.py
    python3 geraDados.py
    ```

3.  **Encerrar o Container:**
    Quando terminar, você pode sair do shell do container (`exit`) e depois parar o serviço com:
    ```bash
    docker-compose down
    ```

### Opção 2: Usar Comandos Docker Manuais

1.  **Construir a Imagem Docker:**
    A partir da **raiz do projeto**, execute:
    ```bash
    docker build -t poc-spark-env -f infra/Dockerfile .
    ```

2.  **Executar o Container:**
    O comando abaixo monta os volumes necessários e inicia um shell interativo. O volume do Kaggle é montado como somente leitura (`:ro`) por segurança.
    ```bash
    docker run -it --rm -v "$(pwd)":/app -v "$HOME/.kaggle":/root/.kaggle:ro poc-spark-env
    ```