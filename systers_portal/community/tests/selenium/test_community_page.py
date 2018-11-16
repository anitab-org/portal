from common.tests.selenium.base import SeleniumTestCase
from community.models import Community


class TestCommunityPage(SeleniumTestCase):
    """
    Automated visual tests for user actions on community page
    """

    def setUp(self):
        super().setUp()
        self.community = Community.objects.create(
            name="Foo Community",
            slug="foo-community",
            order=1,
            admin=self.systers_user)

    def test_can_goto_community_page(self):
        self.browser.get('{}{}'.format(self.live_server_url,
                                       '/community/foo-community'))
        title = self.browser.find_element_by_xpath(
            "//h1[contains(text(),'Foo Community')]").text
        self.assertTrue('Foo Community' == title)

    def test_can_click_request_community(self):
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(self.create_session_cookie())
        self.browser.refresh()
        self.browser.get(self.live_server_url)
        dropdown = self.browser.find_element_by_id('community-dropdown')
        dropdown.click()
        menu = dropdown.find_element_by_class_name('dropdown-menu')
        for menu_item in menu.find_elements_by_tag_name('li'):
            if menu_item.text == 'REQUEST A NEW COMMUNITY':
                menu_item.click()
                break
        self.assertTrue('Request a new Community' in self.browser.title)
