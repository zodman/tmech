from test_plus.test import TestCase
from core.models import Client, Car, Diagnostic, Item
from autofixture import AutoFixture
from django.utils import timezone

class ServiceTest(TestCase):

    def setUp(self):
        self.u = self.make_user()
        client_fixture = AutoFixture(Client)
        carfixture = AutoFixture(Car,follow_fk=True)
        self.clients = client_fixture.create(10)
        self.cars = carfixture.create(10)
        self.services = AutoFixture(Diagnostic, follow_fk=True).create(1)

    def __test_manager(self):
        AutoFixture(Diagnostic, generate_fk=True).create(100)
        s = Diagnostic.objects.all().profit()
        

    def test_search_client(self):
        client_id = self.clients[0].id
        with self.login(self.u):
            self.get("get_cars", data={'client_id': client_id})
            self.response_200()
        
    def test_service_search(self):
        with self.login(self.u):
            self.get_check_200("service_search")
        
    def test_delete_client(self):
        ids = [i.id for i in self.clients]
        with self.login(self.u):
            self.post("delete_clients", data={'ids': ids})
            self.response_200()

    def test_list(self):
        with self.login(self.u):
            self.get_check_200("service_list")
            self.get_check_200("service_detail", pk=self.services[0].id)


    def test_change_status_service(self):
        service = self.services.pop()

        with self.login(self.u):
            self.post("service_change_status", pk=service.id, 
                      data={'status':service.STATUS[1]})
            self.response_200()
            hh = timezone.now().strftime("%Y-%m-%d %H:%M")
            data = {
                "reception_datetime": hh,
                "initial":"init",
                "final":"final",
                "repairs":"repairs",
                "notes":"notes"
            }
            self.post("service_edit", pk=service.id, data=data)
            self.response_200()
        
            
    def test_add_items(self):
        service = self.services.pop()
        data = {
            'quantity':1,
            'description': 'foo bar',
            'price': 100.00
        }

        with self.login(self.u):
            self.post("service_add_item", pk=service.id, data=data)
            self.response_200()
            self.assertResponseHeaders({"X-IC-Redirect":self.reverse("service_detail", pk=service.id)})
            data = {
                'quantity':-1,
                'description': 'foo bar',
                'price': 100.00
            }
            self.post("service_add_item", pk=service.id, data=data)
            self.response_200()
            self.assertInContext("form")


    def test_delete_item(self):
        items = AutoFixture(Item, field_values = {'user':self.u},
            follow_fk=True).create(2)
        for i in items:
            with self.subTest(i=i) and self.login(self.u):
                self.post("service_delete_item", pk=i.id)
                self.response_200()

