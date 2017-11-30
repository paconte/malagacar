from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.template.loader import get_template

from rentcar.forms import SearchForm, BookingForm
from rentcar.models import search_available_cars, get_car, Booking
from rentcar.validators import calculate_total_rent_days, convert_dates, date_to_string, extract_time_from_date


def index(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST, prefix='search_form')
        if search_form.is_valid():
            a, b, c, d, e, f = _get_dates_arguments(request, prefix='search_form')
            # get available cars for given dates
            available_cars = search_available_cars(a, b, c, d, e, f)
            # calculate the total numbers of days the car is hired
            rent_days = calculate_total_rent_days(a, b, c, d, e, f)
            # calculate the cost of hiring the cars for the total numbers of days
            prices = list()
            for car in available_cars:
                prices.append(car.calculate_price(rent_days))
            # create booking form
            booking_forms = list()
            for car in available_cars:
                date_from, date_until = convert_dates(a, b, c, d, e, f)
                price = car.calculate_price(rent_days)
                reservation = Booking(date_from=date_from, date_until=date_until, time_period=rent_days,
                                      car=car, total=price)
                booking_form = BookingForm(instance=reservation)
                booking_forms.append(booking_form)

            # add prices to the available cars
            cars_with_prices = zip(available_cars, prices)
            # render
            return render(request, 'landing.html', {'form': search_form, 'available_cars': cars_with_prices})
        else:
            return render(request, 'landing.html', {'form': search_form})
    else:
        return render(request, 'landing.html', {'form': SearchForm(prefix='search_form')})


def booking(request, car_id):
    if request.method == 'POST':
        search_form = SearchForm(request.POST, prefix='search_form')
        if search_form.is_valid():
            # retrieve the car data from db
            car = _get_car(request, car_id, search_form)
            # calculate the dates
            a, b, c, d, e, f = _get_dates_arguments(request, prefix='search_form')
            date_from, date_until, str_date_from, str_date_until, str_time_from, str_time_until \
                = _calculate_dates(a, b, c, d, e, f)
            # calculate price and total rented days
            rent_days = calculate_total_rent_days(a, b, c, d, e, f)
            price = car.calculate_price(rent_days)
            # pre fill out the reservation
            reservation = Booking(date_from=date_from, date_until=date_until, time_period=rent_days,
                                  car=car, total=price)
            booking_form = BookingForm(instance=reservation, prefix='booking_form')
            return render(request, 'booking.html',
                          {'car': car, 'booking_form': booking_form, 'search_form': search_form,
                           'str_date_from': str_date_from, 'str_date_until': str_date_until,
                           'str_time_from': str_time_from, 'str_time_until': str_time_until})
        else:
            return render(request, 'landing.html', {'form': search_form})
    else:
        return render(request, 'landing.html', {'form': SearchForm()})


def booking_confirmation(request):
    if request.method == 'POST':
        booking_form = BookingForm(request.POST, prefix='booking_form')
        search_form = SearchForm(request.POST, prefix='search_form')
        if search_form.is_valid():
            # retrieve the car data from db
            car = _get_car(request, request.POST['booking_form-car'])
            # calculate dates
            a, b, c, d, e, f = _get_dates_arguments(request, prefix='search_form')
            date_from, date_until, str_date_from, str_date_until, str_time_from, str_time_until \
                = _calculate_dates(a, b, c, d, e, f)
            # check booking form
            if booking_form.is_valid():
                booking = _save_booking_form(booking_form)
                context = {'booking': booking, 'str_date_from': str_date_from, 'str_date_until': str_date_until,
                           'str_time_from': str_time_from, 'str_time_until': str_time_until}
                # send confirmation e-mail
                email_html_template = get_template('confirmation_email.html')
                html_content = email_html_template.render(context)
                mailgun_request = send_email(booking.email, html_content)
                print(mailgun_request.json(), mailgun_request.status_code)
                # render confirmation
                return render(request, 'confirmation.html', context)
            else:
                return render(request, 'booking.html',
                              {'car': car, 'booking_form': booking_form, 'search_form': search_form,
                               'str_date_from': str_date_from, 'str_date_until': str_date_until,
                               'str_time_from': str_time_from, 'str_time_until': str_time_until})

    return render(request, 'landing.html', {'form': SearchForm()})


def _get_car(request, car_id, search_form=SearchForm()):
    try:
        car = get_car(int(car_id))
    except ObjectDoesNotExist:
        return render(request, 'landing.html', {'form': search_form})
    except MultipleObjectsReturned:
        return render(request, 'landing.html', {'form': search_form})
    return car


def _get_dates_arguments(request, prefix):
    prefix = prefix + '-'
    return (request.POST[prefix + 'arrival_date'], request.POST[prefix + 'arrival_hours'],
            request.POST[prefix + 'arrival_minutes'], request.POST[prefix + 'departure_date'],
            request.POST[prefix + 'departure_hours'], request.POST[prefix + 'departure_minutes'])


def _calculate_dates(arrival_date, arrival_hours, arrival_minutes, departure_date, departure_hours, departure_minutes):
    date_from, date_until = convert_dates(arrival_date, arrival_hours, arrival_minutes, departure_date, departure_hours,
                                          departure_minutes)
    str_date_from = date_to_string(date_from)
    str_date_until = date_to_string(date_until)
    str_time_from = extract_time_from_date(date_from)
    str_time_until = extract_time_from_date(date_until)
    return date_from, date_until, str_date_from, str_date_until, str_time_from, str_time_until


def _save_booking_form(booking_form):
    new_booking = booking_form.save()
    new_booking.booking_number = _get_next_booking_number(new_booking.id)
    new_booking.save()
    return new_booking


def _get_next_booking_number(booking_id):
    from datetime import date
    part1 = base36encode(date.today().year)
    part2 = base36encode(date.today().month)
    part3 = base36encode(booking_id)
    return part1 + part2 + part3


def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Converts an integer to a base36 string."""
    if not isinstance(number, int):
        raise TypeError('number must be an positive integer')
    if number < 0:
        raise TypeError('number must be an positive integer')

    base36 = ''

    if 0 <= number < len(alphabet):
        return alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return base36


def base36decode(number):
    return int(number, 36)


def send_email(dst_email, html_content):
    import requests
    from django.conf import settings

    print(settings.MAILGUN_KEY)
    excited_user = ""
    you = "bookings"
    your_domain_name = "mail.frevilla.com"
    subject = "Malagacar booking confirmation"

    return requests.post(
        "https://api.mailgun.net/v3/{}/messages".format(your_domain_name),
        auth=("api", "{}".format(settings.MAILGUN_KEY)),
        data={"from": "{}<{}@{}>".format(excited_user, you, your_domain_name),
              "to": "{}".format(dst_email),
              "subject": "{}".format(subject),
              "html": html_content})
