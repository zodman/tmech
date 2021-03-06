from test_plus.test import TestCase
from core.models import Client, Car, PaypalAccount
from autofixture import AutoFixture
from django.utils import timezone
from datetime import timedelta

class ClientTest(TestCase):

    def setUp(self):
        self.u = self.make_user()
        now = timezone.now() + timedelta(days=3)
        PaypalAccount.objects.create(user=self.u, expire=now)
        client_fixture = AutoFixture(Client, follow_fk=True)
        carfixture = AutoFixture(Car, follow_fk=True)
        self.clients = client_fixture.create(100)
        self.cars = carfixture.create(1)

    def test_search_client(self):
        with self.login(self.u):
            self.get("search_client", data={'q':''})
            self.response_200()

    def test_edit_client(self):
        with self.login(self.u):
            client = self.clients.pop()
            self.get_check_200("edit_client", pk=client.id)
        

    def test_add_client(self):
        data = {
            'name': 'Foo',
            'phone': '123123123',
            'email': 'bar@foo.com'
        }
        
        with self.login(self.u):
            self.post("client_add", data=data)
            self.response_200()
#            self.print_form_errors()
            self.assertTrue(Client.objects.filter(name='Foo').exists())

    def test_delete_client(self):
        ids = [i.id for i in self.clients]
        with self.login(self.u):
            self.post("delete_clients", data={'ids': ids})
            self.response_200()

    def test_list(self):

        with self.login(self.u):
            self.get_check_200("client_list")
            self.get_check_200("car_list")
