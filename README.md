# SCIC — Sistema de Comunicação Interplanetária da Colônia

## 1. Sobre o projeto

O **SCIC (Sistema de Comunicação Interplanetária da Colônia)** é um protótipo desenvolvido em Python para simular o monitoramento e o gerenciamento das comunicações de uma colônia espacial fictícia chamada **Aurora Siger**.

O sistema analisa dados de latência, identifica possíveis falhas de comunicação, organiza alertas por prioridade e utiliza regressão linear para estimar a latência de ciclos futuros.

O projeto foi desenvolvido como atividade acadêmica, com o objetivo de aplicar conceitos de programação, análise de dados, estruturas de dados, inteligência artificial e fundamentos de eletricidade.

## 2. Objetivos

- Monitorar a latência das comunicações entre os módulos da colônia.
- Classificar as comunicações como normais, lentas ou críticas.
- Organizar alertas conforme sua prioridade.
- Prever a latência utilizando um modelo de regressão linear.
- Calcular métricas para avaliar o desempenho do modelo preditivo.
- Realizar buscas por prefixos dos nomes e códigos dos módulos.
- Analisar tensão, corrente elétrica e potência.
- Converter valores entre as bases decimal, binária e hexadecimal.
- Gerar um relatório técnico com os resultados das análises.

## 3. Tecnologias utilizadas

- **Python:** linguagem principal do projeto.
- **Pandas:** leitura, organização e análise dos dados.
- **NumPy:** operações numéricas.
- **Scikit-learn:** implementação da regressão linear e avaliação do modelo.
- **Matplotlib:** biblioteca utilizada para visualizações gráficas, quando necessárias.
- **Rich:** melhoria da apresentação visual do menu e dos resultados no terminal.
- **CSV:** armazenamento dos dados simulados.
- **Markdown:** documentação e geração do relatório técnico.

## 4. Funcionalidades

O sistema possui um menu interativo no terminal com as seguintes opções:

| Opção | Funcionalidade |
|---|---|
| 1 | Resumo das comunicações e das latências |
| 2 | Consulta de alertas organizados por prioridade |
| 3 | Previsão de latência para um ciclo |
| 4 | Busca de módulos por prefixo |
| 5 | Análise elétrica dos módulos |
| 6 | Geração do relatório técnico |
| 7 | Conversão entre bases numéricas |
| 8 | Avaliação das métricas do modelo preditivo |
| 0 | Encerramento do programa |

Após utilizar uma funcionalidade, o usuário pode executá-la novamente ou retornar ao menu principal.

## 5. Dados simulados

O projeto utiliza dados simulados para representar o funcionamento das comunicações da colônia Aurora Siger.

O conjunto de dados contém 100 registros, distribuídos da seguinte maneira:

- **75 registros normais:** latência de até 100 ms.
- **20 registros lentos:** latência acima de 100 ms e até 200 ms.
- **5 registros críticos:** latência acima de 200 ms.

Os registros incluem informações como ciclo, código e nome do módulo, tipo de módulo, latência observada, tensão, corrente, status, código do sensor e mensagem de alerta.

Esses dados são utilizados para testar as funcionalidades sem depender de uma infraestrutura real de comunicação interplanetária.

## 6. Modelo preditivo

O SCIC utiliza **regressão linear**, implementada com a biblioteca Scikit-learn, para estimar a latência de comunicação a partir do número do ciclo.

O desempenho do modelo é avaliado pelas seguintes métricas:

- **MAE:** erro absoluto médio entre os valores previstos e observados.
- **MSE:** média dos erros quadráticos.
- **RMSE:** raiz quadrada do erro quadrático médio.
- **R²:** indicador de quanto da variação dos dados é explicada pelo modelo.

O sistema também permite consultar a previsão de latência para um ciclo informado pelo usuário.

Como os dados são simulados, os resultados representam uma demonstração acadêmica, não uma previsão validada para sistemas reais.

## 7. Estruturas de dados e análise elétrica

O projeto utiliza uma fila de prioridade baseada em heap para organizar os alertas conforme critérios de criticidade e tipo de módulo.

Também implementa uma árvore Trie para realizar buscas por prefixos, permitindo localizar módulos a partir de partes iniciais de seus nomes ou códigos.

Na análise elétrica, o sistema calcula a potência de cada módulo utilizando a fórmula:

**P = V × I**

Onde:
- **P:** potência, em watts (W).
- **V:** tensão elétrica, em volts (V).
- **I:** corrente elétrica, em amperes (A).

## 8. Como executar o projeto

### Pré-requisitos

- Python instalado.
- Terminal ou Visual Studio Code.

### Instalação

1. Abra o terminal na pasta do projeto.
2. Ative o ambiente virtual, caso ele já tenha sido criado.

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Caso ainda não tenha instalado as bibliotecas, execute:

```powershell
pip install numpy pandas scikit-learn matplotlib rich
```

4. Inicie o programa:

```powershell
python codigo_fonte.py
```

O menu principal será exibido no terminal. Basta selecionar a opção desejada e seguir as instruções apresentadas.

## 9. Estrutura do projeto

```text
SCIC/
├── .venv/
├── codigo_fonte.py
├── dados_aurora_siger.csv
├── README.md
└── relatorio_tecnico.md
```

O arquivo `relatorio_tecnico.md` é gerado pela opção 6 do menu. Outros arquivos podem ser adicionados conforme a organização final da entrega.

## 10. Considerações finais

O desenvolvimento do SCIC permitiu integrar diferentes conceitos de programação e análise de dados em um único protótipo. A aplicação demonstra como a classificação de eventos, as estruturas de dados, os modelos preditivos e o monitoramento elétrico podem contribuir para a identificação de problemas e para a organização das comunicações em um ambiente simulado.

O projeto pode ser expandido futuramente com dados reais, visualizações gráficas, novos indicadores e modelos preditivos mais avançados.

---

**Projeto acadêmico — Sistema de Comunicação Interplanetária da Colônia (SCIC).**