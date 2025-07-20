# Preparação do Ambiente

Siga estes passos para configurar o ambiente e baixar o dataset necessário para a POC.

## 1. Instale as Dependências

As bibliotecas Python necessárias estão listadas no arquivo `requirements.txt` dentro desta pasta. É recomendado utilizar um ambiente virtual (`venv`).

```bash
# A partir do diretório raiz do projeto (beam_spark)
pip install -r prep_ambiente/requirements.txt --upgrade
```

## 2. Configure o Acesso à API do Kaggle

O projeto precisa de credenciais para baixar o dataset do Kaggle.

### a. Aceite as Regras do Dataset (Obrigatório)

Antes de usar a API, você **precisa** aceitar os termos de uso do dataset diretamente no site do Kaggle.

1.  **Acesse a página do dataset:** State of Data - Brazil 2023
2.  **Faça login** com sua conta do Kaggle.
3.  **Aceite as regras.** Pode ser necessário clicar em um botão como "Download" ou "I Understand and Accept".

Este passo é crucial. O script falhará com um erro de permissão se ele for pulado.

### b. Posicione seu Token da API

1.  Vá para a sua página de conta no Kaggle (`kaggle.com/me/account`) e clique em **"Create New API Token"**. Isso fará o download de um arquivo `kaggle.json`.
2.  Mova este arquivo para o diretório de configuração padrão do Kaggle e defina as permissões corretas. Este é o método mais confiável e recomendado.

```bash
# Crie o diretório se ele não existir
mkdir -p ~/.kaggle

# Mova o arquivo baixado para o local correto (ajuste o caminho se necessário)
mv ~/Downloads/kaggle.json ~/.kaggle/kaggle.json

# Defina permissões seguras (leitura/escrita apenas para seu usuário)
chmod 600 ~/.kaggle/kaggle.json
```

> ⚠️ **Aviso de Segurança:** Se preferir manter o `kaggle.json` dentro da pasta `prep_ambiente` para referência, certifique-se de que a linha `prep_ambiente/kaggle.json` está no seu arquivo `.gitignore` para evitar o commit acidental de credenciais.

## 3. Baixe o Dataset

Com o ambiente configurado, execute o script de download.

```bash
# Navegue até a pasta de preparação
cd prep_ambiente

# Execute o script
python download_dataset.py
```

Isso baixará o dataset para a pasta `data/raw/` (localizada na raiz do projeto), preparando-o para as próximas etapas da POC.