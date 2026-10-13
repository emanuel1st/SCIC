import heapq
import random
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

ARQUIVO = Path("dados_aurora_siger.csv")
RELATORIO = Path("relatorio_tecnico.md")

MODULOS = [
    ("HAB", "Habitacao", "alto"),
    ("AGR", "Agricultura", "alto"),
    ("MED", "Suporte medico", "critico"),
    ("COM", "Comunicacao principal", "critico"),
    ("LAB", "Laboratorio cientifico", "normal"),
    ("ENE", "Energia", "critico"),
    ("VIDA", "Suporte a vida", "critico"),
    ("MAN", "Manutencao", "alto"),
    ("ARM", "Armazenamento", "normal"),
    ("EXP", "Exploracao", "normal"),
    ("CTL", "Central de controle", "critico"),
]


def classificar_latencia(latencia):
    if latencia <= 100:
        return "normal"
    if latencia <= 200:
        return "lento"
    return "critico"


def gerar_dados():
    """Gera 100 registros simulados com 75 normais, 20 lentos e 5 criticos."""
    rng = random.Random(42)
    registros = []

    for i in range(100):
        ciclo = i // 10 + 1
        codigo, nome, tipo = MODULOS[i % len(MODULOS)]

        if i < 75:
            latencia = rng.randint(45, 90) + ciclo
        elif i < 95:
            latencia = rng.randint(110, 175) + ciclo * 2
        else:
            latencia = rng.randint(220, 280)

        status = classificar_latencia(latencia)
        tensao = rng.choice([5, 12, 24])
        corrente = round(rng.uniform(1.0, 4.0), 2)

        registros.append({
            "ciclo": ciclo,
            "codigo_modulo": codigo,
            "nome_modulo": nome,
            "tipo_modulo": tipo,
            "latencia_observada_ms": latencia,
            "tensao_v": tensao,
            "corrente_a": corrente,
            "status": status,
            "codigo_sensor": 1001 + i,
            "mensagem_alerta": (
                "Falha critica detectada" if status == "critico"
                else "Latencia elevada" if status == "lento"
                else "Operacao normal"
            ),
        })

    pd.DataFrame(registros).to_csv(ARQUIVO, index=False)
    console.print("[green]Base simulada com 100 registros criada.[/green]")


def calcular_prioridade(linha):
    pontos_status = {"normal": 0, "lento": 30, "critico": 60}
    pontos_tipo = {"normal": 0, "alto": 20, "critico": 40}
    return (
        pontos_status[linha["status_calculado"]]
        + pontos_tipo[linha["tipo_modulo"]]
    )


def montar_fila(dados):
    fila = []
    for _, linha in dados.iterrows():
        heapq.heappush(
            fila,
            (
                -calcular_prioridade(linha),
                -int(linha["latencia_observada_ms"]),
                linha["nome_modulo"],
                linha["mensagem_alerta"],
            ),
        )
    return fila


class NoTrie:
    def __init__(self):
        self.filhos = {}
        self.final = False


class Trie:
    def __init__(self):
        self.raiz = NoTrie()

    def inserir(self, palavra):
        no = self.raiz
        for letra in palavra.lower():
            if letra not in no.filhos:
                no.filhos[letra] = NoTrie()
            no = no.filhos[letra]
        no.final = True

    def buscar_prefixo(self, prefixo):
        no = self.raiz
        for letra in prefixo.lower():
            if letra not in no.filhos:
                return False
            no = no.filhos[letra]
        return True


def avaliar_modelo(dados):
    """Treina a regressao e calcula metricas no conjunto de teste."""
    X = dados[["ciclo"]]
    y = dados["latencia_observada_ms"]

    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    modelo = LinearRegression()
    modelo.fit(X_treino, y_treino)
    previsoes = modelo.predict(X_teste)

    erros_absolutos = np.abs(y_teste.to_numpy() - previsoes)
    valores_reais = y_teste.to_numpy()
    erros_relativos = np.divide(
        erros_absolutos,
        np.abs(valores_reais),
        out=np.zeros_like(erros_absolutos, dtype=float),
        where=valores_reais != 0,
    ) * 100

    mse = mean_squared_error(y_teste, previsoes)
    metricas = {
        "MAE": mean_absolute_error(y_teste, previsoes),
        "MSE": mse,
        "RMSE": np.sqrt(mse),
        "R2": r2_score(y_teste, previsoes),
        "Erro absoluto medio": erros_absolutos.mean(),
        "Erro relativo medio (%)": erros_relativos.mean(),
    }
    return modelo, metricas


