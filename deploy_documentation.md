# Documentação de Deploy Automático com GitHub Actions e AWS Elastic Beanstalk

Este documento descreve como realizaramos o deploy automático de uma aplicação utilizando GitHub Actions e AWS Elastic Beanstalk. A estrutura dos arquivos e a configuração necessária são detalhadas abaixo.

## Estrutura do arquivos

A estrutura básica inclui os seguintes arquivos e diretórios:

```
.ebextensions/
  ├── python.config
  ├── setup.config
.github/
  └── workflows/
      └── deploy.yml
Procfile
```

### Descrição dos Arquivos

- **Procfile**: Define o comando para iniciar o servidor da aplicação.

  ```bash
  web: uvicorn src.main:app --host 0.0.0.0 --port 8000
  ```

- **python.config**: Configurações específicas para o ambiente Python no Elastic Beanstalk (definido como containers).

  ```yaml
  option_settings:
    aws:elasticbeanstalk:container:python:
      WSGIPath: src.main:app

    aws:elbv2:loadbalancer:
      IdleTimeout: 300
  ```

- **setup.config**: Scripts de setup para instalar pacotes necessários, como o Google Chrome e o ChromeDriver.

  ```yaml
  packages:
    yum:
      xorg-x11-server-Xvfb: []
      wget: []
      unzip: []

  commands:
    01-setup-google-chrome:
      command: |
        sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm -O /tmp/google-chrome-stable.rpm
        sudo yum localinstall -y /tmp/google-chrome-stable.rpm

    02-setup-chromedriver:
      command: |
        sudo wget https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.99/linux64/chromedriver-linux64.zip -O /tmp/chromedriver-linux64.zip
        sudo cd /tmp/
        sudo unzip chromedriver-linux64.zip
        sudo mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/
        sudo chmod +x /usr/local/bin/chromedriver
  ```

## Configuração do GitHub Actions

O arquivo de workflow do GitHub Actions está localizado em `.github/workflows/deploy.yml`.

Este workflow é acionado sempre que houver um push na branch `main` e executa o deploy da aplicação para o AWS Elastic Beanstalk.

### Conteúdo do Arquivo `deploy.yml`

```yaml
name: Deploy to Elastic Beanstalk

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Install AWS CLI
        run: |
          curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
          unzip awscliv2.zip
          sudo ./aws/install --update

      - name: Install Elastic Beanstalk CLI
        run: |
          sudo apt-get -y install python3-pip
          pip3 install awsebcli --upgrade --user
          export PATH=$PATH:$HOME/.local/bin

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to Elastic Beanstalk
        run: |
          export PATH=$PATH:$HOME/.local/bin
          eb init -p python-3.11 EmbrapaProject --region us-east-1 --platform python-3.11
          eb deploy postech
```

### Explicação das Etapas

1. **Checkout do Código**: Clona o repositório na máquina virtual onde o GitHub Actions executa o workflow.
2. **Configuração do Ambiente Python**: Configura a versão do Python necessária (3.11) para a aplicação.
3. **Instalação das Dependências**: Instala as dependências da aplicação conforme definido no arquivo `requirements.txt`.
4. **Instalação do AWS CLI**: Baixa e instala a AWS CLI na máquina virtual.
5. **Instalação do Elastic Beanstalk CLI**: Instala o CLI do Elastic Beanstalk para gerenciar os ambientes do AWS Elastic Beanstalk.
6. **Configuração das Credenciais AWS**: Configura as credenciais AWS necessárias para realizar o deploy. Essas credenciais devem ser armazenadas como secrets no GitHub.
7. **Deploy para o Elastic Beanstalk**: Inicializa o ambiente Elastic Beanstalk e realiza o deploy da aplicação.

## Conclusão

O deploy da aplicação será feito automaticamente sempre que houver mudanças na branch `main`. Este processo automatizado garante que a aplicação esteja sempre atualizada no ambiente de produção, utilizando o AWS Elastic Beanstalk.
