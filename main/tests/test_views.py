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

