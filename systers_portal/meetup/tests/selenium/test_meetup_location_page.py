from common.tests.selenium.base import SeleniumTestCase


class TestMeetupLocationPage(SeleniumTestCase):
    """
    Automated visual tests for meetup location page.
    """

    def test_can_choose_location(self):
        self.browser.get('{}{}'.format(self.live_server_url, '/meetup/locations/'))
        self.browser.find_element_by_xpath("//a[contains(text(),'Foo Systers')]").click()
        self.assertTrue('Foo Systers' in self.browser.title)

    def test_can_get_members(self):
        self.browser.get('{}{}'.format(self.live_server_url, '/meetup/foo/about'))
        self.browser.find_element_by_xpath("//a[contains(text(),'Members')]").click()
        text = self.browser.find_element_by_xpath("//h2[contains(text(),'Moderators')]").text
        self.assertTrue(text in self.browser.page_source)
