Systers Portal [![Build Status](https://travis-ci.org/systers/portal.svg?branch=master)](https://travis-ci.org/systers/portal) [![Coverage Status](https://coveralls.io/repos/systers/portal/badge.png?branch=master)](https://coveralls.io/r/systers/portal?branch=master)
==============

Systers Portal is for Systers communities to post and share information within
and with other communities.

Website: http://portal.systers.org

Project page: http://systers.github.io/portal/


Setup for developers
--------------------

1. Make sure you have installed Python 3.4 (preferably latest minor release),
   [pip](https://pip.pypa.io/en/latest/) and [virtualenv](http://www.virtualenv.org/en/latest/).
1. Make sure you have PostgreSQL installed. For a tutorial on installing
   Postgres, [Django Girls'](http://djangogirls.org) ebook,
   [Tutorials Extension](http://djangogirls.org/resources/), is a reference.
   The info is also on [Django Girls GitHub repository](https://github.com/DjangoGirls/tutorial-extensions/blob/master/optional_postgresql_installation/README.md).
1. Make sure you have python3-dev installed - `sudo pip install python3-dev`
1. Clone the repo - `git clone git@github.com:systers/portal.git` and cd into
  the `portal` directory.
1. Create a virtual environment with Python 3 and install dependencies:

 ```bash
 $ virtualenv venv --python=/path/to/python3
 $ source venv/bin/activate
 $ pip install -r requirements/dev.txt
 ```
1. Create `systersdb` database, where `systersdb` might be any suitable name.
1. Fill in the database details in `systers_portal/settings/dev.py`.
1. Run `export SECRET_KEY=foobarbaz` in your terminal, ideally the secret key
  should be 40 characters long, unique and unpredictable. Optionally to set the
  shell variable every time you activate the virtualenv, edit `venv/bin/activate`
  and add to the bottom the export statement.
1. Run `python systers_portal/manage.py migrate`.
1. Run `python systers_portal/manage.py createsuperuser` to create a superuser for the admin panel.
  Fill in the details asked.
1. Run `python systers_portal/manage.py runserver` to start the development server. When in testing
  or production, feed the respective settings file from the command line, e.g. for
  testing `python systers_portal/manage.py runserver --settings=systers_portal.settings.testing`.
1. Before commiting run `flake8 systers_portal` and fix PEP8 warnings.
1. Run `python systers_portal/manage.py test --settings=systers_portal.settings.testing`
  to run all the tests.



Run Portal in a Docker container
--------------------------------

If you wish to view a speak peek of the Systers Portal, you may use Docker to
preview the Portal.
Note: The following Docker configuration is not intended to be run in
production at the moment. It may be configured to do so in the future.

1. Install [Docker](https://docs.docker.com/installation/).
   Follow the installation steps for your specific operating system:
     * Docker runs natively on a Linux-based system.
     * For Windows and Mac OS X, you should follow instructions for installing
       boot2docker which also installs VirtualBox.
1. Install [docker-compose](http://docs.docker.com/compose/install/).
   Note: fig has been deprecated. Docker-compose replaces fig.
1. Create a new directory on your local system.
1. Enter `git clone git@github.com:systers/portal.git` to clone the Systers
   Portal repository. After the clone is done, change directory (cd) to the
   `portal` directory.
1. Run `docker-compose build`. This pulls the Docker images required to run the
   project and installs the necessary dependencies.
1. **This step will require the Django SECRET_KEY.**
   Run `docker run -e SECRET_KEY=foobarbaz portal_web`.
1. Run `docker-compose run web python systers_portal/manage.py migrate`.
1. *Optional:*
   Run `docker-compose run web python systers_portal/manage.py createsuperuser`
   if you wish to create a superuser to access the admin panel.
1. Run `docker-compose up` to start the webserver for the Django Systers Portal
   project.
1. Systers Portal should be running on port 8000.
     * If you are on Linux, enter `http://0.0.0.0:8000` in your browser.
     * If you are using boot2docker on Windows or Mac OS X, enter
       `http://192.168.59.103:8000/` in your browser. If this IP address
       doesn't work, run `boot2docker ip` from the command line and replace
       the previous IP address in the HTTP request with the IP returned by
       boot2docker.


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
