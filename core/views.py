from django.shortcuts import render
from django.http import HttpRequest


def pagina_inicial(request: HttpRequest):
    """Renderiza a página inicial (Home) com acesso a todos os módulos."""
    return render(request, "inicio.html")
