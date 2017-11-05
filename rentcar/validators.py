import datetime
import pytz
from django.core.exceptions import ValidationError

DATE_FORMAT = "%d/%m/%Y"
TIME_ZONE = pytz.timezone('Europe/Berlin')
MIN_ARRIVAL_DATE_DELTA = 1
MIN_DEPARTURE_DATE_DELTA = MIN_ARRIVAL_DATE_DELTA + 7
MINUTES_LIST = ['00', '15', '30', '45']
HOURS_LIST = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '14', '15', '16', '17',
              '18', '19', '20', '21', '22', '23']


def get_min_arrival_date(delta=MIN_ARRIVAL_DATE_DELTA):
    arrival_delta = datetime.timedelta(days=delta)
    now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    arrival_initial_date = now + arrival_delta
    return arrival_initial_date


def get_max_arrival_date():
    return get_min_arrival_date(MIN_DEPARTURE_DATE_DELTA)


def arrival_date_validator(value):
    min_arrival_date = get_min_arrival_date()
    arrival_date = datetime.datetime.strptime(value, DATE_FORMAT)
    if not arrival_date >= min_arrival_date:
        msg = u"Wrong arrival date"
        raise ValidationError(msg)


def departure_date_validator(value):
    min_departure_date = get_max_arrival_date()
    departure_date = datetime.datetime.strptime(value, DATE_FORMAT)
    if not departure_date >= min_departure_date:
        msg = u"Wrong departure date"
        raise ValidationError(msg)


def minutes_validator(value):
    if value not in MINUTES_LIST:
        msg = u"Wrong minutes"
        raise ValidationError(msg)


def hours_validator(value):
    if value not in HOURS_LIST:
        msg = u"Wrong minutes"
        raise ValidationError(msg)
