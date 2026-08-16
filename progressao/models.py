from django.db import models


class Simulacao(models.Model):
    TIPO_CHOICES = [
        ("pa", "Progressão Aritmética (P.A.)"),
        ("pg", "Progressão Geométrica (P.G.)"),
    ]

    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default="pa")
    a1 = models.FloatField(verbose_name="Primeiro Termo (a1)", default=1.0)
    razao = models.FloatField(verbose_name="Razão (r ou q)", default=2.0)
    n = models.IntegerField(verbose_name="Número de Termos (n)", default=10)
    soma_calculada = models.FloatField(
        verbose_name="Soma dos Termos", null=True, blank=True
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Simulação"
        verbose_name_plural = "Simulações"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.get_tipo_display()} - a1={self.a1}, r/q={self.razao}, n={self.n}"
