from django.urls import path
from . import views

urlpatterns = [
    # Rota raiz do app: /desafios/ ou /desafios
    path("", views.desafio_dinamico_view, name="desafios_index"),
    # Rotas específicas
    path("dinamico/", views.desafio_dinamico_view, name="desafio_dinamico"),
    path(
        "validar-dinamico/",
        views.validar_resposta_dinamica,
        name="validar_desafio_dinamico",
    ),
    path("quiz/<int:desafio_id>/", views.quiz_view, name="quiz_view"),
    path("validar/<int:desafio_id>/", views.validar_resposta, name="validar_desafio"),
]
