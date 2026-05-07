# Implementação Prática e Operações CRUD

Para demonstrar o cenário descrito anteriormente na prática, utilizamos a API do PySpark com a biblioteca `delta.tables` no nosso caderno `03_dml_delta.ipynb`.

## 1. Modelo de Dados (Tabela fato_evento)
Nossa tabela de eventos contém os dados estruturados de lances do jogo: `id_evento`, `id_partida`, `id_jogador`, `tipo_evento`, `minuto_jogo` e a flag `revisado_var`.

## 2. Inserção Inicial (Create/Insert)
O Delta Lake garante que, mesmo em fluxos de alta velocidade, cada registro seja gravado de forma atômica. Nossos dados iniciais da partida são gravados na camada Bronze.

```python
# Dados iniciais da partida (Simulação: Flamengo x Vasco)
data = [
    (1, 101, 10, "Gol", 15, False),             # Gol do camisa 10
    (2, 101, 5, "Cartão Amarelo", 30, False),    # Falta do volante
    (3, 101, 9, "Gol", 44, False)               # Gol do centroavante
]
columns = ["id_evento", "id_partida", "id_jogador", "tipo_evento", "minuto_jogo", "revisado_var"]

df_eventos = spark.createDataFrame(data, columns)
# Escrita já ocorre no passo de conversão para a camada Bronze
```

## 3. Atualização (Update) - A Correção do VAR
O VAR identificou que o primeiro gol não foi do jogador 10, mas sim do jogador 99. Utilizamos a API do Delta para realizar a correção cirúrgica baseada na condição do ID do evento.

```python
from delta.tables import DeltaTable

# Carrega a tabela Delta mapeando o diretório de arquivos
delta_table = DeltaTable.forPath(spark, "s3a://bronze/eventos_delta")

# Realiza o UPDATE
delta_table.update(
    condition="id_evento = 1",
    set={"id_jogador": "99", "revisado_var": "True"}
)
```

## 4. Exclusão (Delete) - Gol Anulado
Simulamos a anulação do segundo gol da partida por impedimento do jogador 9 (evento de ID 3).

```python
# Realiza o DELETE com base na condição
delta_table.delete(condition="id_evento = 3")
```

## 5. Inserção (Insert / Append) - O Gol do Título
Para completar a tríade de DML, simulamos a inserção de um evento novinho em folha, gerado aos 45 do segundo tempo.

```python
# Inserindo um novo evento no final da partida
novo_evento = [(4, 101, 7, "Gol", 90, False)]
colunas = ["id_evento", "id_partida", "id_jogador", "tipo_evento", "minuto_jogo", "revisado_var"]

df_novo = spark.createDataFrame(novo_evento, colunas)
df_novo.write.format("delta").mode("append").save("s3a://bronze/eventos_delta")
```

## 6. Evidência de Execução (O VAR em Ação)
Ao rodar o arquivo `03_dml_delta.ipynb`, você verá no próprio console do Jupyter que o evento 3 (anulado) foi removido, o jogador do evento 1 foi atualizado com sucesso e um novo evento 4 foi inserido.

## 7. Por baixo dos panos (Arquitetura Delta)
A verdadeira mágica do Delta Lake acontece na pasta `_delta_log` (dentro do bucket no MinIO). Para cada operação CRUD (o INSERT inicial, o UPDATE, o DELETE e o APPEND final), arquivos JSON são gerados mapeando as transações. Isso prova que os arquivos brutos em Parquet não são sobrescritos cegamente, mas sim versionados de forma segura (Transações ACID e Time Travel).
