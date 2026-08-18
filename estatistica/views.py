import math
import random
from collections import Counter
from typing import List
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest


def _calcular_estatisticas(dados: List[float]) -> dict:
    n = len(dados)
    if n == 0:
        return {}

    dados_ordenados = sorted(dados)

    # Média
    media = sum(dados) / n

    # Mediana
    if n % 2 == 1:
        mediana = dados_ordenados[n // 2]
    else:
        mediana = (dados_ordenados[(n // 2) - 1] + dados_ordenados[n // 2]) / 2.0

    # Moda
    frequencias = Counter(dados)
    max_freq = max(frequencias.values())
    modas = [k for k, v in frequencias.items() if v == max_freq]
    if len(modas) == n:
        moda_str = "Amodal"
    else:
        moda_str = ", ".join(str(m) for m in modas)

    # Variância e Desvio Padrão (Amostral if n > 1 else Populacional)
    variancia = sum((x - media) ** 2 for x in dados) / (n - 1 if n > 1 else 1)
    desvio_padrao = math.sqrt(variancia)

    # Amplitude
    amplitude = dados_ordenados[-1] - dados_ordenados[0]

    return {
        "n": n,
        "media": round(media, 2),
        "mediana": round(mediana, 2),
        "moda": moda_str,
        "variancia": round(variancia, 2),
        "desvio_padrao": round(desvio_padrao, 2),
        "amplitude": round(amplitude, 2),
        "minimo": dados_ordenados[0],
        "maximo": dados_ordenados[-1],
        "frequencias": dict(sorted(frequencias.items())),
    }


def pagina_estatistica(request: HttpRequest):
    """Renderiza a página interativa de estatística."""
    return render(request, "estatistica/estatistica.html")


def api_calcular_estatistica(request: HttpRequest) -> JsonResponse:
    """API que recebe uma lista de números e retorna as estatísticas calculadas."""
    raw_data = request.GET.get("dados", "")
    if not raw_data:
        return JsonResponse(
            {"status": "erro", "mensagem": "Nenhum dado fornecido."}, status=400
        )

    try:
        # Aceita separação por vírgula, espaço ou ponto e vírgula
        dados_str = raw_data.replace(";", ",").replace(" ", ",").split(",")
        dados = [float(x.strip()) for x in dados_str if x.strip() != ""]
    except ValueError:
        return JsonResponse(
            {
                "status": "erro",
                "mensagem": "Insira apenas números válidos separados por vírgula.",
            },
            status=400,
        )

    if not dados:
        return JsonResponse(
            {"status": "erro", "mensagem": "Lista de dados vazia."}, status=400
        )

    res = _calcular_estatisticas(dados)
    return JsonResponse({"status": "sucesso", "resultados": res})


def _calcular_estatisticas(dados: List[float]) -> dict:
    n = len(dados)
    if n == 0:
        return {}

    dados_ordenados = sorted(dados)

    # Média
    media = sum(dados) / n

    # Mediana
    if n % 2 == 1:
        mediana = dados_ordenados[n // 2]
    else:
        mediana = (dados_ordenados[(n // 2) - 1] + dados_ordenados[n // 2]) / 2.0

    # Moda
    frequencias = Counter(dados)
    max_freq = max(frequencias.values())
    modas = [k for k, v in frequencias.items() if v == max_freq]
    if len(modas) == n:
        moda_str = "Amodal"
    else:
        moda_str = ", ".join(str(m) for m in modas)

    # Variância e Desvio Padrão (Amostral if n > 1 else Populacional)
    variancia = sum((x - media) ** 2 for x in dados) / (n - 1 if n > 1 else 1)
    desvio_padrao = math.sqrt(variancia)

    # Amplitude
    amplitude = dados_ordenados[-1] - dados_ordenados[0]

    return {
        "n": n,
        "media": round(media, 2),
        "mediana": round(mediana, 2),
        "moda": moda_str,
        "variancia": round(variancia, 2),
        "desvio_padrao": round(desvio_padrao, 2),
        "amplitude": round(amplitude, 2),
        "minimo": dados_ordenados[0],
        "maximo": dados_ordenados[-1],
        "frequencias": dict(sorted(frequencias.items())),
    }


def pagina_estatistica(request: HttpRequest):
    """Renderiza a página interativa de estatística."""
    return render(request, "estatistica/estatistica.html")


def api_calcular_estatistica(request: HttpRequest) -> JsonResponse:
    """API que recebe uma lista de números e retorna as estatísticas calculadas."""
    raw_data = request.GET.get("dados", "")
    if not raw_data:
        return JsonResponse(
            {"status": "erro", "mensagem": "Nenhum dado fornecido."}, status=400
        )

    try:
        # Aceita separação por vírgula, espaço ou ponto e vírgula
        dados_str = raw_data.replace(";", ",").replace(" ", ",").split(",")
        dados = [float(x.strip()) for x in dados_str if x.strip() != ""]
    except ValueError:
        return JsonResponse(
            {
                "status": "erro",
                "mensagem": "Insira apenas números válidos separados por vírgula.",
            },
            status=400,
        )

    if not dados:
        return JsonResponse(
            {"status": "erro", "mensagem": "Lista de dados vazia."}, status=400
        )

    res = _calcular_estatisticas(dados)
    return JsonResponse({"status": "sucesso", "resultados": res})


# --- NOVO: MÓDULO DE PROBABILIDADE & MONTE CARLO ---


def pagina_probabilidade(request: HttpRequest):
    """Renderiza a página interativa de Probabilidade e Monte Carlo."""
    return render(request, "estatistica/probabilidade.html")


def api_simular_monte_carlo(request: HttpRequest) -> JsonResponse:
    """Simula o método de Monte Carlo (Aproximação de Pi + Lei dos Grandes Números)."""
    try:
        n_experimentos = int(request.GET.get("n", 2000))
    except (ValueError, TypeError):
        return JsonResponse(
            {"status": "erro", "mensagem": "Número de experimentos inválido."},
            status=400,
        )

    # Garante limite seguro de processamento
    n_experimentos = max(10, min(n_experimentos, 50000))

    # 1. Estimativa de Pi por Monte Carlo (Pontos no quadrado vs. no círculo)
    dentro_circulo = 0
    pontos_amostra = []

    for i in range(1, n_experimentos + 1):
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        is_dentro = (x**2 + y**2) <= 1
        if is_dentro:
            dentro_circulo += 1

        # Envia até 250 pontos para renderização no canvas visual
        if i <= 250:
            pontos_amostra.append(
                {"x": round(x, 3), "y": round(y, 3), "dentro": is_dentro}
            )

    pi_estimado = 4 * (dentro_circulo / n_experimentos)

    # 2. Lei dos Grandes Números (Frequência Relativa de Lançamento de Moedas)
    caras = 0
    frequencia_relativa = []
    passo = max(1, n_experimentos // 50)

    for i in range(1, n_experimentos + 1):
        if random.random() < 0.5:
            caras += 1
        if i % passo == 0 or i == n_experimentos:
            frequencia_relativa.append(
                {"lancamento": i, "frequencia": round(caras / i, 4)}
            )

    return JsonResponse(
        {
            "status": "sucesso",
            "n_total": n_experimentos,
            "pi_estimado": round(pi_estimado, 5),
            "erro_pi_pct": round(abs((pi_estimado - math.pi) / math.pi) * 100, 2),
            "pontos_amostra": pontos_amostra,
            "convergencia_moeda": frequencia_relativa,
        }
    )
