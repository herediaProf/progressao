import random
import math


class GeradorDesafios:

    @staticmethod
    def gerar_exponencial_log():
        """
        Gera parâmetros válidos para f(x) = k * a^x ou f(x) = k * log_a(x)
        Garante a > 0 e a != 1
        """
        tipo = random.choice(["exp", "log"])

        # Gera bases 'a' seguras evitando valores próximos de 1.0 ou <= 0
        bases_validas = [0.2, 0.5, 0.8, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
        a = random.choice(bases_validas)

        # Multiplicador k diferente de zero
        k_validos = [-2.5, -2.0, -1.5, -1.0, -0.5, 0.5, 1.0, 1.5, 2.0, 2.5]
        k = random.choice(k_validos)

        if tipo == "exp":
            titulo = f"Ajuste Exponencial: f(x) = {k} · ({a})ˣ"
            enunciado = (
                f"Posicione os sliders para reconstruir a curva f(x) = {k} · ({a})ˣ."
            )
        else:
            titulo = f"Ajuste Logarítmico: f(x) = {k} · log_{a}(x)"
            enunciado = f"Posicione os sliders para alinhar com a função f(x) = {k} · log_{a}(x)."

        return {
            "tipo": tipo,
            "titulo": titulo,
            "enunciado": enunciado,
            "alvo_base": round(a, 2),
            "alvo_k": round(k, 2),
            "tolerancia": 0.15,
            "xp_recompensa": 30,
        }

    @staticmethod
    def recomendar_revisao(historico_erros):
        """
        Analisa o histórico recente do aluno e sugere trilhas de reforço.
        """
        if historico_erros.get("exp_log", 0) >= 3:
            return {
                "precisa_reforcio": True,
                "topico": "Potenciação e Propriedades dos Logaritmos",
                "mensagem": "Percebemos que você errou 3 vezes consecutivas. Que tal revisar as propriedades operatórias das potências?",
                "link_revisao": "/algebra/exp-log/",
            }
        return {"precisa_reforcio": False}
