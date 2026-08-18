from django.urls import path
from . import views

urlpatterns = [
    path("", views.pagina_simulador, name="simulador_pa_pg"),
    path("api/gerar/", views.api_gerar_progressao, name="api_gerar_progressao"),
    # Módulo de Matemática Financeira
    path("financeira/", views.pagina_financeira, name="financeira_home"),
    path(
        "api/financeira/", views.api_calcular_financeira, name="api_calcular_financeira"
    ),
]
