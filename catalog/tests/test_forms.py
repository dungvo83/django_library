import datetime
from django.test import TestCase
from django.utils import timezone

from catalog.forms import RenewBookForm


class RenewBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        #print(">>", form.fields['due_back'].label)
        field_label = form.fields['due_back'].label
        #self.assertEqual(form.fields['due_back'].label, '')
        self.assertTrue(field_label == None or field_label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        field_help_text = form.fields['due_back'].help_text
        self.assertEqual(field_help_text, 'Enter a date between now and 4 weeks (default 3).')

    def test_renew_form_date_in_past(self):
        past = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'due_back': past})
        #print(">>", form.is_valid())
        self.assertFalse(form.is_valid())
        #self.assertEqual(past, form.is_valid())

    def test_renew_form_date_too_far(self):
        too_far = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'due_back': too_far})
        self.assertFalse(form.is_valid())
        #self.assertEqual(too_far, datetime.date.today())

    def test_renew_form_date_today(self):
        today = datetime.date.today()
        form = RenewBookForm(data={'due_back': today})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_far(self):
        far = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'due_back': far})
        self.assertTrue(form.is_valid())
        #self.assertEqual(far, datetime.date.today())
        #self.assertEqual(far, datetime.date.today() + datetime.timedelta(weeks=4))
