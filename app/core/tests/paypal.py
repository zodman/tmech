from test_plus.test import TestCase
from core.models import Client, Car, Diagnostic, Item, PaypalAccount, show_me_the_money
from autofixture import AutoFixture
from django.utils import timezone
from datetime import timedelta
from django_populate import Faker
from paypal.standard.ipn.tests.test_ipn import IPN_POST_PARAMS
from paypal.standard.models import ST_PP_COMPLETED 
from paypal.standard.ipn.models import PayPalIPN
from django.conf import settings

class PaypalTest(TestCase):
    def setUp(self):
        pop = Faker.getPopulator()
        self.u = self.make_user()
        now = timezone.now() + timedelta(days=3)
        #PaypalAccount.objects.create(user=self.u, expire=now)
        pop.addEntity(Client, 5, {'user': self.u})
        pop.execute()

    def test_decorator(self):
        u = self.make_user(username="u2")
        with self.login(username=u.username):
            self.get("dashboard")
            self.response_302()

    def test_ipn(self):
        data = IPN_POST_PARAMS
        d_format = timezone.now().strftime("%Y%m%d-%H%M%S")
        invoice_id = "{}-{}".format(self.u.id, d_format)
        gross = getattr(settings, "PAYPAL_COST", "20")
        bussines_email = getattr(settings, "PAYPAL_BUSSINES", "zodman-facilitator@gmail.com")
        data.update({
            "invoice": invoice_id,
            "mc_gross": gross,
            "receiver_email": bussines_email,
            #'payment_status': ST_PP_COMPLETED
        })

        with self.login(self.u):
            self.post(
                "paypal-ipn",
                data=data, extra=dict(content_type='application/x-www-form-urlencoded'))
            self.response_200()
            self.assertTrue(self.last_response.content == b"OKAY", msg=self.last_response.content)
            c = PayPalIPN.objects
            self.assertTrue(c.all().count() > 0)
            ipn = c.all()[0]
            ipn._postback = lambda : b"VERIFIED"
            ipn.verify()
            ipn.payment_status = ST_PP_COMPLETED
            ipn.receiver_email = bussines_email
            ipn.invoice = invoice_id
            ipn.mc_gross = gross
            show_me_the_money(sender=ipn)
            self.u.refresh_from_db()
            self.u.paypalaccount
