from django.template import Context, Engine
from django.test import TestCase
from crispy_forms.tests.forms import SampleForm
from common.helpers import SubmitCancelFormHelper


class SubmitCancelFormHelperTestCase(TestCase):

    def test_submit_cancel_form_helper(self):
        """Test custom crispy forms layout helper"""
        template = Engine().get_default().from_string("""
            {% load crispy_forms_tags %}
            {% crispy form %}
        """)

        test_form = SampleForm()
        test_form.helper = SubmitCancelFormHelper(test_form)

        c = Context({'form': test_form})

        html = template.render(c)
        self.assertEqual(html.count('role="button"'), 1)
        self.assertEqual(html.count('href="#"'), 1)
        self.assertEqual(html.count('Cancel'), 1)
        self.assertEqual(html.count('Submit'), 1)

        test_form = SampleForm()
        test_form.helper = SubmitCancelFormHelper(test_form,
                                                  cancel_href="/some/url/")

        c = Context({'form': test_form})

        html = template.render(c)
        self.assertEqual(html.count('href="/some/url/'), 1)
