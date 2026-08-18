from typing import List, Dict, Any, Tuple
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from .models import Simulacao


def _calcular_progressao(
    tipo: str, a1: float, razao: float, n: int
) -> Tuple[List[float], float]:
    """Calcula os termos e a soma de uma P.A. ou P.G."""
    if tipo == "pa":
        termos = [a1 + (i * razao) for i in range(n)]
        soma = (n * (a1 + termos[-1])) / 2 if n > 0 else 0.0
    else:
        termos = [a1 * (razao**i) for i in range(n)]
        if razao != 1:
            soma = (a1 * (razao**n - 1)) / (razao - 1)
        else:
            soma = a1 * n

    return termos, soma


def pagina_simulador(request: HttpRequest):
    """Renderiza a página principal do simulador."""
    ultimas_simulacoes = Simulacao.objects.all().order_by("-id")[:5]
    return render(
        request, "progressao/simulador.html", {"historico": ultimas_simulacoes}
    )


def api_gerar_progressao(request: HttpRequest) -> JsonResponse:
    """API para calcular P.A./P.G., salvar no BD e retornar JSON com os termos."""
    tipo = request.GET.get("tipo", "pa").lower()

    if tipo not in ("pa", "pg"):
        return JsonResponse(
            {"status": "erro", "mensagem": "Tipo inválido. Use 'pa' ou 'pg'."},
            status=400,
        )

    try:
        a1 = float(request.GET.get("a1", 1))
        razao = float(request.GET.get("razao", 2))
        n = int(request.GET.get("n", 10))
    except (ValueError, TypeError):
        return JsonResponse(
            {"status": "erro", "mensagem": "Parâmetros numéricos inválidos."},
            status=400,
        )

    n = max(1, min(n, 30))

    try:
        termos, soma = _calcular_progressao(tipo, a1, razao, n)
    except ZeroDivisionError:
        return JsonResponse(
            {"status": "erro", "mensagem": "Erro de divisão por zero no cálculo."},
            status=400,
        )

    try:
        simulacao = Simulacao.objects.create(
            tipo=tipo, a1=a1, razao=razao, n=n, soma_calculada=soma
        )
        simulacao_id = simulacao.id
    except Exception:
        simulacao_id = None

    return JsonResponse(
        {
            "status": "sucesso",
            "id": simulacao_id,
            "tipo": tipo,
            "termos": [round(t, 4) for t in termos],
            "soma": round(soma, 4),
        }
    )


def _calcular_juros_comparativo(
    capital: float, taxa_mensal: float, tempo_meses: int
) -> Dict[str, Any]:
    i = taxa_mensal / 100.0
    meses = list(range(tempo_meses + 1))

    simples = [round(capital * (1 + i * t), 2) for t in meses]
    compostos = [round(capital * ((1 + i) ** t), 2) for t in meses]

    return {
        "meses": meses,
        "simples": simples,
        "compostos": compostos,
        "montante_final_simples": simples[-1],
        "montante_final_compostos": compostos[-1],
        "diferenca": round(compostos[-1] - simples[-1], 2),
    }


def pagina_financeira(request: HttpRequest):
    return render(request, "progressao/financeira.html")


def api_calcular_financeira(request: HttpRequest) -> JsonResponse:
    try:
        capital = float(request.GET.get("capital", 1000))
        taxa = float(request.GET.get("taxa", 2.5))
        tempo = int(request.GET.get("tempo", 24))
    except (ValueError, TypeError):
        return JsonResponse(
            {"status": "erro", "mensagem": "Parâmetros numéricos inválidos."},
            status=400,
        )

    tempo = max(1, min(tempo, 120))
    capital = max(1, capital)

    res = _calcular_juros_comparativo(capital, taxa, tempo)
    return JsonResponse({"status": "sucesso", "resultados": res})
