# -*- coding: utf-8 -*-
from django import forms
from .validators import DATE_FORMAT, arrival_date_validator, departure_date_validator, hours_validator, \
    minutes_validator, get_min_arrival_date, get_min_departure_date


class SearchForm(forms.Form):

    locations_list = [('Málaga Airport', 'Málaga Airport')]
    hours_list = [('--', '--'), ('00', '00'), ('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'),
                  ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'),
                  ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'),
                  ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23')]
    minutes_list = [('--', '--'), ('00', '00'), ('15', '15'), ('30', '30'), ('45', '45')]

    arrival_initial_date = get_min_arrival_date().strftime(DATE_FORMAT)
    departure_initial_date = get_min_departure_date().strftime(DATE_FORMAT)

    arrival_location = forms.ChoiceField(choices=locations_list, label='Arrival')
    arrival_date = forms.CharField(initial=arrival_initial_date, validators=[arrival_date_validator])
    arrival_hours = forms.ChoiceField(choices=hours_list, validators=[hours_validator])
    arrival_minutes = forms.ChoiceField(choices=minutes_list, validators=[minutes_validator])

    departure_location = forms.ChoiceField(choices=locations_list)
    departure_date = forms.CharField(initial=departure_initial_date, validators=[departure_date_validator])
    departure_hours = forms.ChoiceField(choices=hours_list, validators=[hours_validator])
    departure_minutes = forms.ChoiceField(choices=minutes_list, validators=[minutes_validator])
