# coding=utf-8

"""."""

import unittest
import time

from django.test import tag

from selenium import webdriver
from selenium.webdriver.support.ui import Select


unittest.TestLoader.sortTestMethodsUsing = None


@tag('functional')
class NewVisitorTest(unittest.TestCase):
    """."""

    def setUp(self):
        """Setup."""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """Teardown."""
        self.browser.quit()

    def test_django_sponsoring_title(self):
        """Test the title in the dj-sponsoring."""
        self.browser.get('http://localhost:8000/sponsors')
        self.assertIn('dj-sponsoring', self.browser.title)

    def test_no_sponsor_in_sponsor_list(self):
        """."""
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000/sponsors')

        # She notices the page title and header mention to-do lists
        self.assertIn("No sponsors", self.browser.page_source)

    def test_create_sponsor(self):
        """."""
        self.browser.get('http://localhost:8000/sponsors/create')

        print(self.browser.page_source)
        select = Select(self.browser.find_element_by_id('id_name'))
        select.send_keys("Any sponsor")

        time.sleep(2)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
