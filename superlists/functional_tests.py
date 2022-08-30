from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import unittest
import pytest

class NewVistorTest(unittest.TestCase):
    def setUp(self):
        service = Service('d://chromedriver')
        option = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=service, options=option)
        self.browser = self.driver
        self.url = "http://127.0.0.1:8000/"

    def tearDown(self):
        self.driver.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.driver.get(self.url)

        assert "To-Do" in self.browser.title
        #pytest.fail('finish the test')

if __name__ == '__main__':
    unittest.main(warnings='ignore')