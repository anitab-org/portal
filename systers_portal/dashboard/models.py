from django.db import models
from django.contrib.auth.models import User
from datetime import date
class Community(models.Model):
	community_name = models.CharField(max_length=255, blank=False, null=False)
	address=models.CharField(max_length=255,blank=False,null=False)
	mailing_list=models.CharField(max_length=255,blank=True,null=True)
	resource_area=models.URLField(max_length=255,blank=True,null=True)
	admin = models.ForeignKey(User)
	website = models.URLField(max_length=255,blank=True,null=True)
	facebook = models.URLField(max_length=255,blank=True,null=True)
	googleplus = models.URLField(max_length=255,blank=True,null=True)
	twitter =  models.URLField(max_length=255,blank=True,null=True)

	def __unicode__(self):
		return self.community_name

class User(models.Model):
	auth_user = models.OneToOneField(User)
	communities = models.ManyToManyField(Community, blank=True,null=True)
	image = models.ImageField(upload_to='photos/',default='photos/duumy.png',blank=True,null=True)
	def __unicode__(self):
		firstname = self.auth_user.first_name
		lastname = self.auth_user.last_name
		if firstname and lastname:
			return "{0} {1}".format(self.auth_user.first_name, self.auth_user.last_name)
		else:
			return self.auth_user.username

class Resource(models.Model):
	RESOURCE_TYPES = ( 
			('FAQ', 'Frequently Asked Questions'),
			('About', 'About'),
			('News', 'News'),
			('Join', 'Join'),
			('Resources', (
				       ('scholarship', 'Scholarship'),
				       ('grant', 'Grant'),
				       ('internship', 'Internship'),
				       ('workshop', 'Workshop'),
				       ('development', 'Professional Development'),
				      )
			),
			('GraceHopper', 'GraceHopper'),
			)

	title = models.CharField(max_length=255, blank=False, null=False)
	community = models.ForeignKey(Community)
	author = models.ForeignKey(User)
	date_created = models.DateField(auto_now=False, auto_now_add=True)
	date_modified = models.DateField(auto_now=True, auto_now_add=False)
	contents = models.TextField()
	resource_type =  models.CharField(max_length=30, choices=RESOURCE_TYPES)
	def __unicode__(self):
		return self.title
