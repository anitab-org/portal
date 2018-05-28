from common.tests.selenium.base import SeleniumTestCase
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TestAdminActions(SeleniumTestCase):
    """
    Automated visual tests admin actions
    """

    def test_can_create_community(self):
        self.make_admin()
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(self.create_session_cookie())
        self.browser.refresh()
        self.browser.get('{}{}'.format(self.live_server_url, '/community/add_community/'))
        name = self.browser.find_element_by_id("id_name")
        slug = self.browser.find_element_by_id("id_slug")
        order = self.browser.find_element_by_id("id_order")
        email = self.browser.find_element_by_id("id_email")
        mailing_list = self.browser.find_element_by_id("id_mailing_list")
        parent_community = Select(
            self.browser.find_element_by_id("id_parent_community"))
        website = self.browser.find_element_by_id("id_website")
        facebook = self.browser.find_element_by_id("id_facebook")
        googleplus = self.browser.find_element_by_id("id_googleplus")
        twitter = self.browser.find_element_by_id("id_twitter")
        name.send_keys("Foo Community")
        slug.send_keys("foo-community")
        order.send_keys("5")
        email.send_keys("foo.community@systers.org")
        mailing_list.send_keys('foo.community.list@systers.org')
        parent_community.select_by_index(0)
        website.send_keys('http://www.foo-community.org')
        facebook.send_keys('http://www.facebook.com/foo-community')
        googleplus.send_keys('http://plus.google.com/foo-community')
        twitter.send_keys('http://www.twitter.com/foo-community')
        self.browser.find_element_by_id('submit-id-save').click()
        # Wait required on this page. Tests will fail without
        # wait even after successful completion of required actions.
        wait = WebDriverWait(self.browser, 10)
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(),'Foo Community')]")))
        self.assertTrue('Foo Community' in self.browser.title)

    def test_can_create_meetup(self):
        self.make_admin()
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(self.create_session_cookie())
        self.browser.refresh()
        self.browser.get('{}{}'.format(self.live_server_url, '/meetup/add/'))
        name = self.browser.find_element_by_id("id_name")
        slug = self.browser.find_element_by_id("id_slug")
        location = Select(self.browser.find_element_by_id("id_location"))
        email = self.browser.find_element_by_id("id_email")
        name.send_keys("Foo Community")
        slug.send_keys("foo-community")
        email.send_keys("foo.community@systers.org")
        location.select_by_index(1)
        # Locate the CKE iframe for description
        description = self.browser.find_element_by_xpath(
            "//div[contains(@id, 'cke_1_contents')]/iframe")
        self.browser.switch_to.frame(description)  # switch context to iframe
        description_editor = self.browser.find_element_by_xpath("//body")
        description_editor.send_keys("Foo description")
        self.browser.switch_to_default_content()  # return to main context
        # Locate the CKE iframe for sponsors
        sponsors = self.browser.find_element_by_xpath(
            "//div[contains(@id, 'cke_2_contents')]/iframe")
        self.browser.switch_to.frame(sponsors)
        sponsors_editor = self.browser.find_element_by_xpath("//body")
        sponsors_editor.send_keys("Foo sponsor")
        self.browser.switch_to_default_content()
        self.browser.find_element_by_id('submit-id-save').click()
        message = self.browser.find_element_by_class_name('container').text
        self.assertTrue('Meetup added Successfully' in message)
