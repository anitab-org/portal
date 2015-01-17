Systers Portal Project [![Build Status](https://travis-ci.org/systers/portal.svg?branch=master)](https://travis-ci.org/systers/portal) [![Coverage Status](https://coveralls.io/repos/systers/portal/badge.png?branch=master)](https://coveralls.io/r/systers/portal?branch=master) [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/systers/portal?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
======================

Systers Portal is for Systers communities to post and share information within and with other communities.

Our project page >> http://systers.github.io/portal/

More information on technical architecture of this project coming soon...


Setup for developers
--------------------

1. Make sure you have installed Python 2.7 or above (preferably latest minor release), 
   [pip](https://pip.pypa.io/en/latest/) and [virtualenv](http://www.virtualenv.org/en/latest/).
2. Make sure you have PostgreSQL installed.
3. Create a virtual environment and install dependencies:

 ```bash
 $ virtualenv venv
 $ source venv/bin/activate
 $ pip install -r requirements/dev.txt
 ```
4. Create `systersdb` database, where `systersdb` might be any suitable name.
5. Fill in the database details in `systers_portal/settings/dev.py`.
6. Run `export SECRET_KEY=foobarbaz` in your terminal, ideally the secret key 
  should be 40 characters long, unique and unpredictable. Optionally to set the
  shell variable every time you activate the virtualenv, edit `venv/bin/activate`
  and add to the bottom the export statement.
7. Run `python systers_portal/manage.py migrate`.
8. Run `python systers_portal/manage.py createsuperuser` to create a superuser for the admin panel.
  Fill in the details asked.
9. Run `python systers_portal/manage.py runserver` to start the development server. When in testing
  or production, feed the respective settings file from the command line, e.g. for  
  testing `python manage.py runserver --settings=systers_portal.settings.testing`
10. Before commiting run `flake8 systers_portal` and fix PEP8 warnings
11. Run `python systers_portal/manage.py test --settings=systers_portal.settings.testing`
  to run all the tests


Documentation
-------------

Documentation for Systers Portal is generated using [Sphinx](http://sphinx-doc.org/)
and available online at http://systers-portal.readthedocs.org/

To build the documentation locally run:
```bash
$ cd docs/
$ make html
```

To view the documentation open the generated `index.html` file in browser - 
`docs/_build/html/index.html`.

For more information on semantics and builds, please refer to the Sphinx
[official documentation](http://sphinx-doc.org/contents.html).

You can view the requirements document [here](docs/requirements/Systers_GSoC14_Portal_Requirements.pdf).
