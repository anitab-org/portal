from common.tests.selenium.base import SeleniumTestCase
from selenium.webdriver.support.ui import Select


class TestUserActions(SeleniumTestCase):
    """
    Automated visual tests for user actions
    """

    def test_can_change_password(self):
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(self.create_session_cookie())
        self.browser.refresh()
        self.verify_user()
        self.browser.get('{}{}'.format(self.live_server_url, '/users/foo'))
        dropdown = self.browser.find_element_by_id('user-dropdown')
        dropdown.click()
        menu = dropdown.find_element_by_class_name('dropdown-menu')
        for menu_item in menu.find_elements_by_tag_name('li'):
            if menu_item.text == 'CHANGE PASSWORD':
                menu_item.click()
                break
        old_password = self.browser.find_element_by_id("id_oldpassword")
        password1 = self.browser.find_element_by_id("id_password1")
        password2 = self.browser.find_element_by_id("id_password2")
        old_password.send_keys("foobar")
        password1.send_keys("FooBar_123")
        password2.send_keys("FooBar_123")
        self.browser.find_element_by_id('change_pass_button').click()
        message = self.browser.find_element_by_class_name('container').text
        self.assertTrue('Password successfully changed.' in message)

    def test_can_edit_profile(self):
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(self.create_session_cookie())
        self.browser.refresh()
        self.verify_user()
        self.browser.get('{}{}'.format(self.live_server_url, '/users/foo/profile'))
        first_name = self.browser.find_element_by_id("id_first_name")
        last_name = self.browser.find_element_by_id("id_last_name")
        country = Select(self.browser.find_element_by_id("id_country"))
        blog_url = self.browser.find_element_by_id("id_blog_url")
        homepage_url = self.browser.find_element_by_id("id_homepage_url")
        first_name.send_keys("John")
        last_name.send_keys("Doe")
        country.select_by_index(1)
        blog_url.send_keys('http://blog.john-doe.com')
        homepage_url.send_keys('http://www.john-doe.com')
        self.browser.find_element_by_id('submit-id-save').click()
        title = self.browser.find_element_by_tag_name('h1').text
        self.assertTrue('John Doe' in title)
