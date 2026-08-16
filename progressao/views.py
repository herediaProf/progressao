from django.shortcuts import render
from django.http import JsonResponse
from .models import Simulacao


def pagina_simulador(request):
    """Renderiza a página principal do simulador."""
    # Busca as últimas 5 simulações salvas no banco
    ultimas_simulacoes = Simulacao.objects.all()[:5]
    return render(
        request, "progressao/simulador.html", {"historico": ultimas_simulacoes}
    )


def api_gerar_progressao(request):
    """API para calcular P.A./P.G., salvar no BD e retornar JSON com os termos."""
    tipo = request.GET.get("tipo", "pa")  # 'pa' ou 'pg'
    try:
        a1 = float(request.GET.get("a1", 1))
        razão = float(request.GET.get("razao", 2))
        n = int(request.GET.get("n", 10))
    except ValueError:
        return JsonResponse(
            {"status": "erro", "mensagem": "Parâmetros inválidos."}, status=400
        )

    # Limite pedagógico para não travar a tela
    if n > 30:
        n = 30
    if n < 1:
        n = 1

    termos = []
    if tipo == "pa":
        # Fórmula P.A.: a_n = a_1 + (n - 1) * r
        termos = [a1 + (i * razão) for i in range(n)]
        soma = (n * (a1 + termos[-1])) / 2 if n > 0 else 0
    else:
        # Fórmula P.G.: a_n = a_1 * (q ** (n - 1))
        termos = [a1 * (razão**i) for i in range(n)]
        if razão != 1:
            soma = (a1 * (razão**n - 1)) / (razão - 1)
        else:
            soma = a1 * n

    # Registra no banco de dados
    simulacao = Simulacao.objects.create(
        tipo=tipo, a1=a1, razao=razão, n=n, soma_calculada=soma
    )

    return JsonResponse(
        {
            "status": "sucesso",
            "id": simulacao.id,
            "tipo": tipo,
            "termos": termos,
            "soma": round(soma, 4),
        }
    )
