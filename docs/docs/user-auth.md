---
id: user-auth
title: User Authentication
---

# User Authentication

## Standard User Model

***What is it?***

Fundamentally, the concept of a user account exists for two reasons: access control and personalized application state. Access control is the idea that resources on a system are only available to some users. Personalized state is heavily dependent on the purpose of the application but may include settings, data, or any other records specific to an individual user. The Django stock User model provides sensible approaches to both use cases.

***Features***

There are two types of users in a Django application: superuser accounts and regular users. Superusers have every attribute and privilege of regular accounts, but also have access to the Django admin panel. Essentially, superusers can create, edit, or delete any data in the application, including other user accounts.

## How is it done in the Backend of Django?

* Django includes substantial password management middleware with the user model
* User passwords are required to be at least 8 characters, not entirely numbers, not match too closely to the username, and not be on a list of the 20,000 most common passwords.
* When a password is sent to the server, it is encrypted before it is stored, by default using the PBKDF2 algorithm with a SHA256 hash.

***Imp***

If you want to effectively delete a user without removing those attached objects, set the user’s is_active field to false instead, or else the data tied to that user would also be deleted.

## The Django-allauth

Django-allauth provides the abstraction which saves us from building things from scratch.

***These are the following features provided by the library which are being used currently in the Project***

- Signup of both local and social accounts
- Connecting more than one social account to a local account
- Disconnecting a social account – requires setting a password if only the local account remains
- Optional instant-signup for social accounts – no questions asked
- E-mail address management (multiple e-mail addresses, setting a primary)
- Password forgotten flow
- E-mail address verification flow

When the Project is locally run, the emails are printed in the console because of the following command

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Other Security Features

SECRET_KEY is needed to be exported for the system to run locally

```shell
export SECRET_KEY==foobarbazz
```
