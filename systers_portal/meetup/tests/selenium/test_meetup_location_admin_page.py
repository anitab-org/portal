from common.tests.selenium.base import SeleniumTestCase


class TestMeetupLocationAdminPage(SeleniumTestCase):
    """
    Extended automated visual tests for admin actions in meetup app,
    test_can_create_meetup removed as its covered in test_admin_actions under common tests.
    """

    def test_can_delete_meetup(self):
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(self.create_session_cookie())
        self.browser.refresh()
        self.browser.get('{}{}'.format(self.live_server_url, '/meetup/foo/about'))
        self.browser.find_element_by_xpath("//a[contains(text(),'Delete Meetup Location')]").click()
        self.browser.find_element_by_xpath('//input[@value="Confirm"]').click()
        self.assertTrue('Meetup Locations' in self.browser.title)
