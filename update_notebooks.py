import json

# Notebook 00
with open('src/00_setup_sqlserver.ipynb', 'r', encoding='utf-8') as f:
    nb00 = json.load(f)

for cell in nb00['cells']:
    if cell['cell_type'] == 'code' and any('df_clientes.write.jdbc' in line for line in cell.get('source', [])):
        cell['source'] = [
            "from pyspark.sql import SparkSession\n",
            "\n",
            "# Inicializa o Spark com o driver do SQL Server\n",
            "spark = SparkSession.builder \\\n",
            "    .appName(\"Setup-SQLServer\") \\\n",
            "    .config(\"spark.jars.packages\", \"com.microsoft.sqlserver:mssql-jdbc:12.6.1.jre11\") \\\n",
            "    .getOrCreate()\n",
            "\n",
            "# Configurações de conexão\n",
            "jdbc_url = \"jdbc:sqlserver://localhost:1433;databaseName=master;encrypt=false;trustServerCertificate=true\"\n",
            "jdbc_props = {\n",
            "    \"user\": \"sa\",\n",
            "    \"password\": \"SqlServer@2024!\",\n",
            "    \"driver\": \"com.microsoft.sqlserver.jdbc.SQLServerDriver\"\n",
            "}\n",
            "\n",
            "# Dados iniciais de uma partida (Simulação: Flamengo x Vasco)\n",
            "data = [\n",
            "    (1, 101, 10, \"Gol\", 15, False),             # Gol do camisa 10\n",
            "    (2, 101, 5, \"Cartão Amarelo\", 30, False),    # Falta do volante\n",
            "    (3, 101, 9, \"Gol\", 44, False)              # Gol do centroavante\n",
            "]\n",
            "\n",
            "columns = [\"id_evento\", \"id_partida\", \"id_jogador\", \"tipo_evento\", \"minuto_jogo\", \"revisado_var\"]\n",
            "\n",
            "df_eventos = spark.createDataFrame(data, columns)\n",
            "\n",
            "# Escreve no SQL Server\n",
            "df_eventos.write.jdbc(url=jdbc_url, table=\"fato_evento\", mode=\"overwrite\", properties=jdbc_props)\n",
            "print(\"Tabela 'fato_evento' criada com sucesso no SQL Server!\")\n"
        ]
        # clear output to avoid confusion
        cell['outputs'] = []

