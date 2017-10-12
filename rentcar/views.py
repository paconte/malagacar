from django.shortcuts import render


def index(request):
    from django.http import HttpResponse
    return HttpResponse("Hello, world. You're at the rentcar index.")
