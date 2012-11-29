import unittest
from models import Payment
from django.contrib.auth.models import User


class PaymentTest(unittest.TestCase):
    
    def setUp(self):
        user = User.objects.create(username='kenneth')
        self.payment = Payment.objects.create_payment(user, 1000.00, 'UGX')
    
    def testingPayment(self):
        self.assertEqual(self.payment.recievemoney, True, 'Testing receive function')
        self.assertEqual(self.payment.sendmoney, True, 'Testing send function')
        self.assertEqual(self.payment.pushmoney, True, 'Testing push function')
        