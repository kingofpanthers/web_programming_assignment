from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class HashBrowserTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        cls.browser = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.browser.quit()
        finally:
            super().tearDownClass()

    def test_preview_and_save(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.ID, 'id_text').send_keys('hello')
        expected = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
        WebDriverWait(self.browser, 10).until(lambda browser: browser.find_element(By.ID, 'quickhash').text == expected)
        self.browser.find_element(By.NAME, 'submit').click()
        WebDriverWait(self.browser, 10).until(lambda browser: '/hash/' in browser.current_url)
        self.assertIn(expected, self.browser.page_source)