def gerar_relatorio(dados, metricas):
    quantidade = dados["status_calculado"].value_counts().to_dict()
    texto = f"""# Relatorio Tecnico - SCIC

## Objetivo
Simular o monitoramento da comunicacao da colonia Aurora Siger.

## Dados
Total de registros: {len(dados)}

- Normais: {quantidade.get("normal", 0)}
- Lentos: {quantidade.get("lento", 0)}
- Criticos: {quantidade.get("critico", 0)}

## Modelo preditivo
Foi utilizada regressao linear com o ciclo como variavel de entrada.
As metricas foram calculadas em dados separados para teste.

- MAE: {metricas["MAE"]:.2f} ms
- MSE: {metricas["MSE"]:.2f}
- RMSE: {metricas["RMSE"]:.2f} ms
- R²: {metricas["R2"]:.3f}
- Erro absoluto medio: {metricas["Erro absoluto medio"]:.2f} ms
- Erro relativo medio: {metricas["Erro relativo medio (%)"]:.2f}%

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
"""
    RELATORIO.write_text(texto, encoding="utf-8")
    console.print(
        Panel(
            f"[green]Relatorio salvo com sucesso em:[/green]\n[bold]{RELATORIO.resolve()}[/bold]",
            title="RELATORIO TECNICO",
            border_style="green",
            expand=True,
        )
    )


def converter_base(numero):
    return {
        "Decimal": str(numero),
        "Binario": bin(numero),
        "Hexadecimal": hex(numero),
    }


def menu_conversao_bases():
    while True:
        console.print(
            Panel(
                "[bold white]CONVERSOR DE BASES NUMERICAS[/bold white]\n"
                "[cyan]Conversao entre decimal, binario e hexadecimal[/cyan]",
                title="[bold cyan]SCIC | FERRAMENTAS[/bold cyan]",
                border_style="cyan",
                padding=(1, 3),
            )
        )
        entrada = console.input(
            "\n[bold yellow]Digite um numero decimal inteiro: [/bold yellow]"
        ).strip()

        try:
            numero = int(entrada)
            if numero < 0:
                console.print("[red]Digite um numero inteiro nao negativo.[/red]")
                continue

            resultado = converter_base(numero)
            tabela = Table(
                title=f"RESULTADO DA CONVERSAO — {numero}",
                box=box.ROUNDED,
                border_style="green",
                header_style="bold green",
                expand=True,
            )
            tabela.add_column("Sistema numerico", style="cyan", width=22)
            tabela.add_column("Valor convertido", style="bold white")
            tabela.add_row("Decimal (base 10)", resultado["Decimal"])
            tabela.add_row("Binario (base 2)", resultado["Binario"])
            tabela.add_row("Hexadecimal (base 16)", resultado["Hexadecimal"])
            console.print(tabela)
        except ValueError:
            console.print("[red]Entrada invalida. Digite um numero inteiro.[/red]")
            continue

        escolha = console.input(
            "\n[bold yellow]1 - Converter outro numero | 0 - Voltar ao menu: [/bold yellow]"
        ).strip()
        if escolha != "1":
            return


def aguardar_retorno():
    console.print(
        Panel(
            "[bold]O que deseja fazer agora?[/bold]\n\n"
            "[1] Executar novamente esta opcao\n"
            "[0] Voltar ao menu principal",
            title="[cyan]NAVEGACAO[/cyan]",
            border_style="cyan",
            expand=True,
        )
    )
    escolha = console.input("[bold yellow]Escolha: [/bold yellow]").strip()
    return escolha == "1"


