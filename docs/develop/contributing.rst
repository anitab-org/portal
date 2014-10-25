First contribution
==================

This guide will show you step by step how to make your first contribution to
Systers Portal.

#. Go to http://github.com and create a github account, if you don't have one yet.
#. Fork the `Systers Portal <https://github.com/systers/portal/>`_ repo. In the
   upper left corner there is **Fork** button. A "copy" of the project will appear
   in the list of your repositories.
#. Generate SSH keys and add the public key to your Github account. Github 
   provides `a very good article on how to do that <https://help.github.com/articles/generating-ssh-keys/>`_.
#. Suppose I have forked the project and my username is **foobar**. Now clone 
   the forked project to your system files (the ``$`` symbol denotes the shell 
   prompt, don't type it)::
      
      $ git clone git@github.com:foobar/portal.git

#. Enter the ``portal`` directory and checkout to ``develop`` branch::

      $ cd portal
      $ git checkout develop
      
#. Setup the project. The instruction can be found in 
   `README.md <https://github.com/systers/portal/#setup-for-developers>`_. The
   guide assumes that you will be able to install and configure by yourself 
   ``pip``, ``virtualenv`` and ``PostgreSQL``.
#. Choose a task to work on.
#. Create a new feature branch from ``develop`` branch. The feature branch 
   should have a short and relevant name. :: 

      $ git checkout -b <feature-branch-name>

#. Work on the task. Write unittests if necessary. When you consider the task 
   done, you should check the following:
     
      #. PEP8 style - ``flake8 systers_portal``. If ``flake8`` gives you warnings,
         please correct them. There should be nothing on output.
      #. Unittests - ``python systers_portal/manage.py test --settings=systers_portal.settings.testing``.
         This command will run all the unittests. If a unittest will fail or give
         errors, please check the traceback and correct the issues. Rerun the
         unittests.
      #. If you have made any changes to the HTML or have manipulates the DOM
         using JavaScript, please check the validity of the file. Open the page 
         in the browser, copy the page source code and paste it 
         `here <http://validator.w3.org/#validate_by_input>`_. If there are
         errors, please correct them and revalidate.  
#. If all the checks have passed, you can commit your changes. Please be careful
   to not commit any user-specific files or changes that are out of scope. You
   can make more commits, if you consider it is necessary. ::

      $ git add <file1> <file2>
      $ git commit -m "relevant commit message"

#. Push to your local branch::

      $ git push origin <feature-branch-name>

#. Go to github and make a pull request. Add description and point to the task
   you have solved.
#. Someone from the team will review your code, provide feedback and if
   everything is ok, will merge your changes. 
#. Don't forget to `sync your fork <https://help.github.com/articles/syncing-a-fork/>`_
   in case the upstream repo was updated.
   
