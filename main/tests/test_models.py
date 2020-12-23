from decimal import Decimal
from django.test import TestCase
from main import models


class TestModel(TestCase):
    def test_active_manager_works(self):
        models.Product.objects.create(name='Jacket',price=Decimal('70.00'))
        models.Product.objects.create(name='Pant',price=Decimal('10.99'))
        models.Product.objects.create(name='Tie',price=Decimal('6.99'),active=False)
        self.assertEqual(len(models.Product.objects.active()),2)


    def test_create_order_works(self):
        
        p1 = models.Product.objects.create(name='The cathedral and the bazaar',price=Decimal('30.99'))
        p2 = models.Product.objects.create(name='Pride and Prejudice',price=Decimal(10.99))
        user1 = models.User.objects.create_user('user1','testpass123')
        billing = models.Address.objects.create(user=user1,name="Frank Chuka",address1="12 dell road",city="London",country="uk",)
        shipping = models.Address.objects.create(user=user1,name="Frank Chuka",address1="1 Dean road",city="London",country="uk",)
        basket = models.Basket.objects.create(user=user1)
        models.BasketLine.objects.create(basket=basket,product=p1)
        models.BasketLine.objects.create(basket=basket,product=p2)
        with self.assertLogs("main.models", level="INFO") as cm:
            order = basket.create_order(billing,shipping)
        self.assertGreaterEqual(len(cm.output),1)
        order.refresh_from_db()
        self.assertEqual(order.user,user1)
        self.assertEquals(order.billing_address1,"12 dell road") 
        self.assertEquals(order.shipping_address1,"1 Dean road")
        self.assertEqual(order.lines.all().count(),2)
        lines = order.lines.all()
        self.assertEqual(lines[0].product,p1)
        self.assertEqual(lines[1].product,p2)


 
