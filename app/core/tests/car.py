from test_plus.test import TestCase
from core.models import Client, Car
from autofixture import AutoFixture


class CarTest(TestCase):

    def setUp(self):
        client_fixture = AutoFixture(Client)
        carfixture = AutoFixture(Car, generate_fk=True)
        self.clients = client_fixture.create(10)
        self.cars = carfixture.create(10)

    def test_delete_cars(self):
        data = {'ids': [i.id for i in self.cars]}
        self.post("delete_cars", data=data)
        self.response_200()

    def test_list(self):
        self.get_check_200("car_list")

    def test_search(self):
        self.get_check_200("search_car", data={'search':'xtrail'})
        self.get_check_200("car_client_search", data={'search':'xtrail'})
        

    def test_add_car(self):
        data = {
            'client_id': self.clients[0].id,
            'brand': 'brandfoo',
            'model': 'modelbar',
            'year': 2019 
        }
        self.post("car_add", data=data)
        self.response_200()

        # raise Error for duplicate car
        self.post("car_add", data=data)
        self.assertInContext("form")
        form = self.get_context("form")
        self.assertTrue(form.non_field_errors())

