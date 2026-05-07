<div align="center">
  <h1>🚀 Trabalho 2: Pipeline de Engenharia de Dados</h1>
  <p><i>Extração de Dados do SQL Server e Ingestão no MinIO utilizando Apache Spark e Delta Lake.</i></p>

  ![Python](https://img.shields.io/badge/python-3.12-blue.svg)
  ![PySpark](https://img.shields.io/badge/PySpark-3.5.1-orange.svg)
  ![Delta Lake](https://img.shields.io/badge/Delta_Lake-3.2.0-blue)
  ![MinIO](https://img.shields.io/badge/MinIO-Object_Storage-red)
  ![SQL Server](https://img.shields.io/badge/SQL_Server-Docker-lightgrey)
  ![uv](https://img.shields.io/badge/uv-Package_Manager-magenta.svg)
</div>

---

## 📖 Sobre o Projeto

Este é o segundo trabalho prático da disciplina de **Engenharia de Dados**. O grande objetivo deste repositório é demonstrar a construção de um pipeline de dados *end-to-end* envolvendo a extração de um banco relacional, armazenamento em *Object Storage* e estruturação em camadas *Lakehouse*.

O fluxo de dados consiste em:
1. Conectar-se a um banco de dados **SQL Server** via PySpark.
2. Ingerir os dados e salvá-los no formato CSV em uma camada **Landing Zone** no **MinIO** (simulando um AWS S3).
3. Processar esses arquivos e movê-los para a camada **Bronze**, salvando-os utilizando o formato transacional **Delta Lake**.
4. Executar operações ACID e testes de manipulação de dados (DML) sobre a tabela Delta.

---

## ⚠️ Disclaimer

> [!IMPORTANT]
> Este projeto possui caráter acadêmico. Todo o ambiente (SQL Server e MinIO) foi configurado para rodar em *containers Docker* visando isolamento, segurança e reprodutibilidade perfeita. O ambiente foi testado nativamente em sistema Linux (Ubuntu/WSL).

---

## 🏛️ Arquitetura do Pipeline

A arquitetura foi desenhada em 4 pilares principais:

1. **Origem (Fonte de Dados):** SQL Server isolado em um container Docker.
2. **Armazenamento (Data Lake):** MinIO, um Object Storage 100% compatível com a API do AWS S3.
3. **Processamento Engine:** Apache Spark (PySpark) com suporte habilitado ao Delta Lake.
4. **Ambiente e Dependências:** Gerenciado pelo **UV**, o gerenciador de pacotes ultra-rápido do ecossistema Python.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
| :--- | :--- |
| **Docker & Docker Compose** | Orquestração dos serviços do SQL Server e do MinIO. |
| **MinIO** | Servidor de armazenamento de objetos (Landing Zone e Bronze). |
| **SQL Server** | Banco de dados relacional de origem simulando um sistema transacional (OLTP). |
| **Python (3.12) + UV** | Linguagem principal e gerenciador de pacotes. |
| **PySpark (3.5.1)** | Motor de processamento distribuído. |
| **Delta Lake (3.2.0)** | Formato de tabela Lakehouse garantindo transações ACID. |

---

## 📂 Estrutura de Diretórios

```text
Trabalho2-EngenhariaDados/
├── data/                  # Diretório local para persistência e logs
├── docs/                  # Documentação em MkDocs
├── src/                   # 📓 Cadernos Jupyter contendo a inteligência do pipeline
│   ├── 00_setup_sqlserver.ipynb       # Preparação das tabelas e carga no SQL Server
│   ├── 01_sqlserver_to_landing.ipynb  # Extração SQL Server -> MinIO (Landing/CSV)
│   ├── 02_landing_to_bronze.ipynb     # Processamento Landing -> MinIO (Bronze/Delta)
│   └── 03_dml_delta.ipynb             # Demonstração de operações ACID e DML no Delta
├── .env.example           # Modelo do arquivo de variáveis de ambiente
├── docker-compose.yml     # Orquestração do SQL Server e MinIO
├── pyproject.toml         # Mapeamento de dependências pelo UV
└── README.md              # Este documento
```

---

## 🚀 Como Executar o Projeto (Guia Passo-a-Passo)

### 1. Clonar e Preparar Variáveis
Clone o repositório e crie o seu arquivo de variáveis de ambiente a partir do exemplo fornecido:
```bash
git clone <url-do-repositorio>
cd Trabalho2-EngenhariaDados
cp .env.example .env
```

### 2. Subir a Infraestrutura Base (Docker)
Inicie os containers do SQL Server e do MinIO em segundo plano (detached mode):
```bash
docker compose up -d
```
> [!TIP]
> Verifique se os containers estão rodando corretamente utilizando o comando `docker ps`.

### 3. Instalar Dependências e Ativar Ambiente (UV)
Instale o ecossistema Python e ative o ambiente virtual para poder rodar o PySpark:
```bash
uv sync
source .venv/bin/activate
```

### 4. Executar os Notebooks
Para visualizar o código em ação, suba o **Jupyter Lab** e execute a sequência arquitetada:
```bash
uv run jupyter lab
```
Dentro da interface web do Jupyter, navegue até a pasta `src/` e execute os cadernos na seguinte ordem:
1. `00_setup_sqlserver.ipynb`
2. `01_sqlserver_to_landing.ipynb`
3. `02_landing_to_bronze.ipynb`
4. `03_dml_delta.ipynb`

---

## 📚 Documentação (MkDocs)

Assim como em projetos anteriores, a documentação teórica completa do projeto foi construída utilizando o **MkDocs** e aborda conceitos profundos sobre as ferramentas (SQL Server, MinIO e Delta Lake).

🌐 **Acesse a documentação web facilmente através do link:**
[https://bernardosvent.github.io/Trabalho2-EngenhariaDados/](https://bernardosvent.github.io/Trabalho2-EngenhariaDados/)

*(Alternativamente, para rodar localmente, utilize o comando `uv run mkdocs serve` e acesse http://127.0.0.1:8000).*

<br>
<div align="center">
  <p>Desenvolvido para fins acadêmicos. 🚀</p>
</div>
