from test_plus.test import TestCase
from core.models import Client, Car, PaypalAccount
from autofixture import AutoFixture
from django.utils import timezone
from datetime import timedelta


class CarTest(TestCase):

    def setUp(self):
        self.u = self.make_user()
        client_fixture = AutoFixture(Client, follow_fk=True)
        carfixture = AutoFixture(Car, follow_fk=True)
        self.clients = client_fixture.create(10)
        self.cars = carfixture.create(1)
        now = timezone.now() + timedelta(days=3)
        PaypalAccount.objects.create(user=self.u, expire=now)


    def test_delete_cars(self):
        data = {'ids': [i.id for i in self.cars]}
        with self.login(self.u):
            self.post("delete_cars", data=data)
            self.response_200()

    def test_list(self):
        with self.login(self.u):
            self.get_check_200("car_list")

    def test_search(self):
        with self.login(self.u):
            self.get_check_200("search_car", data={'search':'xtrail'})
            self.get_check_200("car_client_search", data={'search':'xtrail'})

    def test_add_car(self):
        data = {
            'client_id': self.clients[0].id,
            'brand': 'brandfoo',
            'model': 'modelbar',
            'year': 2019 
        }
        with self.login(self.u):
            self.post("car_add", data=data)
            self.response_200()
            # raise Error for duplicate car
            self.post("car_add", data=data)
            self.assertInContext("form")
            form = self.get_context("form")
            self.assertTrue(form.non_field_errors())

