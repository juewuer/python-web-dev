from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from django.core.exceptions import ValidationError

from lists.views import home_page, view_list
from lists.models import Item, List
from lists.forms import ItemForm


# Create your tests here.

class ItemFormTest(TestCase):
    def test_0001_form_render_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
        print(f'{form = }, {form.as_p() = }')

    def test_0002_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ["You can't have an empty list item"])
