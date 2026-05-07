# Apache Spark e Delta Lake

## Processamento com PySpark

O **Apache Spark** é o motor de processamento distribuído responsável por toda a carga de trabalho de transformação neste projeto. Ele não armazena dados, apenas fornece "músculo" computacional para ler, transformar e escrever. 

Nosso script PySpark lê os dados do SQL Server via JDBC, deposita no MinIO (CSV), e depois em uma segunda etapa, transforma esses CSVs para o formato Lakehouse.

## O que é o Delta Lake?

Historicamente, os *Data Lakes* (construídos em cima do Hadoop HDFS ou S3) sofriam com problemas gravíssimos de confiabilidade de dados. Se um pipeline falhasse no meio de uma gravação de grandes arquivos `.parquet`, a tabela ficaria corrompida. Além disso, não era possível realizar comandos SQL triviais como `UPDATE` ou `DELETE` diretamente nos arquivos.

O **Delta Lake** resolve exatamente isso. Ele é uma camada de armazenamento open-source que traz **Transações ACID** (Atomicidade, Consistência, Isolamento e Durabilidade) para o mundo dos Data Lakes, operando por cima de arquivos Parquet e rastreando alterações através de logs de transação.

## Implementação Prática e Operações CRUD

No nosso arquivo `03_dml_delta.ipynb`, nós validamos na prática o poder do Delta Lake executando comandos DML.

### 1. Atualização (Update)
Executamos a alteração de registros específicos (ex: modificando a idade da cliente Ana Silva para 99), utilizando operações de UPDATE sem precisar regravar o banco inteiro.

```python
from delta.tables import DeltaTable

delta_table = DeltaTable.forPath(spark, "s3a://bronze/clientes_delta")

# UPDATE: Atualizar idade do cliente de ID 1
delta_table.update(
    condition="id = 1",
    set={"idade": "99"}
)
```

### 2. Exclusão (Delete)
Demonstramos a exclusão de dados baseada em uma cláusula SQL condicional, removendo o cliente de ID 3 de forma atômica e segura.

```python
# DELETE: Remover cliente de ID 3
delta_table.delete(condition="id = 3")
```

### 3. Inserção (Append / Insert)
Podemos inserir novos registros facilmente na nossa camada Bronze.

```python
# INSERT: Adicionar novo cliente
novos_clientes = spark.createDataFrame(
    [(4, "Joao", "joao@email.com", 25)], 
    "id int, nome string, email string, idade int"
)
novos_clientes.write.format("delta").mode("append").save("s3a://bronze/clientes_delta")
```

### 4. Time Travel (Viagem no Tempo)
Uma das maiores *features* do Delta. Como todas as mudanças e metadados são salvos, o Delta permite consultar o histórico de alterações (Auditoria) e ler a tabela como ela era no passado.

```python
# Consultar o log de transações
delta_table.history().select("version", "operation", "timestamp").show(truncate=False)
```
