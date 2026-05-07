<div align="center">
  <h1>Trabalho de Pesquisa: Apache Spark com Delta Lake (Simulação de Futebol e VAR)</h1>
</div>

## Descrição
Este projeto é referente ao trabalho da disciplina de Engenharia de Dados (Arquitetura de Dados). O objetivo é implementar um pipeline de dados *end-to-end* utilizando Apache Spark (PySpark) e demonstrar o funcionamento prático do formato de tabela **Delta Lake**. O projeto simula a ingestão de dados de uma partida de futebol (ex: Flamengo x Vasco), extraindo as informações de um banco de dados relacional (SQL Server), armazenando em um Object Storage (MinIO) estruturado nas camadas *Landing Zone* e *Bronze*, e demonstra a aplicação prática de comandos DML (INSERT, UPDATE e DELETE) simulando as intervenções do Árbitro de Vídeo (VAR).

## Disclaimer ou alertas/avisos
> [!IMPORTANT]
> Este é um projeto acadêmico desenvolvido para fins de avaliação. Todo o ambiente (SQL Server e MinIO) foi configurado para rodar em *containers Docker* visando isolamento. O ambiente foi configurado e testado em um sistema Linux (Ubuntu/WSL) para garantir a total compatibilidade e estabilidade das ferramentas de Engenharia de Dados, conforme recomendado nas aulas.
> **Dica para usuários de WSL 2:** Ao conectar no banco via JDBC, certifique-se de utilizar `127.0.0.1` ao invés de `localhost` para evitar conflitos de resolução IPv6.

## 🛠️ Tecnologias e Pré-requisitos
Para garantir a reprodutibilidade, utilizamos o gerenciador UV para travar as dependências exatas do projeto e o Docker para a infraestrutura de dados:

- **Docker & Docker Compose:** Orquestração dos serviços base (SQL Server e MinIO).
- **Java (OpenJDK 11 ou 17):** Necessário para a execução do motor Spark.
- **Python:** Versão 3.12.
- **UV:** Gerenciador de pacotes e ambientes virtuais (substituindo Pip/Poetry).
- **PySpark:** 3.5.1.
- **Delta Lake:** 3.2.0.

## Instalação
Siga o roteiro passo a passo abaixo para reproduzir a configuração exata do ambiente:

1. **Clone o repositório do projeto:**
```bash
git clone https://github.com/bernardosvent/Trabalho2-EngenhariaDados.git
cd Trabalho2-EngenhariaDados
```

2. **Crie as variáveis de ambiente base:**
```bash
cp .env.example .env
```

3. **Suba a infraestrutura base (SQL Server e MinIO):**
Antes de iniciar o Spark, inicie os containers em background:
```bash
docker compose up -d
```

4. **Garanta que o gerenciador UV está instalado:** 
Caso não tenha o UV, instale-o globalmente utilizando o pipx ou pip:
```bash
pip install uv
```

5. **Instale as dependências e crie o ambiente virtual:** 
Como estamos utilizando o padrão do UV, as bibliotecas já estão mapeadas no projeto. Para instalar tudo e gerar o ambiente virtual automaticamente, execute:
```bash
uv sync
```

6. **Ative o ambiente virtual:** 
Sempre que for trabalhar no projeto, ative o ambiente com o comando:
```bash
source .venv/bin/activate
```

## Howto
Para utilizar o projeto e visualizar as implementações práticas da arquitetura Lakehouse:

1. Com o ambiente virtual ativado e os containers rodando, inicie o servidor do Jupyter Labs executando:
```bash
uv run jupyter lab
```
2. No navegador, acesse a interface do Jupyter e navegue até a pasta `src/`.
3. Abra e execute os arquivos `.ipynb` na ordem cronológica (de `00` a `03`). Neles você verá a extração dos dados do SQL Server, a conversão para Delta Lake no MinIO e os blocos de código contendo o passo a passo das operações DML (Update, Delete) simulando o VAR.

## Testes
Para rodar a suíte de testes de qualidade de dados ou funções auxiliares do projeto utilizando o framework Pytest, execute no terminal (com o ambiente ativado):
```bash
pytest -v
```

## Documentação
A documentação teórica completa do projeto foi construída utilizando o MkDocs, contendo:

- Contextualização do trabalho e cenário dos dados (Futebol, Fonte de dados).
- Explicação teórica sobre o Apache Spark (PySpark).
- Explicação teórica sobre o Delta Lake e operações ACID em Data Lakes.
- Passos de extração e conversão para as camadas Landing Zone e Bronze.

Acesse a documentação web: [https://bernardosvent.github.io/Trabalho2-EngenhariaDados/](https://bernardosvent.github.io/Trabalho2-EngenhariaDados/)

*(Para rodar MinIO, acesse (http://127.0.0.1:9001/browser)).*

## 📚 Referências
**Fontes Recomendadas**
- **Canal DataWay BR (YouTube):** Tutoriais práticos sobre Engenharia de Dados, ecossistema Hadoop/Spark e arquiteturas de Lakehouse.
- **Repositórios de Referência (GitHub - @jlsilva01):**
  - spark-delta - Configuração do ecossistema Spark com Delta Lake.
  - spark-iceberg - Configuração do ecossistema Spark com Apache Iceberg.

**Documentação Oficial e Fontes Globais**
- **Delta Lake Official Documentation** - Guia oficial de arquitetura, cobrindo transações ACID, Time Travel e Schema Enforcement.
- **Apache Spark Documentation** - Documentação oficial do motor de processamento distribuído utilizado como base para o projeto.
- **MinIO Documentation** - Referência para configuração de Object Storage local compatível com S3.
