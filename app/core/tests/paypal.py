from test_plus.test import TestCase
from core.models import Client, Car, Diagnostic, Item, PaypalAccount
from autofixture import AutoFixture
from django.utils import timezone
from datetime import timedelta
from django_populate import Faker



class PaypalTest(TestCase):
    def setUp(self):
        pop = Faker.getPopulator()
        self.u = self.make_user()
        now = timezone.now() + timedelta(days=3)
        PaypalAccount.objects.create(user=self.u, expire=now)
        pop.addEntity(Client, 5, {'user': self.u})
        pop.execute()
    
    def test_decorator(self):
        u = self.make_user(username="u2")
        with self.login(username=u.username):
            self.get("dashboard")
            self.response_302()
