# Relatorio Tecnico - SCIC

## Objetivo
Simular o monitoramento da comunicacao da colonia Aurora Siger.

## Dados
Total de registros: 100

- Normais: 75
- Lentos: 20
- Criticos: 5

## Modelo preditivo
Foi utilizada regressao linear com o ciclo como variavel de entrada.
As metricas foram calculadas em dados separados para teste.

- MAE: 18.89 ms
- MSE: 640.60
- RMSE: 25.31 ms
- R²: 0.548
- Erro absoluto medio: 18.89 ms
- Erro relativo medio: 24.13%

## Eletricidade
A potencia e calculada por P = V x I, em watts.

## Gestao de alertas
A fila de prioridades utiliza heapq e considera a gravidade do alerta
e a importancia do modulo. A pontuacao e uma regra definida para este prototipo.

## Busca
A estrutura Trie permite verificar prefixos de nomes de modulos e codigos.

## Reflexao social, cultural e sustentabilidade
O monitoramento pode apoiar a distribuicao de recursos essenciais,
a comunicacao entre equipes de diferentes areas e a manutencao preventiva.
O consumo de energia deve ser acompanhado para reduzir desperdicios.
Os dados sao simulados e nao representam uma colonia real.
