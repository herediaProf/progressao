from django.urls import path
from . import views

urlpatterns = [
    path("", views.pagina_estatistica, name="estatistica_home"),
    path(
        "api/calcular/", views.api_calcular_estatistica, name="api_calcular_estatistica"
    ),
    # Novas rotas de Probabilidade
    path("probabilidade/", views.pagina_probabilidade, name="probabilidade_home"),
    path("api/monte-carlo/", views.api_simular_monte_carlo, name="api_monte_carlo"),
]
