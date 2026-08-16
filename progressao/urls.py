from django.urls import path
from . import views

urlpatterns = [
    path("", views.pagina_simulador, name="simulador"),
    path("api/gerar/", views.api_gerar_progressao, name="api_gerar_progressao"),
]
