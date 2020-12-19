from django.urls import path
from django.views.generic import TemplateView,DetailView
from main import views
from main import models

urlpatterns = [
    path('signup/',views.SignupView.as_view(),name='signup'),
    path('products/<slug:tag>/',views.ProductListView.as_view(),name='products',),
    path('product/<slug:slug>/', DetailView.as_view(model=models.Product),name='product',),
    path('about-us/',TemplateView.as_view(template_name='main/about_us.html'),name='about_us'),
    path('contact-us/',views.ContactUsView.as_view(),name='contact_us'),
    path('',TemplateView.as_view(template_name='main/home.html'),name='home'),
]