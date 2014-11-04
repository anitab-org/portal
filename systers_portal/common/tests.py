from django.core.urlresolvers import reverse
from django.template import loader, Context
from django.test import TestCase, Client
from crispy_forms.tests.forms import TestForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from common.forms.bootstrap import SubmitCancelFormActions


class CommonViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        """Test index/landing page"""
        index_url = reverse('index')
        response = self.client.get(index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/index.html')


class FormLayoutObjectsTestCase(TestCase):
    def test_submit_cancel_form_actions(self):
        """Test custom SubmitCancelFormActions bootstrap layout object"""
        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form %}
        """)

        test_form = TestForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            SubmitCancelFormActions()
        )

        c = Context({'form': test_form})

        html = template.render(c)
        self.assertEqual(html.count('class="form-actions'), 1)
        self.assertEqual(html.count('role="button"'), 1)
        self.assertEqual(html.count('href="#"'), 1)
        self.assertEqual(html.count('Cancel'), 1)
        self.assertEqual(html.count('Submit'), 1)

        test_form.helper.layout = Layout(
            SubmitCancelFormActions(cancel_href="/some/url/")
        )
        c = Context({'form': test_form})

        html = template.render(c)
        self.assertEqual(html.count('href="/some/url/'), 1)
