---
id: tech-decisions
title: Technical Decisions
---


# Technical Decisions

### This page contains the details about the choice of tech stack and implementation methods chosen.

***
# Django 1.11 (Backend + Frontend)

Django has been been growing popularly ever since and has emerged as the first choice of any python developer who
looks forward to try one's hands on Web Development.

***At the time the project was started, back in year 2014, Django 1.11 was the latest version of django. And there has been continuous work being done on the same framework for the past 6-7 years now.***

These are a few reasons why Django is considered as an apt framework for this project.

- A web application framework is basically a toolkit of components that all web applications need. The point of this is to let developers focus on the things that are new and unique about their project instead of implementing the same solutions over and over again. Django is even more fully featured than most other frameworks, coming with everything you need to build a web app right out-of-the-box.

- Part of what makes Django so powerful is it’s ability to be extended with ‘app’ plugins. There are hundreds of these packages that make it easy to do things. For example, in this particular project we are using a number of libraries and plugins viz Django Guardian, AllAuth, CkEditor, Crispy Forms, GeoIP and a lot more are being used.

- Django, evolving as a very popular framework, has an excellent community of developers because of which easy help is available, just a google search away.


<<<<<<< HEAD
### Anyone wishing to try their hands on Django can check out the excellent documentation by checking out this [link](https://docs.djangoproject.com/en/3.0/)

## Django-AllAuth
=======
## Anyone wishing to try their hands on Django can check out the excellent documentation by checking out this [link](https://docs.djangoproject.com/en/3.0/)

# Django-AllAuth
>>>>>>> 4b4eb36... docs: Added tech decisions doc

***All the Authentication Done for the Portal is done by DJango-ALlauth which provides great abstraction over User Authentication and Social Accounts Authentication.***

The Following are the Reasons for Using Django-AllAuth

- Signup of both local and social accounts
- Connecting more than one social account to a local account
- Disconnecting a social account – requires setting a password if only the local account remains
- Optional instant-signup for social accounts – no questions asked
- E-mail address management (multiple e-mail addresses, setting a primary)
- Password forgotten flow
- E-mail address verification flow
- A huge number of Social Account Providers

<<<<<<< HEAD
#### Architecture & Design
=======
### Architecture & Design
>>>>>>> 4b4eb36... docs: Added tech decisions doc

- Pluggable signup form for asking additional questions during signup.
- Support for connecting multiple social accounts to a Django user account.
- The required consumer keys and secrets for interacting with Facebook, Twitter and the likes are to be configured in the database via the -
  Django admin using the SocialApp model.
- Consumer keys, tokens make use of the Django sites framework. This is especially helpful for larger multi-domain projects, but also allows for easy switching between a development (localhost) and production setup without messing with your settings and database.


For more info, visit the following link [Django-Allauth](https://django-allauth.readthedocs.io/en/latest/overview.html).

<<<<<<< HEAD
### Django Nose
=======
## Django Nose
>>>>>>> 4b4eb36... docs: Added tech decisions doc

***Testing proves to be an important part of any product. IN case of Portal we abide by Django-Nose For testing and Coverage.***

The Reasons for Using Django-Nose

Django-nose provides all the goodness of nose in your Django tests, like:

- Testing just your apps by default, not all the standard ones that happen to be in INSTALLED_APPS
- Running the tests in one or more specific modules (or apps, or classes, or folders, or just running a specific test)
- Obviating the need to import all your tests into tests/__init__.py. This not only saves busy-work but also eliminates the possibility of - accidentally shadowing test classes.
- Taking advantage of all the useful nose plugins

For more info visit https://django-nose.readthedocs.io/

<<<<<<< HEAD
### Flake 8

***Used to catch linting and indentation warning and errors.***

### Pinax Notification
=======
## Flake 8

***Used to catch linting and indentation warning and errors.***

## Pinax Notification
>>>>>>> 4b4eb36... docs: Added tech decisions doc

***Pinax Notification is being used in the Portal to send in-app Notifications based on different triggers or actionss.***

Features provided by Pinax Notifications

- Submission of notification messages by other apps
- Notification messages via email (configurable by user)
- Ability to supply your own backend notification channels
- Ability to scope notifications at the site level

<<<<<<< HEAD
### Django-selenium

***Web Driver Selenium tests are done using django-selenium in the Portal***

### GeoIP2
=======
## Django-selenium

***Web Driver Selenium tests are done using django-selenium in the Portal***

## GeoIP2
>>>>>>> 4b4eb36... docs: Added tech decisions doc

*** This particular Library is being used to fetch user locations from the maxmind database.***

Reasons for Using GeoIP2

- IP geolocation is inherently imprecise. Locations are often near the center of the population. Any location provided by a GeoIP2 database or web service should not be used to identify a particular address or household.
- Many of the records returned by the GeoIP web services and databases include a geoname_id field. This is the ID of a geographical feature (city, region, country, etc.) in the GeoNames database.
- Easy to fetch location details using the Url Headers.

<<<<<<< HEAD
### Crispy Forms
=======
## Crispy Forms
>>>>>>> 4b4eb36... docs: Added tech decisions doc

*** Crispy forms are used in the Portal to make the Default Django forms more intuitive and giving it a human touch. Helps provide customized form rendering in django***

For more details visit the Link : https://django-crispy-forms.readthedocs.io/en/d-0/index.html
