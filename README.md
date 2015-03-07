Systers Portal [![Build Status](https://travis-ci.org/systers/portal.svg?branch=master)](https://travis-ci.org/systers/portal) [![Coverage Status](https://coveralls.io/repos/systers/portal/badge.png?branch=master)](https://coveralls.io/r/systers/portal?branch=master) [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/systers/portal?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
==============

Systers Portal is for Systers communities to post and share information within
and with other communities.

Website: http://portal.systers.org

Project page: http://systers.github.io/portal/


Setup for developers
--------------------

1. Make sure you have installed Python 3.4 (preferably latest minor release),
   [pip](https://pip.pypa.io/en/latest/) and [virtualenv](http://www.virtualenv.org/en/latest/).
1. Make sure you have PostgreSQL installed.
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
  testing `python manage.py runserver --settings=systers_portal.settings.testing`.
1. Before commiting run `flake8 systers_portal` and fix PEP8 warnings.
1. Run `python systers_portal/manage.py test --settings=systers_portal.settings.testing`
  to run all the tests.



Run Portal with Docker
----------------------

If you want to take a speak peek at Systers Portal, a Docker container is for
you. The following Docker is not intended to be run in production at the
moment (but might be configured to do so in the future).

1. Install [Docker](https://docs.docker.com/installation/) on your system.
  Check the installation steps for your specific OS. Docker runs natively on
  Linux-based system. For Windows and Mac OS X, you should install VirtualBox
  and Boot2Docker.
1. Install [fig](http://www.fig.sh/install.html).
1. Clone the repo - `git clone git@github.com:systers/portal.git` and cd into
  the `portal` directory.
1. Run `fig build`. This command will pull the images required to run the project
  and will install the dependencies.
1. Run `docker run -e SECRET_KEY=foobarbaz portal_web` in your terminal.
1. Run `fig run web python systers_portal/manage.py migrate`.
1. Run `fig run web python systers_portal/manage.py createsuperuser` if you
  want to create a superuser to access the admin panel.
1. Run `fig up` to run the project.
1. Now Systers Portal should be running on port 8000. If you are on Linux, it
  is `http://0.0.0.0:8000`. If you are using Boot2Docker, then it might be
  `http://192.168.59.103:8000/`. If the following IP address doesn't work for
  you, run `boot2docker ip` and replace the previous ip with the Boot2Docker
  outputted IP address.


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
