from common.tests.selenium.base import SeleniumTestCase
from community.models import Community, RequestCommunity


class TestCommunityAdminActions(SeleniumTestCase):
    """
    Automated tests for admin actions in community app
    """

    def setUp(self):
        super().setUp()
        self.make_admin()
        self.community = Community.objects.create(
            name="Foo Community", slug="foo-community",
            order=1, admin=self.systers_user)
        self.request_community = RequestCommunity.objects.create(
            name="Foo", slug="foo",
            order=2, is_member='Yes', type_community='Other',
            community_channel='Existing Social Media Channels ',
            is_avail_volunteer='Yes', count_avail_volunteer=0,
            user=self.systers_user)

    def test_can_view_requests(self):
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(self.create_session_cookie())
        self.browser.refresh()
        self.browser.get('{}{}'.format(self.live_server_url,
                                       '/community/community_requests'))
        title = self.browser.find_element_by_xpath(
            "//h2[contains(text(), 'Unapproved Community Requests')]").text
        self.assertTrue('Unapproved Community Requests' == title)

    def test_can_accept_requests(self):
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(self.create_session_cookie())
        self.browser.refresh()
        self.browser.get('{}{}'.format(self.live_server_url,
                                       '/community/foo/view_request/'))
        self.browser.find_element_by_xpath(
            "//a[contains(text(),'Approve')]").click()
        message = self.browser.find_element_by_class_name('container').text
        self.assertTrue('Community created successfully!' == message)

    def test_can_reject_requests(self):
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(self.create_session_cookie())
        self.browser.refresh()
        self.browser.get('{}{}'.format(self.live_server_url,
                                       '/community/foo/view_request/'))
        self.browser.find_element_by_xpath(
            "//a[contains(text(),'Reject')]").click()
        self.browser.find_element_by_class_name("btn-danger").click()
        message = self.browser.find_element_by_class_name('container').text
        self.assertTrue('Community request successfullly rejected!' == message)
