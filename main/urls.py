from django.urls import path
from django.views.generic import TemplateView,DetailView
from django.contrib.auth import views as auth_views
from main import forms
from main import views
from main import models


urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='main/login.html',form_class=forms.AuthenticationForm,),name='login',),
    path('signup/',views.SignupView.as_view(),name='signup'),
    path('address/',views.AddressListView.as_view(),name='address_list'),
    path('address/create/',views.AddressCreateView.as_view(),name='address_create'),
    path('address/<int:pk>/',views.AddressUpdateView.as_view(),name='address_update'),
    path('address/<int:pk>/delete/',views.AddressDeleteView.as_view(),name='address_delete'),
    path('products/<slug:tag>/',views.ProductListView.as_view(),name='products',),
    path('product/<slug:slug>/', DetailView.as_view(model=models.Product),name='product',),
    path('add_to_basket/',views.add_to_basket,name='add_to_basket',),
    path('about-us/',TemplateView.as_view(template_name='main/about_us.html'),name='about_us'),
    path('contact-us/',views.ContactUsView.as_view(),name='contact_us'),
    path('',TemplateView.as_view(template_name='main/home.html'),name='home'),
]