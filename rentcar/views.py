from django.shortcuts import render

from rentcar.forms import SearchForm
from rentcar.models import search_available_cars


def index(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        print(search_form.fields['arrival_date'])
        if search_form.is_valid():
            available_cars = search_available_cars(
                request.POST['arrival_date'],
                request.POST['arrival_hours'],
                request.POST['arrival_minutes'],
                request.POST['departure_date'],
                request.POST['departure_hours'],
                request.POST['departure_minutes'])
            return render(request, 'landing.html', {'form': search_form, 'available_cars': available_cars})
        else:
            return render(request, 'landing.html', {'form': search_form, 'search_result': list()})
    else:
        return render(request, 'landing.html', {'form': SearchForm(), 'search_result': list()})


def booking(request):
    return render(request, 'booking.html')

