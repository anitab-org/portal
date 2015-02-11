from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, HTML


class SubmitCancelFormHelper(FormHelper):
    """Custom FormHelper that appends to the layout cancel and submit
    buttons (works only with bootstrap crispy-forms pack). It expects a
    `cancel_href` attribute to be used as cancel button URL.

    Example::

        SubmitCancelFormHelper(self, cancel_href="/some/url/")
    """
    def __init__(self, *args, **kwargs):
        cancel_href = kwargs.pop('cancel_href', '#')
        super(SubmitCancelFormHelper, self).__init__(*args, **kwargs)
        self.layout.append(
            Layout(
                FormActions(
                    HTML("""<a role="button" class="btn btn-default mr4"
                            href="{0}">Cancel</a>""".format(cancel_href)),
                    Submit('save', 'Submit'),
                )
            )
        )
