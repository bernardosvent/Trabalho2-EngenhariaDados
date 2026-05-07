# Arquitetura e SQL Server

## Desenho da Solução

Nossa arquitetura de dados segue o paradigma de extração e carga assíncrona, separando o processamento transacional (que impacta a aplicação) do processamento analítico (que impacta a tomada de decisão).

As tecnologias foram cuidadosamente escolhidas para emular um ambiente Cloud *on-premise*:
- **Banco de Dados Relacional:** SQL Server (via Docker)
- **Data Lake (Storage):** MinIO (via Docker)
- **Motor de Processamento:** Apache Spark (PySpark)
- **Formato de Tabela Analítico:** Delta Lake

## O Papel do SQL Server

O SQL Server atua como nosso banco de dados de origem. Em um cenário corporativo real, ele seria o banco de dados por trás de uma aplicação de vendas, ERP, CRM, etc.

Para demonstrar este fluxo, preparamos o SQL Server inicialmente no arquivo `00_setup_sqlserver.ipynb` gerando dados fictícios via PySpark JDBC:

```python
# Inicializa o Spark com o driver JDBC do SQL Server
spark = SparkSession.builder \
    .appName("Setup-SQLServer") \
    .config("spark.jars.packages", "com.microsoft.sqlserver:mssql-jdbc:12.6.1.jre11") \
    .getOrCreate()

# Dados de exemplo: Clientes
clientes_data = [
    (1, "Ana Silva", "ana@email.com", 28),
    (2, "Carlos Souza", "carlos@email.com", 35),
    (3, "Maria Oliveira", "maria@email.com", 42)
]
df_clientes = spark.createDataFrame(clientes_data, schema=schema_clientes)

# Gravação no banco para emular uma tabela transacional (Produção)
df_clientes.write.jdbc(url=jdbc_url, table="clientes", mode="overwrite", properties=jdbc_props)
```

No pipeline seguinte (`01_sqlserver_to_landing.ipynb`), utilizamos o Apache Spark para conectar diretamente ao banco novamente, ler essas tabelas em sua totalidade, e gravar na nossa **Landing Zone** no MinIO no formato `CSV`.
