from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from crispy_forms.helper import FormHelper

from common.forms import ModelFormWithHelper
from common.helpers import SubmitCancelFormHelper


class ModelFormWithHelperTestCase(TestCase):
    def test_model_form_without_helper(self):
        """Test the custom model form without a helper class"""
        class FooForm(ModelFormWithHelper):
            class Meta:
                model = User
                fields = "__all__"

        self.assertRaises(ImproperlyConfigured, FooForm, {})

    def test_model_form_with_helper(self):
        """Test the custom model form with a helper class present"""
        class FooForm(ModelFormWithHelper):
            class Meta:
                model = User
                fields = "__all__"
                helper_class = FormHelper

        form = FooForm()
        self.assertEqual(form.helper.__class__, FormHelper)

        class BarForm(ModelFormWithHelper):
            class Meta:
                model = User
                fields = "__all__"
                helper_class = SubmitCancelFormHelper
                helper_cancel_href = "some/url/"

        form = BarForm()
        self.assertEqual(form.helper.__class__, SubmitCancelFormHelper)
