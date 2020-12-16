from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('about-us/',TemplateView.as_view(template_name='main/about_us.html'),name='about_us'),
    path('',TemplateView.as_view(template_name='main/home.html'),name='home'),
]