with open('src/00_setup_sqlserver.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb00, f, indent=1)

# Notebook 01
with open('src/01_sqlserver_to_landing.ipynb', 'r', encoding='utf-8') as f:
    nb01 = json.load(f)

for cell in nb01['cells']:
    if cell['cell_type'] == 'code' and any('df_clientes = spark.read.jdbc' in line for line in cell.get('source', [])):
        cell['source'] = [
            "from pyspark.sql import SparkSession\n",
            "\n",
            "# Inicializa o Spark com pacotes do SQL Server e MinIO (AWS S3)\n",
            "spark = SparkSession.builder \\\n",
            "    .appName(\"Extract-To-Landing\") \\\n",
            "    .config(\"spark.jars.packages\", \"com.microsoft.sqlserver:mssql-jdbc:12.6.1.jre11,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.endpoint\", \"http://localhost:9000\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.access.key\", \"minioadmin\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.secret.key\", \"minioadmin\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.path.style.access\", \"true\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.connection.ssl.enabled\", \"false\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.impl\", \"org.apache.hadoop.fs.s3a.S3AFileSystem\") \\\n",
            "    .getOrCreate()\n",
            "\n",
            "jdbc_url = \"jdbc:sqlserver://localhost:1433;databaseName=master;encrypt=false;trustServerCertificate=true\"\n",
            "jdbc_props = {\n",
            "    \"user\": \"sa\",\n",
            "    \"password\": \"SqlServer@2024!\",\n",
            "    \"driver\": \"com.microsoft.sqlserver.jdbc.SQLServerDriver\"\n",
            "}\n",
            "\n",
            "# Lendo a tabela do SQL Server\n",
            "df_eventos = spark.read.jdbc(url=jdbc_url, table=\"fato_evento\", properties=jdbc_props)\n",
            "df_eventos.show()\n",
            "\n",
            "# Escrevendo no MinIO (bucket landing-zone) em formato CSV\n",
            "landing_path = \"s3a://landing-zone/eventos_csv\"\n",
            "df_eventos.write.csv(landing_path, header=True, mode=\"overwrite\")\n",
            "\n",
            "print(\"Dados exportados para o MinIO em CSV com sucesso!\")\n"
        ]
        cell['outputs'] = []
    
    if cell['cell_type'] == 'markdown' and any('clientes_csv' in line or 'tabelas' in line for line in cell.get('source', [])):
        cell['source'] = [
            "# Passo 1: Extração (SQL Server para MinIO - CSV)\n",
            "Neste notebook, conectamos no SQL Server, lemos a tabela fato_evento e gravamos no bucket `landing-zone` no formato CSV."
        ]

with open('src/01_sqlserver_to_landing.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb01, f, indent=1)

# Notebook 02
with open('src/02_landing_to_bronze.ipynb', 'r', encoding='utf-8') as f:
    nb02 = json.load(f)

for cell in nb02['cells']:
    if cell['cell_type'] == 'code' and any('df_csv = spark.read.csv' in line for line in cell.get('source', [])):
        cell['source'] = [
            "from pyspark.sql import SparkSession\n",
            "\n",
            "# Inicializa o Spark com pacotes do Delta Lake e MinIO\n",
            "spark = SparkSession.builder \\\n",
            "    .appName(\"Landing-To-Bronze\") \\\n",
            "    .config(\"spark.jars.packages\", \"io.delta:delta-spark_2.12:3.2.0,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262\") \\\n",
            "    .config(\"spark.sql.extensions\", \"io.delta.sql.DeltaSparkSessionExtension\") \\\n",
            "    .config(\"spark.sql.catalog.spark_catalog\", \"org.apache.spark.sql.delta.catalog.DeltaCatalog\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.endpoint\", \"http://localhost:9000\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.access.key\", \"minioadmin\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.secret.key\", \"minioadmin\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.path.style.access\", \"true\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.connection.ssl.enabled\", \"false\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.impl\", \"org.apache.hadoop.fs.s3a.S3AFileSystem\") \\\n",
            "    .getOrCreate()\n",
            "\n",
            "# Lendo o CSV da landing-zone\n",
            "landing_path = \"s3a://landing-zone/eventos_csv\"\n",
            "df_csv = spark.read.csv(landing_path, header=True, inferSchema=True)\n",
            "df_csv.show()\n",
            "\n",
            "# Escrevendo em formato Delta na bronze\n",
            "bronze_path = \"s3a://bronze/eventos_delta\"\n",
            "df_csv.write.format(\"delta\").mode(\"overwrite\").save(bronze_path)\n",
            "\n",
            "print(\"Tabela Delta criada com sucesso na Bronze!\")\n"
        ]
        cell['outputs'] = []

with open('src/02_landing_to_bronze.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb02, f, indent=1)

# Notebook 03
with open('src/03_dml_delta.ipynb', 'r', encoding='utf-8') as f:
    nb03 = json.load(f)

for cell in nb03['cells']:
    if cell['cell_type'] == 'code' and any('delta_table = DeltaTable.forPath' in line for line in cell.get('source', [])):
        cell['source'] = [
            "from pyspark.sql import SparkSession\n",
            "from delta.tables import DeltaTable\n",
            "\n",
            "# Inicializa o Spark\n",
            "spark = SparkSession.builder \\\n",
            "    .appName(\"DML-Delta-VAR\") \\\n",
            "    .config(\"spark.jars.packages\", \"io.delta:delta-spark_2.12:3.2.0,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262\") \\\n",
            "    .config(\"spark.sql.extensions\", \"io.delta.sql.DeltaSparkSessionExtension\") \\\n",
            "    .config(\"spark.sql.catalog.spark_catalog\", \"org.apache.spark.sql.delta.catalog.DeltaCatalog\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.endpoint\", \"http://localhost:9000\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.access.key\", \"minioadmin\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.secret.key\", \"minioadmin\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.path.style.access\", \"true\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.connection.ssl.enabled\", \"false\") \\\n",
            "    .config(\"spark.hadoop.fs.s3a.impl\", \"org.apache.hadoop.fs.s3a.S3AFileSystem\") \\\n",
            "    .getOrCreate()\n",
            "\n",
            "bronze_path = \"s3a://bronze/eventos_delta\"\n",
            "delta_table = DeltaTable.forPath(spark, bronze_path)\n",
            "\n",
            "print(\"Placar Inicial:\")\n",
            "delta_table.toDF().orderBy(\"id_evento\").show()\n",
            "\n",
            "# 1. Cenário VAR 1: Corrigindo o autor do gol (id_evento = 1)\n",
            "print(\">>> VAR analisando o primeiro gol...\")\n",
            "delta_table.update(\n",
            "    condition=\"id_evento = 1\",\n",
            "    set={\"id_jogador\": \"99\", \"revisado_var\": \"True\"}\n",
            ")\n",
            "\n",
            "# 2. Cenário VAR 2: Anulando o gol por impedimento (id_evento = 3)\n",
            "print(\">>> VAR anulando o segundo gol por impedimento...\")\n",
            "delta_table.delete(condition=\"id_evento = 3\")\n",
            "\n",
            "print(\"Placar Final atualizado pelo VAR:\")\n",
            "delta_table.toDF().orderBy(\"id_evento\").show()\n",
            "\n",
            "print(\">>> Consultando a Versão 0 (Antes da intervenção do VAR):\")\n",
            "df_v0 = spark.read.format(\"delta\").option(\"versionAsOf\", 0).load(bronze_path)\n",
            "df_v0.orderBy(\"id_evento\").show()\n",
            "\n",
            "print(\"Histórico de versões (Time Travel):\")\n",
            "delta_table.history().select(\"version\", \"operation\", \"timestamp\").show(truncate=False)\n"
        ]
        cell['outputs'] = []

with open('src/03_dml_delta.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb03, f, indent=1)

print("Notebooks atualizados com sucesso!")
