from django.contrib import admin
from .models import Simulacao


@admin.register(Simulacao)
class SimulacaoAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo", "a1", "razao", "n", "soma_calculada", "criado_em")
    list_filter = ("tipo", "criado_em")
    search_fields = ("a1", "razao")
