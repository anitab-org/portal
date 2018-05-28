from common.tests.selenium.base import SeleniumTestCase


class TestMeetupLocationAdminPage(SeleniumTestCase):

    def test_can_add_new_meetup(self):
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(self.create_session_cookie())
        self.browser.refresh()
        self.browser.get('{}{}'.format(self.live_server_url, '/meetup/add'))
        self.assertTrue(True)

    def test_can_delete_meetup(self):
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(self.create_session_cookie())
        self.browser.refresh()
        self.browser.get('{}{}'.format(self.live_server_url, '/meetup/foo/about'))
        self.browser.find_element_by_xpath("//a[contains(text(),'Delete Meetup Location')]").click()
        self.browser.find_element_by_xpath('//input[@value="Confirm"]').click()
        self.assertTrue('Meetup Locations' in self.browser.title)
