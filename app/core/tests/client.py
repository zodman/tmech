from test_plus.test import TestCase
from core.models import Client, Car
from autofixture import AutoFixture


class ClientTest(TestCase):

    def setUp(self):
        client_fixture = AutoFixture(Client)
        carfixture = AutoFixture(Car, generate_fk=True)
        self.clients = client_fixture.create(100)
        self.cars = carfixture.create(1)

    def test_search_client(self):
        self.get("search_client", data={'q':''})
        self.response_200()

    def test_add_client(self):
        data = {
            'name': 'Foo',
            'phone': '123123123',
            'email': 'bar@foo.com'
        }
        self.post("client_add", data=data)
        self.response_200()
        self.assertTrue(Client.objects.filter(name='Foo').exists())

    def test_delete_client(self):
        ids = [i.id for i in self.clients]
        self.post("delete_clients", data={'ids': ids})
        self.response_200()

    def test_list(self):
        self.get_check_200("client_list")
        self.get_check_200("car_list")