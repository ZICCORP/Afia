from django.views.generic.edit import FormView
from main import forms
from django.urls import reverse

class ContactUsView(FormView):
    template_name = 'main/contact_form.html'
    form_class = forms.ContactForm
    success_url = '/'


    def form_valid(self,form):
        form.send_mail()
        return super().form_valid(form)