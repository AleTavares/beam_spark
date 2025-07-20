# Use uma imagem base com Java (pré-requisito para Spark)
FROM eclipse-temurin:11-jdk-focal

# Evita prompts interativos durante a instalação de pacotes
ENV DEBIAN_FRONTEND=noninteractive

# Instala Python, pip e outras utilidades
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências do Python para o container
# O Dockerfile está em /infra, então o caminho para o requirements.txt é ../prep_ambiente/requirements.txt
COPY ../prep_ambiente/requirements.txt .

# Instala as dependências do Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Inicia um shell bash para que o usuário possa executar os scripts manualmente.
CMD ["bash"]