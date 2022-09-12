import sys
import time
import os
import django

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



from .base import FunctionalTest

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superlists.settings")
#django.setup()
from lists.models import Item

class NewVistorTest(FunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.server_url)

        assert "To-Do" in self.browser.title
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        # header_text = self.browser.find_element_by_tag_name('h1').text
        assert 'To-Do' in header_text

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        assert inputbox.get_attribute('placeholder') == 'Enter a to-do item'

        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        time.sleep(3)
        print(f'{edith_list_url =}')
        assert '/lists/' in edith_list_url

        self.check_for_row_in_list_table('Buy peacock feathers')

        # second
        self.browser.get(self.server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            print(f'  -----------{row.text}')

        self.check_for_row_in_list_table('Use peacock feathers to make a fly')

        # pytest.fail('finish the test')

        self.browser.quit()
        service = Service('d://chromedriver')
        option = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(service=service, options=option)

        self.browser.get(self.server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        assert "Buy peacock feathers" not in page_text
        assert "Use peacock feathers to make a fly" not in page_text

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('By milk')
        inputbox.send_keys(Keys.ENTER)
        francis_list_url = self.browser.current_url
        assert '/lists/' in francis_list_url
        print(f'{edith_list_url =} {francis_list_url =}')
        assert francis_list_url != edith_list_url

        page_text = self.browser.find_element(by=By.TAG_NAME, value='body').text
        assert "Buy peacock feathers" not in page_text
        assert "Use peacock feathers to make a fly" not in page_text

