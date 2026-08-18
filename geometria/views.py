from django.shortcuts import render
import math
from typing import Dict, Any
from django.http import JsonResponse, HttpRequest


def trigonometria(request):
    return render(request, "geometria/trigonometria.html")


def espacial(request):
    return render(request, "geometria/espacial.html")


def pagina_geometria_plana(request: HttpRequest):
    """Renderiza a página de Geometria Plana."""
    return render(request, "geometria/plana.html")


def pagina_geometria_espacial(request: HttpRequest):
    """Renderiza a página de Geometria Espacial (Visualizador 3D)."""
    return render(request, "geometria/espacial.html")


def api_calcular_espacial(request: HttpRequest) -> JsonResponse:
    """Calcula volume e área de superfície de sólidos 3D."""
    solido = request.GET.get("solido", "cubo")
    try:
        raio_lado = float(request.GET.get("a", 2.0))  # Raio ou Aresta
        altura = float(request.GET.get("h", 4.0))  # Altura (quando aplicável)
    except (ValueError, TypeError):
        return JsonResponse(
            {"status": "erro", "mensagem": "Valores numéricos inválidos."}, status=400
        )

    volume = 0.0
    area_total = 0.0

    if solido == "cubo":
        volume = raio_lado**3
        area_total = 6 * (raio_lado**2)
    elif solido == "esfera":
        volume = (4 / 3) * math.pi * (raio_lado**3)
        area_total = 4 * math.pi * (raio_lado**2)
    elif solido == "cilindro":
        volume = math.pi * (raio_lado**2) * altura
        area_total = 2 * math.pi * raio_lado * (altura + raio_lado)
    elif solido == "cone":
        geratriz = math.sqrt(raio_lado**2 + altura**2)
        volume = (1 / 3) * math.pi * (raio_lado**2) * altura
        area_total = math.pi * raio_lado * (raio_lado + geratriz)

    return JsonResponse(
        {
            "status": "sucesso",
            "solido": solido,
            "volume": round(volume, 2),
            "area_total": round(area_total, 2),
        }
    )
