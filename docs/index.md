# Contextualização e Cenário

## O Problema de Negócio
O ecossistema de análise de dados no esporte, especificamente no futebol de alto rendimento, gera um volume massivo de eventos a cada partida. O desafio arquitetural é manter um Data Lake atualizado com dados de jogadores, clubes e eventos de partidas (gols, cartões, substituições), garantindo a confiabilidade das estatísticas.

Em um Data Lake tradicional, operações de atualização e exclusão são complexas e custosas. No entanto, no cenário do futebol moderno, o uso do Árbitro de Vídeo (VAR) e auditorias pós-jogo frequentemente exigem a correção de dados históricos, como:

- **INSERT:** Inserção de novos eventos em tempo real ou em lotes ao fim de uma rodada.
- **UPDATE:** Correção da autoria de um gol ou atualização do status de um jogador transferido.
- **DELETE:** Anulação de um gol ou reversão de um cartão vermelho após revisão do VAR.

Para solucionar este problema, este projeto implementa a tecnologia **Delta Lake**, que traz transações ACID para o Data Lake.

## Fonte de Dados
A fonte primária de dados simulada para este ambiente baseia-se em extratos públicos no formato CSV inspirados em bases estatísticas do Kaggle (como o Campeonato Brasileiro de Futebol Dataset).

Os arquivos crus (.csv) são ingeridos e processados pelo Apache Spark, transformados em um modelo relacional e salvos no formato colunar avançado (Delta Lake) na camada Bronze do MinIO da nossa arquitetura.

## Modelo Entidade-Relacionamento (ER)
Para estruturar as análises, foi definido um modelo contemplando as dimensões de Clubes e Jogadores, e tabelas fato para as Partidas e os Eventos que ocorrem dentro delas. Nosso foco principal recai sobre a tabela `fato_evento`, que registra o que acontece durante os 90 minutos de jogo.
