from common.tests.selenium.base import SeleniumTestCase


class TestMeetupPage(SeleniumTestCase):
    """
    Automated visual tests for meetup entry page.
    """

    def test_can_goto_meetup_page(self):
        self.browser.get('{}{}'.format(self.live_server_url, '/meetup/foo/baz/'))
        title = self.browser.find_element_by_id('meetup-title')
        self.assertTrue(title.text == 'Test Meetup')
