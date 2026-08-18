from django.urls import path
from . import views

urlpatterns = [
    path("plana/", views.pagina_geometria_plana, name="geometria_plana"),
    path("espacial/", views.pagina_geometria_espacial, name="geometria_espacial"),
    path("trigonometria/", views.trigonometria, name="geometria_trigonometria"),
    path("api/espacial/", views.api_calcular_espacial, name="api_geometria_espacial"),
]
