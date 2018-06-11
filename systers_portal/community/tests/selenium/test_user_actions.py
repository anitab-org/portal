from common.tests.selenium.base import SeleniumTestCase
from selenium.webdriver.support.ui import Select


class TestUserActions(SeleniumTestCase):
    """
    Automated visual tests for logged in user actions on community app.
    """

    def test_can_request_community(self):
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(self.create_session_cookie())
        self.browser.refresh()
        self.browser.get('{}{}'.format(self.live_server_url, '/community/request_community/'))
        is_a_member = Select(self.browser.find_element_by_id("id_is_member"))
        email_id = self.browser.find_element_by_id("id_email_id")
        name = self.browser.find_element_by_id("id_name")
        slug = self.browser.find_element_by_id("id_slug")
        email = self.browser.find_element_by_id("id_email")
        order = self.browser.find_element_by_id("id_order")
        community_type = Select(self.browser.find_element_by_id("id_type_community"))
        parent_community = Select(self.browser.find_element_by_id("id_parent_community"))
        community_channel = Select(self.browser.find_element_by_id("id_community_channel"))
        mailing_list = self.browser.find_element_by_id("id_mailing_list")
        website = self.browser.find_element_by_id("id_website")
        facebook = self.browser.find_element_by_id("id_facebook")
        googleplus = self.browser.find_element_by_id("id_googleplus")
        twitter = self.browser.find_element_by_id("id_twitter")
        demographic_target = self.browser.find_element_by_id("id_demographic_target_count")
        purpose = self.browser.find_element_by_id("id_purpose")
        available_volunteers = Select(self.browser.find_element_by_id("id_is_avail_volunteer"))
        no_available_volunteers = self.browser.find_element_by_id("id_count_avail_volunteer")
        content = self.browser.find_element_by_id("id_content_developer")
        selection_criteria = self.browser.find_element_by_id("id_selection_criteria")
        real_time = self.browser.find_element_by_id("id_is_real_time")
        is_a_member.select_by_index(1)
        email_id.send_keys("foo-maker@gmail.com")
        name.send_keys("Foo Community Request")
        slug.send_keys("foo-community-request")
        email.send_keys("foo.community@systers.org")
        order.send_keys("5")
        community_type.select_by_index(1)
        parent_community.select_by_index(0)
        community_channel.select_by_index(1)
        mailing_list.send_keys("list@foo-community.org")
        website.send_keys('http://www.foo-community.org')
        facebook.send_keys('http://www.facebook.com/foo-community')
        googleplus.send_keys('http://plus.google.com/foo-community')
        twitter.send_keys('http://www.twitter.com/foo-community')
        demographic_target.send_keys("Demographic target information")
        purpose.send_keys("Some purpose")
        available_volunteers.select_by_index(1)
        no_available_volunteers.send_keys("25")
        content.send_keys("Some content")
        selection_criteria.send_keys("Some selection criteria used")
        real_time.send_keys("Its real time")
        self.browser.find_element_by_id('submit-id-save').click()
        title = self.browser.find_element_by_xpath(
            "//h2[contains(text(), 'Foo Community Request')]").text
        self.assertTrue(title == 'Foo Community Request')
