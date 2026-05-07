# Trabalho 2: Pipeline de Engenharia de Dados

Bem-vindo à documentação do nosso projeto! 

Este trabalho prático tem como objetivo construir um pipeline de extração de dados de um banco relacional legado e sua respectiva ingestão em um *Data Lake* moderno, dividindo o fluxo de dados em camadas lógicas (Landing e Bronze) suportadas por tecnologias como MinIO e Delta Lake.

## Objetivo do Projeto
O trabalho foi estruturado estritamente para cumprir três grandes requisitos exigidos pela disciplina de Engenharia de Dados:
1. **Extração:** Extrair dados do SQL Server e gravar no formato bruto CSV no MinIO (`landing-zone`).
2. **Conversão e Otimização:** Ler os arquivos CSV da Landing Zone e convertê-los para o formato transacional Delta Lake no MinIO (`bronze`).
3. **Transações ACID:** Comprovar o suporte a operações DML (`INSERT`, `UPDATE`, `DELETE`) na tabela Delta da camada Bronze.

Navegue pelo menu lateral para acessar a explicação técnica detalhada de cada etapa e conferir as respectivas **imagens e evidências de comprovação** da nossa implementação.
