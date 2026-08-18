from django.urls import path
from . import views

urlpatterns = [
    path("exponencial-log/", views.pagina_exp_log, name="exp_log"),
    path("matrizes/", views.pagina_matrizes, name="matrizes_home"),
    path(
        "api/matrizes/calcular/", views.api_calcular_matriz, name="api_calcular_matriz"
    ),
    # Eixo 1: Conjuntos e Teoria das Funções
    path("conjuntos/", views.pagina_conjuntos, name="conjuntos_home"),
    path(
        "api/conjuntos/operacao/",
        views.api_operacao_conjuntos,
        name="api_operacao_conjuntos",
    ),
]