def mostrar_resumo(dados):
    total = len(dados)
    normais = (dados["status_calculado"] == "normal").sum()
    lentos = (dados["status_calculado"] == "lento").sum()
    criticos = (dados["status_calculado"] == "critico").sum()
    media = dados["latencia_observada_ms"].mean()

    console.print(
        Panel(
            "[bold white]RESUMO DAS COMUNICACOES[/bold white]\n"
            "[cyan]Situacao geral da rede de Aurora Siger[/cyan]",
            title="[bold cyan]SCIC | MONITORAMENTO[/bold cyan]",
            border_style="cyan",
            padding=(1, 3),
        )
    )

    indicadores = Table(title="INDICADORES GERAIS", box=box.ROUNDED, expand=True)
    indicadores.add_column("Indicador", style="cyan")
    indicadores.add_column("Resultado", justify="center", style="bold white")
    indicadores.add_row("Total de registros", str(total))
    indicadores.add_row("Latencia media", f"{media:.2f} ms")
    indicadores.add_row("Comunicacoes normais", f"[green]{normais}[/green]")
    indicadores.add_row("Comunicacoes lentas", f"[yellow]{lentos}[/yellow]")
    indicadores.add_row("Comunicacoes criticas", f"[red]{criticos}[/red]")
    console.print(indicadores)

    tabela = Table(title="PRIMEIRO REGISTRO DE CADA MODULO", box=box.ROUNDED, expand=True)
    tabela.add_column("Modulo", style="cyan")
    tabela.add_column("Latencia", justify="right")
    tabela.add_column("Status", justify="center")
    tabela.add_column("Potencia", justify="right")
    cores = {"normal": "green", "lento": "yellow", "critico": "red"}

    for _, linha in dados.drop_duplicates(subset=["codigo_modulo"]).iterrows():
        status = linha["status_calculado"]
        tabela.add_row(
            linha["nome_modulo"],
            f"{linha['latencia_observada_ms']} ms",
            f"[{cores[status]}]{status.upper()}[/{cores[status]}]",
            f"{linha['potencia_w']:.2f} W",
        )
    console.print(tabela)

    if criticos:
        console.print(
            Panel(
                f"[bold red]ATENCAO: {criticos} registro(s) critico(s) detectado(s)![/bold red]\n"
                "Consulte a fila de prioridades para identificar os alertas mais urgentes.",
                border_style="red",
                title="ALERTA DO SISTEMA",
                expand=True,
            )
        )
    else:
        console.print(Panel("Nenhum registro critico detectado.", border_style="green"))


def mostrar_fila(dados):
    fila = montar_fila(dados)
    tabela = Table(title="ALERTAS POR PRIORIDADE", box=box.ROUNDED, expand=True)
    tabela.add_column("Modulo", style="cyan")
    tabela.add_column("Prioridade", justify="right")
    tabela.add_column("Latencia", justify="right")
    tabela.add_column("Alerta")
    for _ in range(min(10, len(fila))):
        pontos, latencia, modulo, alerta = heapq.heappop(fila)
        tabela.add_row(modulo, str(-pontos), f"{-latencia} ms", alerta)
    console.print(tabela)


def mostrar_previsao(modelo):
    try:
        ciclo = int(console.input("[yellow]Informe o ciclo a prever (1 a 10): [/yellow]"))
        previsao = float(modelo.predict(pd.DataFrame({"ciclo": [ciclo]}))[0])
        status = classificar_latencia(previsao)
        cores = {"normal": "green", "lento": "yellow", "critico": "red"}
        console.print(
            Panel(
                f"Ciclo solicitado: [bold]{ciclo}[/bold]\n"
                f"Latencia prevista: [bold]{previsao:.2f} ms[/bold]\n"
                f"Classificacao estimada: [{cores[status]}]{status.upper()}[/{cores[status]}]",
                title="PREVISAO DE LATENCIA",
                border_style=cores[status],
                expand=True,
            )
        )
    except ValueError:
        console.print("[red]Digite um numero inteiro valido.[/red]")


def mostrar_busca(dados, trie):
    prefixo = console.input("[yellow]Digite o inicio do nome ou codigo: [/yellow]").strip()
    if not prefixo:
        console.print("[yellow]Digite ao menos uma letra ou numero.[/yellow]")
        return

    if not trie.buscar_prefixo(prefixo):
        console.print("[yellow]Nenhum resultado para esse prefixo.[/yellow]")
        return

    encontrados = sorted(set(
        dados.loc[
            dados["nome_modulo"].str.lower().str.startswith(prefixo.lower()),
            "nome_modulo",
        ].tolist()
        + dados.loc[
            dados["codigo_modulo"].str.lower().str.startswith(prefixo.lower()),
            "codigo_modulo",
        ].tolist()
    ))
    if encontrados:
        tabela = Table(title="RESULTADOS DA BUSCA", box=box.ROUNDED, expand=True)
        tabela.add_column("Correspondencia", style="cyan")
        for valor in encontrados:
            tabela.add_row(valor)
        console.print(tabela)
    else:
        console.print("[yellow]O prefixo existe, mas nao correspondeu a um modulo listado.[/yellow]")


def mostrar_analise_eletrica(dados):
    tabela = Table(title="ANALISE ELETRICA", box=box.ROUNDED, expand=True)
    tabela.add_column("Modulo", style="cyan")
    tabela.add_column("Tensao", justify="right")
    tabela.add_column("Corrente", justify="right")
    tabela.add_column("Potencia", justify="right")
    unicos = dados.drop_duplicates(subset=["codigo_modulo"])
    for _, linha in unicos.iterrows():
        tabela.add_row(
            linha["nome_modulo"],
            f"{linha['tensao_v']} V",
            f"{linha['corrente_a']:.2f} A",
            f"{linha['potencia_w']:.2f} W",
        )
    console.print(tabela)
    console.print(
        Panel(
            f"Potencia somada dos primeiros registros por modulo: "
            f"[bold]{unicos['potencia_w'].sum():.2f} W[/bold]",
            border_style="green",
            expand=True,
        )
    )


