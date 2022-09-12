from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page, view_list
from lists.models import Item, List
from django.core.exceptions import ValidationError


# Create your tests here.

class ListAndItemModelTest(TestCase):
    def test_0001_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        first_item = Item()
        first_item.text = 'The first list item'
        first_item.list = list_
        first_item.save()

        item = Item()
        item.text = 'The second list item'
        item.list = list_
        item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        items = Item.objects.all()
        assert items.count() == 2

        first = items[0]
        second = items[1]
        self.assertEqual(first.list, list_)
        self.assertEqual(second.list, list_)

    def test_0002_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
