# Trabalho 2: Engenharia de Dados (Delta Lake + MinIO + SQL Server)

## Descrição
Este é o segundo trabalho da disciplina de Engenharia de Dados. O objetivo é criar um pipeline de dados executando a extração de dados de um banco de dados relacional (SQL Server) e salvando as camadas `landing-zone` (CSV) e `bronze` (Delta Lake) utilizando um Object Storage (MinIO).

## Arquitetura
1. **Origem:** SQL Server (Container Docker)
2. **Armazenamento:** MinIO (AWS S3-Compatible)
3. **Processamento:** PySpark com Delta Lake
4. **Gerenciador:** UV

## Como executar
1. Copie o arquivo de variáveis de ambiente:
   `cp .env.example .env`
2. Suba os containers do SQL Server e do MinIO:
   `docker compose up -d`
3. Instale as dependências com UV e ative o ambiente:
   `uv sync`
   `source .venv/bin/activate`
4. Inicie o Jupyter Lab e execute os notebooks sequencialmente na pasta `src/`:
   `uv run jupyter lab`