def mostrar_metricas(metricas):
    tabela = Table(title="AVALIACAO DA REGRESSAO LINEAR", box=box.ROUNDED, expand=True)
    tabela.add_column("Metrica", style="cyan")
    tabela.add_column("Resultado", justify="right", style="bold white")
    tabela.add_row("MAE", f"{metricas['MAE']:.2f} ms")
    tabela.add_row("MSE", f"{metricas['MSE']:.2f}")
    tabela.add_row("RMSE", f"{metricas['RMSE']:.2f} ms")
    tabela.add_row("R²", f"{metricas['R2']:.3f}")
    tabela.add_row("Erro absoluto medio", f"{metricas['Erro absoluto medio']:.2f} ms")
    tabela.add_row("Erro relativo medio", f"{metricas['Erro relativo medio (%)']:.2f}%")
    console.print(tabela)
    console.print(
        "[dim]As metricas foram calculadas em registros separados para teste. "
        "Os dados sao simulados.[/dim]"
    )


def main():
    if ARQUIVO.exists():
        try:
            existentes = pd.read_csv(ARQUIVO)
            status_existentes = existentes["latencia_observada_ms"].apply(classificar_latencia)
            contagem = status_existentes.value_counts().to_dict()
            base_valida = (
                len(existentes) == 100
                and contagem.get("normal", 0) == 75
                and contagem.get("lento", 0) == 20
                and contagem.get("critico", 0) == 5
            )
        except (KeyError, pd.errors.EmptyDataError, pd.errors.ParserError):
            base_valida = False
    else:
        base_valida = False

    if not base_valida:
        gerar_dados()

    dados = pd.read_csv(ARQUIVO)
    dados["status_calculado"] = dados["latencia_observada_ms"].apply(classificar_latencia)
    dados["potencia_w"] = dados["tensao_v"] * dados["corrente_a"]

    modelo, metricas = avaliar_modelo(dados)

    trie = Trie()
    for valor in dados["nome_modulo"].tolist() + dados["codigo_modulo"].tolist():
        trie.inserir(valor)

    while True:
        console.print()
        console.print(
            Panel(
                "[bold white]SISTEMA DE COMUNICACAO INTERPLANETARIA[/bold white]\n"
                "[cyan]Monitoramento e gestao da colonia Aurora Siger[/cyan]",
                title="[bold cyan]SCIC[/bold cyan]",
                subtitle="[green]Sistema operacional[/green]",
                border_style="cyan",
                padding=(1, 3),
            )
        )

        menu = Table(title="MENU PRINCIPAL", box=box.ROUNDED, border_style="blue",
                     header_style="bold cyan")
        menu.add_column("Opcao", justify="center", style="bold yellow")
        menu.add_column("Funcionalidade", style="white")
        menu.add_row("1", "Resumo das comunicacoes")
        menu.add_row("2", "Fila de alertas prioritarios")
        menu.add_row("3", "Previsao de latencia")
        menu.add_row("4", "Busca de modulos por prefixo")
        menu.add_row("5", "Analise eletrica")
        menu.add_row("6", "Gerar relatorio tecnico")
        menu.add_row("7", "Conversao de bases numericas")
        menu.add_row("8", "Metricas do modelo preditivo")
        menu.add_row("0", "Encerrar sistema")
        console.print(menu)

        opcao = console.input("\n[bold yellow]Escolha uma opcao: [/bold yellow]").strip()

        if opcao == "0":
            console.print(Panel("[bold green]SCIC encerrado. Ate logo![/bold green]",
                                border_style="green", expand=True))
            break

        if opcao not in {"1", "2", "3", "4", "5", "6", "7", "8"}:
            console.print("[red]Opcao invalida. Tente novamente.[/red]")
            continue

        # Cada funcionalidade fica numa tela; 1 repete a opcao e 0 volta ao menu.
        if opcao == "7":
            menu_conversao_bases()
            continue

        while True:
            console.print()
            if opcao == "1":
                mostrar_resumo(dados)
            elif opcao == "2":
                mostrar_fila(dados)
            elif opcao == "3":
                mostrar_previsao(modelo)
            elif opcao == "4":
                mostrar_busca(dados, trie)
            elif opcao == "5":
                mostrar_analise_eletrica(dados)
            elif opcao == "6":
                gerar_relatorio(dados, metricas)
            elif opcao == "8":
                mostrar_metricas(metricas)

            if aguardar_retorno():
                continue
            break


if __name__ == "__main__":
    main()
