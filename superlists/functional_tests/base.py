import sys
import time
import os
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import pytest

import django

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superlists.settings")
#django.setup()
from lists.models import Item

class FunctionalTest(StaticLiveServerTestCase):


    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = f'http://{arg.split("=")[1]}'
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url


    @classmethod
    def tearDownClass(cls):
        if cls.server_url  == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        service = Service('d://chromedriver')
        option = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(service=service, options=option)
        # self. = self.driver
        # self.url = self.live_server_url

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, content):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        assert any([content in row.text for row in rows])

