from test_plus.test import TestCase
from core.models import Client, Car
from autofixture import AutoFixture


class ServiceTest(TestCase):

    def setUp(self):
        client_fixture = AutoFixture(Client)
        carfixture = AutoFixture(Car, generate_fk=True)
        self.clients = client_fixture.create(10)
        self.cars = carfixture.create(10)

    def test_search_client(self):
        client_id = self.clients[0].id
        self.get("get_cars", data={'client_id': client_id})
        self.response_200()

    def __test_add_client(self):
        data = {
            'name': 'Foo',
            'phone': '123123123',
            'email': 'bar@foo.com'
        }
        self.post("client_add", data=data)
        self.response_200()
        self.assertTrue(Client.objects.filter(name='Foo').exists())

    def __test_delete_client(self):
        ids = [i.id for i in self.clients]
        self.post("delete_clients", data={'ids': ids})
        self.response_200()

    def test_list(self):
        self.get_check_200("service_list")
