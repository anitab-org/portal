from common.tests.selenium.base import SeleniumTestCase


class TestAuthPages(SeleniumTestCase):
    """
    Automated visual tests for common auth operations
    """

    def test_can_login(self):
        self.browser.get('{}{}'.format(self.live_server_url, '/accounts/login/'))
        self.verify_user()
        username = self.browser.find_element_by_id("id_login")
        password = self.browser.find_element_by_id("id_password")
        username.send_keys("foo")
        password.send_keys("foobar")
        self.browser.find_element_by_id('login_button').click()
        message = self.browser.find_element_by_class_name('message-success').text
        self.assertTrue('Successfully signed in as foo.' in message)

    def test_can_signup(self):
        self.browser.get('{}{}'.format(self.live_server_url,
                                       '/accounts/signup/'))
        email = self.browser.find_element_by_id("id_email")
        username = self.browser.find_element_by_id("id_username")
        password1 = self.browser.find_element_by_id("id_password1")
        password2 = self.browser.find_element_by_id("id_password2")
        email.send_keys("foo1@systers.org")
        username.send_keys("foo1")
        password1.send_keys("FooBar_123")
        password2.send_keys("FooBar_123")
        self.browser.find_element_by_id('signup_button').click()
        message = self.browser.find_element_by_class_name('message-info').text
        self.assertTrue(
            'Confirmation e-mail sent to foo1@systers.org.' in message)

    def test_can_logout(self):
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(self.create_session_cookie())
        self.browser.refresh()
        self.browser.get('{}{}'.format(self.live_server_url, '/users/foo'))
        dropdown = self.browser.find_element_by_id('user-dropdown')
        dropdown.click()
        menu = dropdown.find_element_by_class_name('dropdown-menu')
        for menu_item in menu.find_elements_by_tag_name('li'):
            if menu_item.text == 'LOGOUT':
                menu_item.click()
                break
        self.browser.find_element_by_id('signout_button').click()
        message = self.browser.find_element_by_class_name(
            'message-success').text
        self.assertTrue('You have signed out.' in message)
