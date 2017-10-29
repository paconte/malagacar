from django.shortcuts import render


def index(request):
    if request.method == 'POST':
        return render(request, 'rent.html')
    else:
        return render(request, 'landing.html')


def rent(request):
    if request.method == 'POST':
        return render(request, 'rent.html')


def booking(request):
    return render(request, 'booking.html')

