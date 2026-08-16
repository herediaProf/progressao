from django.urls import path
from . import views

urlpatterns = [
    path("trigonometria/", views.trigonometria, name="trigonometria"),
    path("espacial/", views.espacial, name="espacial"),
]
