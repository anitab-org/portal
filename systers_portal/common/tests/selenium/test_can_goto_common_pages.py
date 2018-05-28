from common.tests.selenium.base import SeleniumTestCase


class TestCanGoToCommonPages(SeleniumTestCase):
    """
    Automated visual tests to visit common pages
    """

    def test_can_goto_home_page(self):
        self.browser.get(self.live_server_url)
        welcome = self.browser.find_element_by_tag_name('h1').text
        self.assertTrue(welcome == 'Welcome to Systers Portal!')

    def test_can_goto_about_page(self):
        self.browser.get('{}{}'.format(self.live_server_url, '/about-us'))
        about = self.browser.find_element_by_tag_name('h1').text
        self.assertTrue(about == 'About Systers')

    def test_can_goto_contact_page(self):
        self.browser.get('{}{}'.format(self.live_server_url, '/contact'))
        contact = self.browser.find_element_by_tag_name('h1').text
        self.assertTrue(contact == 'Contact Systers')

    def test_can_goto_login_page(self):
        self.browser.get('{}{}'.format(self.live_server_url, '/accounts/login/'))
        self.assertTrue('Sign In' in self.browser.title)

    def test_can_goto_signup_page(self):
        self.browser.get('{}{}'.format(self.live_server_url, '/accounts/signup/'))
        self.assertTrue('Sign Up' in self.browser.title)
