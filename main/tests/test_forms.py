from django.test import TestCase
from django.core import mail
from main import forms


class TestForm(TestCase):
    def test_valid_contact_us_form_sends_email(self):
        form = forms.ContactForm({'name':'Frank Chuka','message':'Hello team'})
        self.assertTrue(form.is_valid())
        with self.assertLogs('main.forms',level='INFO') as cm:
            form.send_mail()

        self.assertEqual(len(mail.outbox),1)
        self.assertEqual(mail.outbox[0].subject,'Site Message')

    def test_invalid_contact_us_form(self):
        form = forms.ContactForm({'name':'Frank chuka'})
        self.assertFalse(form.is_valid())