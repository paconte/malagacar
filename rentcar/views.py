from django.shortcuts import render

from rentcar.forms import SearchForm


def index(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            return render(request, 'landing.html', {'form': search_form, 'search_result': list('a')})
        else:
            return render(request, 'landing.html', {'form': search_form, 'search_result': list()})
    else:
        return render(request, 'landing.html', {'form': SearchForm(), 'search_result': list()})


def booking(request):
    return render(request, 'booking.html')

