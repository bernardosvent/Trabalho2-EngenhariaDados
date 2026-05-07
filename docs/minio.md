# MinIO (Object Storage)

## O que é o MinIO?

O MinIO é um servidor de armazenamento de objetos de alto desempenho e código aberto. Ele foi construído especificamente para cargas de trabalho de infraestrutura em nuvem e é 100% compatível com a API do **Amazon S3**.

Em vez de depender de sistemas de arquivos distribuídos tradicionais como o HDFS (Hadoop Distributed File System), a arquitetura de dados moderna abraça os *Object Storages* por causa da sua escalabilidade massiva e menor custo operacional.

## Aplicação no nosso Cenário

Em nosso projeto, utilizamos o MinIO para construir e segregar nosso Data Lake em camadas lógicas (Buckets):

- **Bucket `landing-zone`:** Recebe os arquivos extratos (em formato CSV) diretamente do SQL Server. Representa o dado "cru" (raw), exatamente como saiu da fonte no momento da extração.
- **Bucket `bronze`:** Recebe os dados processados e estruturados a partir da camada landing. Aqui, os arquivos são gravados no formato colunar de alta performance, gerenciados pelo Delta Lake.
