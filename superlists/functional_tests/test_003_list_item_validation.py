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

    def test_0001_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        print(f'test_0001_cannot_add_empty_list_items: {self.server_url = }')
        inputbox = self.browser.find_element(By.ID, 'id_text')
        inputbox.send_keys(Keys.ENTER)

        error = self.browser.find_element(by=By.CSS_SELECTOR, value='.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element(By.ID, 'id_new_item').send_keys("Buy milk")
        self.check_for_row_in_list_table("Buy milk")

        self.browser.find_element(By.ID, 'id_new_item').send_keys("\n")

        self.check_for_row_in_list_table("Buy milk")
        error = self.browser.find_element(By.CSS_SELECTOR, value='.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element(By.ID, 'id_new_item').send_keys("Make Tea\n")
        self.check_for_row_in_list_table("Buy milk")
        self.check_for_row_in_list_table("Make Tea")

