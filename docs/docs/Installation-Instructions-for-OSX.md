---
id: setup-osx
title: Installation Instructions for OSX
---

Setup for Developers (working on OSX)
=======================================

* **Requirements:**
        * Django v1.11
        * Python 3.3.5
        * `PostgreSQL <https://www.postgresql.org/download/macosx/>`_
        * `Homebrew <https://brew.sh/>`_


*   Ensure that **SSL module** is also installed while installing Python 3.3.5. In case if you
    are not able to get the
    module then follow the following steps of code in the terminal to set up:
    (Replace *foo* in all the paths below with the Username on your system)::

         $ brew install openss
         $ brew install pyenv
         $ CFLAGS="-I$(brew --prefix openssl)/include" LDFLAGS="-L$(brew --prefix openssl)/lib" pyenv install 3.3.5
         $ cd /Users/foo/.pyenv)
         $ cd shims
         $ cat ~/.bashrc
         $ cat ~/.bash_profile

*   Open .bash_profile in text-editor and replace everything with: ::

         $ alias sudo="sudo "
         $ alias python3.3="/Users/foo/.pyenv/shims/python3.3"
         $ alias pip3.3="/Users/foo/.pyenv/shims/pip3.3"


    Also, delete the .bashrc file.
* ::

         $ source ~/.bash_profile
         $ alias
         $ pyenv global 3.3.5
         $ pip3.3 --version


 (Ensuring that pip version 9.0.1 is there. If it is not present then `install <https://pip.pypa.io/en/stable/installing/>`_.)

*   Create a virtual environment with Python 3 and install dependencies: ::

        $ virtualenv venv --python=/opt/python3.3/bin/python3.3
        $ source venv/bin/activate
        $ pip3.3 install -r requirements/dev.txt

*   Create *systersdb* database, where systersdb might be any suitable name.

*   Fill in the database details in systers_portal/settings/dev.py.

*   Run export SECRET_KEY= foobarbaz in your terminal, ideally the secret key should be 40
    characters long, unique and
    unpredictable. Optionally to set the shell variable every time you activate the virtualenv,
    edit venv/bin/activate and add to the bottom the export statement.

* ::

         $ python3.3 systers_portal/manage.py migrate
         $ python3.3 systers_portal/manage.py createsuperuser
         $ python3.3 systers_portal/manage.py runserver
