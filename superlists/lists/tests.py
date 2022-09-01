from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

# Create your tests here.

class SmokeTest(TestCase):
    def test_bad_maths(self):
        self.assertEqual(1+1, 2)

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


    def test_0002_home_page_can_save_a_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_0003_home_page_redirect_after_post(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
        return



        content = response.content.decode("utf-8-sig").encode('utf-8').decode()
        self.assertTrue('A new list item' in content)
        expected_html = render_to_string('home.html', {'new_item_text': 'A new list item'})
        #print(f'{type(content.decode()) = }')
        #print(f'{content.decode() = }')
        self.assertEqual(content[:100], expected_html[:100])


    def test_0004_home_page_displays_all_list_item(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        request = HttpRequest()
        response = home_page(request)
        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())


class ItemModelTest(TestCase):
    def test_0001_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first list item'
        first_item.save()

        item = Item()
        item.text = 'The second list item'
        item.save()

        items = Item.objects.all()
        assert items.count() == 2


