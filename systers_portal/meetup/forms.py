from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from common.forms import ModelFormWithHelper
from common.helpers import SubmitCancelFormHelper
from meetup.models import Meetup, MeetupLocation, Rsvp
from users.models import SystersUser
from common.models import Comment


class AddMeetupForm(ModelFormWithHelper):
    """Form to create new Meetup. The created_by and the meetup_location of which meetup belong to
    are expected to be provided when initializing the form:

    * created_by - currently logged in user
    * meetup_location - to which Meetup belongs
    """
    class Meta:
        model = Meetup
        fields = ('title', 'slug', 'date', 'time', 'venue', 'description')
        widgets = {'date': forms.DateInput(attrs={'type': 'text', 'class': 'datepicker'}),
                   'time': forms.TimeInput(attrs={'type': 'text', 'class': 'timepicker'})}
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'about_meetup_location' meetup_location.slug %}"

    def __init__(self, *args, **kwargs):
        self.created_by = kwargs.pop('created_by')
        self.meetup_location = kwargs.pop('meetup_location')
        super(AddMeetupForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """Override save to add created_by and meetup_location to the instance"""
        instance = super(AddMeetupForm, self).save(commit=False)
        instance.created_by = SystersUser.objects.get(user=self.created_by)
        instance.meetup_location = self.meetup_location
        if commit:
            instance.save()
        return instance

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now().date():
            raise forms.ValidationError("Date should not be before today's date.")
        return date

    def clean_time(self):
        time = self.cleaned_data.get('time')
        date = self.cleaned_data.get('date')
        if time:
            if date == timezone.now().date() and time < timezone.now().time():
                raise forms.ValidationError("Time should not be a time that has already passed.")
        return time


class EditMeetupForm(ModelFormWithHelper):
    """Form to edit Meetup"""
    class Meta:
        model = Meetup
        fields = ('title', 'slug', 'date', 'time', 'description', 'venue')
        widgets = {'date': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
                   'time': forms.TimeInput(attrs={'type': 'time', 'class': 'timepicker'})}
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_meetup' meetup_location.slug meetup.slug %}"


class AddMeetupLocationMemberForm(ModelFormWithHelper):
    """Form for adding a new member to a meetup location"""
    class Meta:
        model = User
        fields = ('username',)
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'members_meetup_location' meetup_location.slug %}"

    def __init__(self, *args, **kwargs):
        super(AddMeetupLocationMemberForm, self).__init__(*args, **kwargs)
        self.meetup_location = kwargs.get('instance')
        if self.is_bound:
            self.username = kwargs['data']['username']

    def save(self, commit=True):
        """Override save to map input username to User and append it to the meetup location."""
        instance = super(AddMeetupLocationMemberForm, self).save(commit=False)
        instance.username = self.username
        user = get_object_or_404(User, username=instance.username)
        systersuser = get_object_or_404(SystersUser, user=user)
        if systersuser not in self.meetup_location.members.all():
            self.meetup_location.members.add(systersuser)
        if commit:
            instance.save()
        return instance

    def clean(self):
        """Ensure only the username of an existing systers user is given"""
        cleaned_data = super(AddMeetupLocationMemberForm, self).clean()
        username = cleaned_data.get('username')

        if len(User.objects.filter(username=username)) != 1:
            raise forms.ValidationError("Enter username of an existing user")


class AddMeetupLocationForm(ModelFormWithHelper):
    """Form to create new Meetup Location"""
    class Meta:
        model = MeetupLocation
        fields = ('name', 'slug', 'location', 'description', 'email', 'sponsors')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'list_meetup_location' %}"


class EditMeetupLocationForm(ModelFormWithHelper):
    """Form to edit Meetup Location"""
    class Meta:
        model = MeetupLocation
        fields = ('name', 'slug', 'location', 'description', 'email', 'sponsors')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'about_meetup_location' meetup_location.slug %}"


class RsvpForm(ModelFormWithHelper):
    """Form to add RSVP"""
    class Meta:
        model = Rsvp
        fields = ('coming', 'plus_one')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_meetup' meetup_location.slug meetup.slug %}"

    def __init__(self, *args, **kwargs):
        self.user = kwargs['data'].pop('user')
        self.meetup = kwargs['data'].pop('meetup')
        super(RsvpForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """Override save to add user and meetup to the instance"""
        instance = super(RsvpForm, self).save(commit=False)
        instance.user = SystersUser.objects.get(user=self.user)
        instance.meetup = self.meetup
        if commit:
            instance.save()
        return instance


class AddMeetupCommentForm(ModelFormWithHelper):
    """Form to add a comment to a Meetup"""
    class Meta:
        model = Comment
        fields = ('body',)
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_meetup' meetup_location.slug meetup.slug %}"

    def __init__(self, *args, **kwargs):
        self.content_object = kwargs.pop('content_object')
        self.author = kwargs.pop('author')
        super(AddMeetupCommentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """Override save to add content_object and author to the instance"""
        instance = super(AddMeetupCommentForm, self).save(commit=False)
        instance.content_object = self.content_object
        instance.author = SystersUser.objects.get(user=self.author)
        if commit:
            instance.save()
        return instance


class EditMeetupCommentForm(ModelFormWithHelper):
    """Form to edit a comment for a Meetup"""
    class Meta:
        model = Comment
        fields = ('body',)
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_meetup' meetup_location.slug meetup.slug %}"
