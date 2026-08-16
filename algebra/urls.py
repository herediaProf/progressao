from django.urls import path
from . import views

urlpatterns = [
    path("exponencial-log/", views.exponencial_log, name="exponencial_log"),
]
