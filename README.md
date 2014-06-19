Systers Portal Project
======================

Systers Portal is for Systers communities to post and share information within and with other communities.

Our project page >> http://systers.github.io/portal/

More information on technical architecture of this project coming soon...


Setup for developers
--------------------

1. Make sure you have installed Python 2.6.5 or higher, [pip](https://pip.pypa.io/en/latest/) 
   and [virtualenv](http://www.virtualenv.org/en/latest/)
2. Create a virtual environment and install dependencies

 ```bash
 $ virtualenv venv
 $ source venv/bin/activate
 $ pip install -r requirements.txt
 ```
3. Make sure you have PostgreSQL database up and running
4. Create `systersdb` database, where `systersdb` might be any suitable name
5. Fill in the database details in `systers_portal/settings/dev.py`
6. Run `export SECRET_KEY=foobarbaz` in your terminal, ideally the secret key 
  should be 40 characters long, unique and unpredictable
7. Run `python systers_portal/manage.py syncdb`
8. Run `python systers_portal/manage.py runserver` to start the development server. When in testing
  or production, feed the respective settings file from the command line, e.g. for  
  testing `python manage.py runserver settings=systers_portal.settings.testing`
9. Before commiting run `flake8 systers_portal` and fix PEP8 warnings
10. Run `python systers_portal/manage.py test` to run all the tests


Documentation
-------------

Documentation for Systers Portal is generated using [Sphinx](http://sphinx-doc.org/).
For more information on semantics and builds, please refer to the Sphinx
[official documentation](http://sphinx-doc.org/contents.html).

You can view the requirements document [here](docs/requirements/Systers_GSoC14_Portal_Requirements.pdf).
