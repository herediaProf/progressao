from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Desafio, PerfilEstudante
from .generators import GeradorDesafios


def quiz_view(request, desafio_id):
    desafio = get_object_or_404(Desafio, pk=desafio_id)
    return render(request, "desafios/quiz.html", {"desafio": desafio})


def validar_resposta(request, desafio_id):
    if request.method == "POST":
        desafio = get_object_or_404(Desafio, pk=desafio_id)

        base_user = float(request.POST.get("base", 0))
        k_user = float(request.POST.get("k", 0))

        # Cálculo da margem de erro relativa
        erro_base = abs(base_user - desafio.alvo_base)
        erro_k = abs(k_user - desafio.alvo_k)

        correto = (erro_base <= desafio.tolerancia) and (erro_k <= desafio.tolerancia)

        xp_ganho = 0
        if correto and request.user.is_authenticated:
            perfil, _ = PerfilEstudante.objects.get_or_create(usuario=request.user)
            if desafio not in perfil.desafios_concluidos.all():
                perfil.desafios_concluidos.add(desafio)
                perfil.adicionar_xp(desafio.xp_recompensa)
                xp_ganho = desafio.xp_recompensa

        return JsonResponse(
            {
                "correto": correto,
                "erro_base": round(erro_base, 2),
                "erro_k": round(erro_k, 2),
                "xp_ganho": xp_ganho,
                "mensagem": (
                    "Excelente! Função ajustada com precisão."
                    if correto
                    else "Ainda fora de alvo. Continue ajustando os controles."
                ),
            }
        )


def desafio_dinamico_view(request):
    """
    Gera um desafio inédito na hora usando o algoritmo dinâmico.
    """
    dados_desafio = GeradorDesafios.gerar_exponencial_log()

    # Salva os parâmetros na sessão HTTP para validação posterior sem persistir no BD
    request.session["desafio_atual"] = dados_desafio

    # Recupera histórico de erros da sessão
    erros = request.session.get("erros_consecutivos", 0)
    recomendacao = GeradorDesafios.recomendar_revisao({"exp_log": erros})

    return render(
        request,
        "desafios/desafio_dinamico.html",
        {"desafio": dados_desafio, "recomendacao": recomendacao},
    )


def validar_resposta_dinamica(request):
    if request.method == "POST":
        desafio_atual = request.session.get("desafio_atual")
        if not desafio_atual:
            return JsonResponse({"erro": "Nenhum desafio ativo na sessão."}, status=400)

        base_user = float(request.POST.get("base", 0))
        k_user = float(request.POST.get("k", 0))

        erro_base = abs(base_user - desafio_atual["alvo_base"])
        erro_k = abs(k_user - desafio_atual["alvo_k"])

        correto = (erro_base <= desafio_atual["tolerancia"]) and (
            erro_k <= desafio_atual["tolerancia"]
        )

        if correto:
            request.session["erros_consecutivos"] = 0
            xp_ganho = desafio_atual["xp_recompensa"]

            if request.user.is_authenticated:
                perfil, _ = PerfilEstudante.objects.get_or_create(usuario=request.user)
                perfil.adicionar_xp(xp_ganho)
        else:
            request.session["erros_consecutivos"] = (
                request.session.get("erros_consecutivos", 0) + 1
            )
            xp_ganho = 0

        erros_atuais = request.session.get("erros_consecutivos", 0)
        recomendacao = GeradorDesafios.recomendar_revisao({"exp_log": erros_atuais})

        return JsonResponse(
            {
                "correto": correto,
                "erro_base": round(erro_base, 2),
                "erro_k": round(erro_k, 2),
                "xp_ganho": xp_ganho,
                "erros_consecutivos": erros_atuais,
                "recomendacao": recomendacao,
                "mensagem": (
                    "Excelente! Resposta correta!"
                    if correto
                    else "Curva desalinhada. Tente ajustar os parâmetros."
                ),
            }
        )
