import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unittest
import pytest

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superlists.settings")
django.setup()
from lists.models import Item

class NewVistorTest(unittest.TestCase):
    def setUp(self):
        service = Service('d://chromedriver')
        option = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(service=service, options=option)
        #self. = self.driver
        self.url = "http://127.0.0.1:8000/"

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.url)

        assert "To-Do" in self.browser.title
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        #header_text = self.browser.find_element_by_tag_name('h1').text
        assert 'To-Do' in header_text

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        assert inputbox.get_attribute('placeholder') == 'Enter a to-do item'

        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        assert any(['Buy peacock feathers' in row.text for row in rows])


        # second

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        assert any(['Buy peacock feathers' in row.text for row in rows])
        assert any(['Use peacock feathers to make a fly' in row.text for row in rows])
        time.sleep(3)
        #pytest.fail('finish the test')



if __name__ == '__main__':
    unittest.main(warnings='ignore')