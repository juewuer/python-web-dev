from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page, view_list
from lists.models import Item, List
from django.core.exceptions import ValidationError


# Create your tests here.

class ListAndItemModelTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, "")

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

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

    #
    def test_0003_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item.objects.create(list=list_, text='bla')
            item.full_clean()

    def test_0004_can_save_same_item_to_different_lists(self):
        list_ = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        item = Item.objects.create(list=list2, text='bla')
        item.full_clean()