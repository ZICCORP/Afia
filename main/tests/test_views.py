from django.test import TestCase
from django.urls import reverse
from main import forms
from decimal import Decimal
from main import models
from unittest.mock import patch
from django.contrib import auth

class TestPage(TestCase):
    def test_home_page_works(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'main/home.html')
        self.assertContains(response,'Afia')

    def test_about_page_works(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'main/about_us.html')
        self.assertContains(response,'Afia')

    def test_contact_us_page_works(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'main/contact_form.html')
        self.assertContains(response,'Afia')
        self.assertIsInstance(response.context['form'],forms.ContactForm)

    def test_contact_us_view_sends_mail(self):
        response = self.client.post(reverse('contact_us'),{'name':'Frank Chuka','message':'Hi team'})
        self.assertEqual(response.status_code,302)

    def test_products_page_returns_active(self):
        models.Product.objects.create(name='4 Bedroom mansion',slug='4-Bedroom-mansion',price=Decimal('30.00'),)
        models.Product.objects.create(name='Tie',slug='tie',price=Decimal('3.99'),active=False)
        response = self.client.get(reverse("products",kwargs={"tag":"all"}))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'Afia')
        product_list = models.Product.objects.active().order_by('name')
        self.assertEqual(list(response.context['object_list']),list(product_list),)

    def test_products_page_filters_by_tag_and_active(self):
        cb =  models.Product.objects.create(name='4 Bedroom mansion',slug='4-Bedroom-mansion',price=Decimal('30.00'),)
        cb.tags.create(name='Luxury',slug='luxury')
        models.Product.objects.create(name='Tie',slug='tie',price=Decimal('3.99'),)
        response = self.client.get(reverse("products",kwargs={"tag":'luxury'}))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'Afia')
        product_list = models.Product.objects.active().filter(tags__slug='luxury').order_by('name')
        self.assertEqual(list(response.context['object_list']),list(product_list),)

    def test_user_signup_page_loads_correctly(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'main/signup.html')
        self.assertContains(response,'Afia')
        self.assertIsInstance(response.context['form'],forms.UserCreationForm)

    def test_user_signup_page_submission_works(self):
        post_data = {
            "email":'user@domain.com',
            "password1":'abcdef11',
            "password2":'abcdef11',
        }
        with patch.object(forms.UserCreationForm,"send_mail") as mock_send:
            response=self.client.post(reverse('signup'),post_data)
        self.assertEqual(response.status_code,302)
        self.assertTrue(models.User.objects.filter(email="user@domain.com").exists())
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        mock_send.assert_called_once()


    def test_address_list_page_returns_only_owned(self):
       
        user1 =models.User.objects.create_user("user1@gmail.com",'abcdef11')
        user2 =models.User.objects.create_user("user2@gmail.com",'abcdef11')
        models.Address.objects.create(user=user1,name='Frank Chuka',address1='flat 3',address2='14 millenium estate',city='Ikeja',country='ng')
        add1 = models.Address.objects.get(user=user1)
        self.client.force_login(user2)
        response = self.client.get(reverse("address_list"))
        self.assertEqual(response.status_code,200)
        address_list = models.Address.objects.filter(user=user2)
        self.assertEqual(list(response.context['object_list']),list(address_list))

    def test_address_create_stores_user(self):
        models.User.objects.create_user("user1@gmail.com",'abcdef11')
        user1 = models.User.objects.get(email="user1@gmail.com")
        post_data = {"name":"Frank Zuck","address1":'1 catherina str',"address2":'','zip_code':'FA23GW','city':'Lekki','country':'ng',}
        self.client.force_login(user1)
        self.client.post(reverse('address_create'),post_data)
        self.assertTrue(models.Address.objects.filter(user=user1).exists())

    def test_add_to_basket_logged_in_works(self):
        user1 = models.User.objects.create_user("user@email.com",'testpass123')
        d = models.Product.objects.create(name='Detergent',slug='detergent',price=Decimal('10.00'),)
        rl = models.Product.objects.create(name='Rechargeable Lantern',slug='rechargeable-lantern',price=Decimal('25.99'),)
        self.client.force_login(user1)
        response = self.client.get(reverse('add_to_basket'),{'product_id':d.id})
        self.assertTrue(models.Basket.objects.filter(user=user1).exists())
        self.assertEqual(models.BasketLine.objects.filter(basket__user=user1).count(),1)
        response = self.client.get(reverse('add_to_basket'),{'product_id':rl.id})
        self.assertEqual(models.BasketLine.objects.filter(basket__user=user1).count(),2)

    def test_add_to_basket_login_merge_works(self):
        user4 = models.User.objects.create_user(email='user4@gmail.com',password='testpass123')
        d = models.Product.objects.create(name='Detergent',slug='detergent',price=Decimal('5.99'))
        rl = models.Product.objects.create(name='Rechargeable Lantern',slug='rechargeable-lantern',price=Decimal('15.99'))
        basket = models.Basket.objects.create(user=user4)
        models.BasketLine.objects.create(basket=basket,product=d,quantity=2)
        response = self.client.get(reverse('add_to_basket'),{'product_id':rl.id})
        response = self.client.post(reverse('login'), {'email':'user4@gmail.com','password':'testpass123'},)
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        self.assertTrue(models.Basket.objects.filter(user=user4).exists())
        basket = models.Basket.objects.get(user=user4)
        self.assertEqual(basket.count(),3)





    