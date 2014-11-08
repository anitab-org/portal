from django.template import loader, Context
from django.test import TestCase
from crispy_forms.tests.forms import TestForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from common.crispy_forms.bootstrap import SubmitCancelFormActions


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
