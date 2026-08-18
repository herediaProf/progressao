import numpy as np
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest


def exponencial_log(request):
    return render(request, "algebra/exponencial_log.html")


def pagina_exp_log(request: HttpRequest):
    return render(request, "algebra/exp_log.html")


def pagina_matrizes(request: HttpRequest):
    """Renderiza a interface interativa de Matrizes e Determinantes."""
    return render(request, "algebra/matrizes.html")


def api_calcular_matriz(request: HttpRequest) -> JsonResponse:
    """Calcula Determinante, Traço e Matriz Inversa (se existir)."""
    try:
        # Recebe os elementos da matriz 2x2
        a11 = float(request.GET.get("a11", 1))
        a12 = float(request.GET.get("a12", 0))
        a21 = float(request.GET.get("a21", 0))
        a22 = float(request.GET.get("a22", 1))

        matriz = np.array([[a11, a12], [a21, a22]])
        det = float(np.linalg.det(matriz))
        traco = float(np.trace(matriz))

        inversa = None
        if abs(det) > 1e-9:
            inv_mat = np.linalg.inv(matriz)
            inversa = np.round(inv_mat, 4).tolist()

        return JsonResponse(
            {
                "status": "sucesso",
                "determinante": round(det, 4),
                "traco": round(traco, 4),
                "inversa": inversa,
                "interpretacao": (
                    "Área do paralelogramo formado pelos vetores base"
                    if abs(det) > 0
                    else "Espaço colapsado (linha/ponto)"
                ),
            }
        )
    except Exception as e:
        return JsonResponse({"status": "erro", "mensagem": str(e)}, status=400)


def pagina_conjuntos(request: HttpRequest):
    """Renderiza a interface do Diagrama de Venn Interativo."""
    return render(request, "algebra/conjuntos.html")


def api_operacao_conjuntos(request: HttpRequest) -> JsonResponse:
    """Calcula União, Interseção, Diferenças e Cardinalidade entre dois conjuntos."""
    raw_a = request.GET.get("set_a", "1, 2, 3, 4, 5")
    raw_b = request.GET.get("set_b", "4, 5, 6, 7, 8")

    try:
        # Tratamento e higienização dos elementos
        set_a = set(x.strip() for x in raw_a.split(",") if x.strip())
        set_b = set(x.strip() for x in raw_b.split(",") if x.strip())

        uniao = sorted(list(set_a | set_b))
        intersecao = sorted(list(set_a & set_b))
        diff_a_b = sorted(list(set_a - set_b))
        diff_b_a = sorted(list(set_b - set_a))

        return JsonResponse(
            {
                "status": "sucesso",
                "set_a": sorted(list(set_a)),
                "set_b": sorted(list(set_b)),
                "uniao": uniao,
                "intersecao": intersecao,
                "diff_a_b": diff_a_b,
                "diff_b_a": diff_b_a,
                "cardinalidade": {
                    "n_a": len(set_a),
                    "n_b": len(set_b),
                    "n_uniao": len(uniao),
                    "n_intersecao": len(intersecao),
                },
            }
        )
    except Exception as e:
        return JsonResponse({"status": "erro", "mensagem": str(e)}, status=400)
