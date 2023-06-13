'''
    # https://faker.readthedocs.io/en/master/
    $ pip install faker # install faker module
    python manage.py flush # delete all exists data from db. dont forget: createsuperuser
    python manage.py shell
    from flight_app.faker import run
    run()
    exit()
'''


from .models import Flight, Passenger, Reservation
import random
from django.utils import timezone
from datetime import datetime
from faker import Faker

from django.contrib.auth.models import User
import pytz

def add_flights():
    airlines = [("Spirit", "NK"), ("Frontier", "F9"), ("American", "AA"), ("United", "UA")]
    cities = ["New York", "Miami", "Boston", "Chicago", "Los Angles", "Dallas", "Denver"]

    fake = Faker() 
    for _ in range(200):
        flight = Flight()
        number = random.randint(100,999)
        airline = random.choice(airlines)
        flight.airlines = airline[0]
        flight.flight_number = airline[1] + str(number)
        places = random.sample(cities,2)
        flight.departure_city = places[0]
        flight.arrival_city = places[1]
        flight.date = fake.date_between(start_date=datetime(2023,3,1), end_date=datetime(2023,7,31))
        flight.time = fake.time()
        # flight.datetime = datetime.combine(flight.date, datetime.strptime(flight.time, "%H:%M:%S").time())
        

        # flight.datetime = flight.datetime.replace(tzinfo=pytz.UTC)
        flight.save()

    print('Flights created')

def add_user():
    fake = Faker()
    for _ in range(10):
        user = User()
        user.first_name = fake.first_name()
        user.last_name = fake.last_name()
        user.email = fake.free_email() 
        user.username = user.email
        user.set_password("qazqwe123")
        user.save()
    print('Users created')

def add_passanger():
    fake = Faker()
    for _ in range(10):
        user = Passenger()
        user.first_name = fake.first_name()
        user.last_name = fake.last_name()
        user.email = fake.free_email() 
        user.phone_number = fake.phone_number()
        user.save()
    print('Passangers created')

def add_reservation():
    fake = Faker()
    users = User.objects.all()
    passangers = Passenger.objects.all()
    flights = Flight.objects.all()
    for _ in range(50):
        reservation = Reservation()
        reservation.user = users[fake.random_int(min=0, max=len(users)-1)]
        reservation.flight = flights[fake.random_int(min=0, max=len(flights)-1)]
        reservation.save()
        count = fake.random_int(min=1, max=3)
        for _ in range(count):
            reservation.passenger.add(passangers[fake.random_int(min=0, max=len(users)-1)])
        reservation.save()
        
    print('Reservations created')

def run():
    print('Fake data generation started')
    add_flights()
    add_user()
    add_passanger()
    add_reservation()
    print('Fake data generation completed')