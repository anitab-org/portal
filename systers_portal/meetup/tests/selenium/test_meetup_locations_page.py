from common.tests.selenium.base import SeleniumTestCase


class TestMeetupLocationsPage(SeleniumTestCase):
    """
    Automated visual tests for meetup locations page.
    """

    def test_can_goto_meetuplocations_page(self):
        self.browser.get('{}{}'.format(self.live_server_url, '/meetup/locations/'))
        self.assertTrue('Meetup Locations' in self.browser.title)

    def test_can_choose_meetup_locations(self):
        self.browser.get(self.live_server_url)
        dropdown = self.browser.find_element_by_id('meetup-dropdown')
        dropdown.click()
        menu = dropdown.find_element_by_class_name('dropdown-menu')
        for menu_item in menu.find_elements_by_tag_name('li'):
            if menu_item.text == 'MEETUP LOCATIONS':
                menu_item.click()
                break
        self.assertTrue('Meetup Locations' in self.browser.title)

    def test_can_choose_location(self):
        self.browser.get('{}{}'.format(self.live_server_url, '/meetup/locations/'))
        self.browser.find_element_by_xpath("//a[contains(text(),'Foo Systers')]").click()
        self.assertTrue('Foo Systers' in self.browser.title)
