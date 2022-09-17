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

    def test_0002_layout_and_styling(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)
        inputbox = self.browser.find_element(By.ID, 'id_text')
        self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2, 512, delta=10  )
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        inputbox = self.browser.find_element(By.ID, 'id_text')
        self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2, 512, delta=10  )
