from decimal import Decimal
from django.test import TestCase
from main import models


class TestModel(TestCase):
    def test_active_manager_works(self):
        models.Product.objects.create(name='Jacket',price=Decimal('70.00'))
        models.Product.objects.create(name='Pant',price=Decimal('10.99'))
        models.Product.objects.create(name='Tie',price=Decimal('6.99'),active=False)
        self.assertEqual(len(models.Product.objects.active()),2)