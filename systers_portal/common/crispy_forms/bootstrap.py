from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import LayoutObject, Submit, HTML


class SubmitCancelFormActions(LayoutObject):
    """Custom bootstrap layout object. It wraps a Cancel anchor tag and a Submit
    input field in a <div class="form-actions">.

    Example::

        SubmitCancelFormActions(cancel_href="/some/url/")
    """
    def __init__(self, *fields, **kwargs):
        self.cancel_href = kwargs.pop('cancel_href', '#')

    def render(self, form, form_style, context):
        layout_object = FormActions(
            HTML("""<a role="button" class="btn btn-default mr4" href="{0}">
                    Cancel</a>""".format(self.cancel_href)),
            Submit('save', 'Submit'),
        )
        return layout_object.render(form, form_style, context)
