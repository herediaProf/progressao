from django.test import TestCase, Client
from django.urls import reverse
from .models import Simulacao


class ProgressaoMathTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_calculo_pa(self):
        """Testa o cálculo da P.A. (a1=2, r=3, n=4 -> 2, 5, 8, 11 -> Soma=26)"""
        url = reverse("api_gerar_progressao") + "?tipo=pa&a1=2&razao=3&n=4"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["termos"], [2, 5, 8, 11])
        self.assertEqual(data["soma"], 26)

        # Verifica se gravou no banco de dados
        self.assertEqual(Simulacao.objects.count(), 1)

    def test_calculo_pg(self):
        """Testa o cálculo da P.G. (a1=2, q=3, n=3 -> 2, 6, 18 -> Soma=26)"""
        url = reverse("api_gerar_progressao") + "?tipo=pg&a1=2&razao=3&n=3"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["termos"], [2, 6, 18])
        self.assertEqual(data["soma"], 26)
