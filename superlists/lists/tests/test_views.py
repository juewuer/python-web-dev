from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.views import home_page, view_list
from lists.models import Item, List
from lists.forms import STR_EMPYT_LIST_ERROR, ItemForm


# Create your tests here.

class SmokeTest(TestCase):
    def test_bad_maths(self):
        self.assertEqual(1 + 1, 2)


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_0001_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        content = response.content.decode("utf-8-sig").encode('utf-8')
        # print(f'{type(content) =}, {content}')

        self.assertTrue(content.startswith(b"<html>"))
        self.assertIn(b'<title>To-Do Lists</title>', content)
        self.assertTrue(content.endswith(b"</html>"))
        # failed for csrf
        # self.assertEqual(response.content.decode(), render_to_string('home.html'))

    '''
    def test_0004_home_page_displays_all_list_item(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)
        request = HttpRequest()
        response = view_list(request)
        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())
    '''


class ListViewTest(TestCase):
    '''
    def test_users_list_template(self):
        response = self.client.get('/lists/all/')

        self.assertTemplateUsed(response, 'list.html')
    '''

    def test_0002_users_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')

        self.assertTemplateUsed(response, 'list.html')

    def test_0003_display_only_items_for_that_list(self):
        list1 = List.objects.create()
        Item.objects.create(text='itemey 1.1', list=list1)
        Item.objects.create(text='itemey 1.2', list=list1)
        list2 = List.objects.create()
        Item.objects.create(text='itemey 2.1', list=list2)
        Item.objects.create(text='itemey 2.2', list=list2)
        response = self.client.get(f"/lists/{list1.id}/")
        content = response.content.decode("utf-8-sig").encode('utf-8')
        # print(f'{type(content) =}, {content}')

        self.assertContains(response, 'itemey 1.1')
        self.assertContains(response, 'itemey 1.2')
        self.assertNotContains(response, 'itemey 2.1')
        self.assertNotContains(response, 'itemey 2.2')

    """
    def test_display_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)
        response = self.client.get("/lists/all/")

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
    """

    def test_0005_passes_correst_list_to_templeate(self):
        list2 = List.objects.create()
        list1 = List.objects.create()
        response = self.client.get(f'/lists/{list1.id}/')
        self.assertEqual(response.context['list'], list1)

    def test_0006_validation_error_end_up_on_list_page(self):
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/', data={"text": ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

        content = response.content.decode("utf-8-sig").encode('utf-8')
        print(f'test_0006_validation_error_end_up_on_list_page {type(content) =}, {content}')

        self.assertContains(response, escape("You can't have an empty list item"))


class NewListTest(TestCase):
    def test_0001_saving_a_POST_request(self):
        print(f'Before post')
        self.client.post('/lists/new', data={'text': 'A new list item'})

        print(f'{Item.objects.count()}, {Item.objects =}')
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_0003_home_page_redirect_after_post(self):
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        list_ = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/lists/{list_.id}/')

    def test_0004a_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_0004b_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(STR_EMPYT_LIST_ERROR))

    def test_0004c_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_0005_invalid_list_items_arent_saved(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class NewItemTest(TestCase):
    def test_0001_can_save_a_POST_request_to_an_existing_list(self):
        list2 = List.objects.create()
        list1 = List.objects.create()
        response = self.client.post(f'/lists/{list1.id}/',
                                    data={'text': 'A new list item for existing list'})
        print(f'test_0001_can_save_a_POST_request_to_an_existing_list: {response.status_code}, {response = }')
        print(f'{list(Item.objects.all()) = }')
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item for existing list')
        self.assertEqual(new_item.list, list1)

    def test_0002_redirect_to_list_view(self):
        list2 = List.objects.create()
        list1 = List.objects.create()
        response = self.client.post(f'/lists/{list1.id}/',
                                    data={'text': 'A new list item for existing list'})
        self.assertRedirects(response, f'/lists/{list1.id}/')
