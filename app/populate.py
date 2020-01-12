import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
import django
from django.conf import settings
django.setup()
from django_seed import Seed
from core.models import *
from django.contrib.auth.models import User
from django.utils import timezone

cars = """
Ford
Cadillac
Maserati
Skoda
Rolls-Royce
Maybach
Toyota
Abarth
Infiniti
Audi
Mini
Dacia
Renault
Peugeot
BMW
Honda
BMW
Caterham
Holden
Mini
"""


user = User.objects.get(username="taller")

print("delete objects")
Client.objects.all().delete()
Car.objects.all().delete()
Item.objects.all().delete()
Diagnostic.objects.all().delete()
print("create entities")
fake = Seed.seeder()
fake.add_entity(Client, 200, {
    'user':user,
    'name': lambda x: fake.faker.name()
})
fake.add_entity(Car, 800,{
    'user':user,
    'brand': lambda x: fake.faker.random_element(cars.split())
    })

fake.add_entity(Diagnostic, 800, {
    'user':user,
    'reception_datetime': lambda x: timezone.make_aware(
            fake.faker.date_time_between(
                start_date="-1y", end_date="now")),
    'status': lambda x: fake.faker.random_element(Diagnostic.STATUS)[0],

})

fake.add_entity(Item, 300, {
     'user':user,
})

print("execute")
fake.execute()


