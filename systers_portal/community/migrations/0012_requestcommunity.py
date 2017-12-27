# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0003_auto_20160207_1550'),
        ('community', '0011_auto_20150522_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestCommunity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='Proposed Community Name', max_length=255)),
                ('slug', models.SlugField(verbose_name='Slug', unique=True, max_length=150)),
                ('order', models.PositiveIntegerField(verbose_name='Order', null=True, blank=True)),
                ('email', models.EmailField(verbose_name=' At what email address would you like to be contacted?', max_length=255, blank=True)),
                ('mailing_list', models.EmailField(verbose_name='Mailing list of the community', max_length=255, blank=True)),
                ('website', models.URLField(verbose_name='Link to the website', max_length=255, blank=True)),
                ('facebook', models.URLField(verbose_name='Link to the community on Facebook', max_length=255, blank=True)),
                ('googleplus', models.URLField(verbose_name='Link to the community on Google+', max_length=255, blank=True)),
                ('twitter', models.URLField(verbose_name='Link to the community on Twitter', max_length=255, blank=True)),
                ('is_member', models.CharField(verbose_name='Are you a member of Systers?', max_length=25, default=None, choices=[('Yes', 'Yes'), ('No', 'No')])),
                ('email_id', models.EmailField(verbose_name='What email have you used to sign up for Systers?', max_length=255, blank=True)),
                ('type_community', models.CharField(verbose_name='Type of Community', max_length=255, default=None, choices=[('Affinity Group', 'Affinity Group (Latinas in Computing, LGBT, etc'), ('Special Interest Group', 'Special Interest Group (Student Researchers, Systers in Government,Women in Cyber Security, etc) '), ('Email list', 'Email list (using Mailman3)'), ('Other', 'Other')])),
                ('other_community_type', models.CharField(verbose_name='Other type of community(Please specify)', max_length=255, blank=True)),
                ('community_channel', models.CharField(verbose_name='Online Community Channels', max_length=255, default=None, choices=[('Existing Social Media Channels ', 'Existing Social Media Channels '), ('Request New Social Media Channels ', 'Request New Social Media Channels ')])),
                ('social_presence', models.CharField(verbose_name='Check off all the social media accounts you can manage                                    for your proposed community:', null=True, max_length=255)),
                ('other_account', models.CharField(verbose_name='Other social channel(Please specify)', max_length=25, blank=True)),
                ('demographic_target_count', models.TextField(verbose_name='Who will it serve (                                                explain target demographics and number of people):', blank=True)),
                ('purpose', models.TextField(verbose_name='Explain the purpose and                               need for this group or account:', blank=True)),
                ('is_avail_volunteer', models.CharField(verbose_name='Do you have volunteers committed?', max_length=25, default=None, choices=[('Yes', 'Yes'), ('No', 'No')])),
                ('count_avail_volunteer', models.PositiveIntegerField(verbose_name='If yes, how many?', default=0)),
                ('content_developer', models.TextField(verbose_name='Explain the content of this group.                                         What service will this group provide (example: discussion,                                         linksharing, support)? Who will develop the content? What                                         kind of content will be shared in the group? How often                                         will moderators post/engage with users?', blank=True)),
                ('selection_criteria', models.TextField(verbose_name='Will there be screening of new members of will this group be open to anyone?         If there will be screening,what will the criteria for membership be?', blank=True)),
                ('is_real_time', models.TextField(verbose_name=' Will there be real-time meetings in addition to an online community?         (Example, at the Grace Hopper Celebration; regional meetings; etc)', blank=True)),
                ('is_approved', models.BooleanField(verbose_name='Approved', default=False)),
                ('date_created', models.DateTimeField(verbose_name='Date created', auto_now_add=True)),
                ('approved_by', models.ForeignKey(null=True, verbose_name='Approved by', to='users.SystersUser', blank=True)),
                ('parent_community', models.ForeignKey(null=True, verbose_name='Parent community', to='community.Community', blank=True)),
                ('user', models.ForeignKey(related_name='requestor', verbose_name='Created by', to='users.SystersUser')),
            ],
            options={
                'verbose_name_plural': 'Community requests',
                'permissions': (('view_community_request', 'View the community request'), ('edit_community_request', 'Edit the community request')),
            },
            bases=(models.Model,),
        ),
    ]
