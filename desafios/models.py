from django.db import models
from django.contrib.auth.models import User


class Badge(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    descricao = models.TextField()
    icone = models.CharField(max_length=10, default="🏆")
    xp_necessario = models.IntegerField(default=100)

    def __str__(self):
        return self.nome


class Desafio(models.Model):
    CATEGORIAS = [
        ("exp_log", "Exponenciais e Logaritmos"),
        ("matrizes", "Matrizes e Determinantes"),
        ("trigonometria", "Trigonometria"),
    ]

    titulo = models.CharField(max_length=150)
    enunciado = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)

    # Parâmetros Meta
    alvo_base = models.FloatField(help_text="Valor correto da base (a)")
    alvo_k = models.FloatField(help_text="Valor correto do multiplicador (k)")
    tolerancia = models.FloatField(default=0.1, help_text="Margem de erro aceitável")

    xp_recompensa = models.IntegerField(default=50)

    def __str__(self):
        return f"[{self.categoria}] {self.titulo}"


class PerfilEstudante(models.Model):
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="perfil_math"
    )
    xp_total = models.IntegerField(default=0)
    badges = models.ManyToManyField(Badge, blank=True)
    desafios_concluidos = models.ManyToManyField(Desafio, blank=True)

    def adicionar_xp(self, quantidade):
        self.xp_total += quantidade
        self.save()
        self.checar_novas_badges()

    def checar_novas_badges(self):
        badges_disponiveis = Badge.objects.filter(xp_necessario__lte=self.xp_total)
        for badge in badges_disponiveis:
            if badge not in self.badges.all():
                self.badges.add(badge)
