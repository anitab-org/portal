---
id: test-the-app
title: How to Test The Application
---

### The website is served live on [this link](http://ec2-54-215-223-241.us-west-1.compute.amazonaws.com/)

***

### To run test cases on the app, run the following command after you setup the portal locally.

```shell
python systers_portal/manage.py runserver --settings=systers_portal.settings.testing
```
### To check for the PEP8 style guide errors, run the following command

```shell
flake8 systers_portal
```
