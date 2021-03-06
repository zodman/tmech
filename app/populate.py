import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
import django
from django.conf import settings
django.setup()
from django_seed import Seed
from core.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker
from faker_car import CarProvider

import sys


user = User.objects.get(username=sys.argv[1])

f = Faker()
f.add_provider(CarProvider)

print("delete objects")
Client.objects.all().delete()
Car.objects.all().delete()
Item.objects.all().delete()
Diagnostic.objects.all().delete()
print("create entities")
fake = Seed.seeder()
expire= fake.faker.date_time_between(start_date='+5m', end_date="+2y")

PaypalAccount.objects.get_or_create(user=user, defaults={'expire':expire})

fake.add_entity(Client, 80, {
    'user':user,
    'name': lambda x: fake.faker.name()
})
fake.add_entity(Car, 200,{
    'user': user,
    'brand': lambda x: f.car(),
    'model': lambda x: f.car_model()[1]
    })

fake.add_entity(Diagnostic, 300, {
    'user':user,
    'reception_datetime': lambda x: timezone.make_aware(
            fake.faker.date_time_between(
                start_date="-5m", end_date="now"),is_dst=False),
    'status': lambda x: fake.faker.random_element(Diagnostic.STATUS)[0],

})

fake.add_entity(Item, 300, {
     'user':user,
})

print("execute")
fake.execute()


