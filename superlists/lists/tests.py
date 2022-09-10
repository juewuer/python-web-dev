from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page, view_list
from lists.models import Item, List


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
        print(f'{type(content) =}, {content}')

        self.assertTrue(content.startswith(b"<html>"))
        self.assertIn(b'<title>To-Do Lists</title>', content)
        self.assertTrue(content.endswith(b"</html>"))
        # failed for csrf
        # self.assertEqual(response.content.decode(), render_to_string('home.html'))

    """
    # move to NewListTest
    def test_0002_home_page_can_save_a_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    # move to NewListTest
    def test_0003_home_page_redirect_after_post(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/all/')
        return

        content = response.content.decode("utf-8-sig").encode('utf-8').decode()
        self.assertTrue('A new list item' in content)
        expected_html = render_to_string('home.html', {'new_item_text': 'A new list item'})
        # print(f'{type(content.decode()) = }')
        # print(f'{content.decode() = }')
        self.assertEqual(content[:100], expected_html[:100])
    """

    def test_0004_home_page_displays_all_list_item(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list = list_)
        Item.objects.create(text='itemey 2', list = list_)
        request = HttpRequest()
        response = view_list(request)
        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())


class ListViewTest(TestCase):
    def test_users_list_template(self):
        response = self.client.get('/lists/all/')

        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list = list_)
        Item.objects.create(text='itemey 2', list = list_)
        response = self.client.get("/lists/all/")

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')


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

        saved_list= List.objects.first()
        self.assertEqual(saved_list, list_)

        items = Item.objects.all()
        assert items.count() == 2

        first = items[0]
        second = items[1]
        self.assertEqual(first.list, list_)
        self.assertEqual(second.list, list_)

class NewListTest(TestCase):
    def test_saving_a_POST_request(self):

        print(f'Before post')
        self.client.post('/lists/new', data = {'item_text': 'A new list item'})

        print(f'{Item.objects.count()}, {Item.objects =}')
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_0003_home_page_redirect_after_post(self):
        response = self.client.post('/lists/new', data = {'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/all/')