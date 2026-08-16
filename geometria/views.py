from django.shortcuts import render


def trigonometria(request):
    return render(request, "geometria/trigonometria.html")


def espacial(request):
    return render(request, "geometria/espacial.html")
