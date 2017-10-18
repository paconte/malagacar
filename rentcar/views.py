from django.shortcuts import render


def index(request):
    if request.method == 'POST':
        print("TODO BIEN")
        return render(request, 'rent.html')
    else:
        print("TODO MAL")
        return render(request, 'landing.html')


def rent(request):
    if request.method == 'POST':
        print("TODO BIEN")
        return render(request, 'rent.html')

