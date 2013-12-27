from django.test import LiveServerTestCase
from selenium import webdriver

class AdminFuncTests(LiveServerTestCase):
  fixtures = ['functest_users.json'] 
  
  def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    self.browser.quit()

  def test_admin_site_up(self):
    self.browser.get(self.live_server_url + '/admin/')
    body = self.browser.find_element_by_tag_name('body')
    self.assertIn('Django administration', body.text)