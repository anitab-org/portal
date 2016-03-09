Contributing
============
If you want to start contributing to Systers Portal or you are a regular
contributor, this is the place for you. It covers such topics as setting up the
project, working and updating pull requests, Continuous Integration with Travis.

.. NOTE::
   The ``$`` symbol denotes the shell prompt, don't type it.

Setup the project
-----------------
Before doing any actual work, it is necessary to prepare your local machine
for developement and deploy Systers Portal locally.

#. Install ``git`` on your local computer. If on Ubuntu, run::

      $ sudo apt-get install git-core

#. Set up your name and email address in ``git`` configuration::

      $ git config --global user.name "John Doe"
      $ git config --global user.email johndoe@example.com

#. Go to http://github.com and create a GitHub account, if you don't have one
   yet. Use the previously introduced email to create the GitHub account.
   That way GitHub will be able to associate your ``git`` commits with your
   GitHub profile.
#. Fork the `Systers Portal <https://github.com/systers/portal/>`_ repo. In the
   upper left corner there is **Fork** button. A "copy" of the project will appear
   in the list of your repositories.
#. Generate SSH keys and add the public key to your GitHub account. GitHub
   provides `a very good article on how to do that <https://help.github.com/articles/generating-ssh-keys/>`_.
#. Go to the page where the forked Systers Portal is. Copy the *SSH clone URL*
   from the right sidebar. If your username is *john-doe*, then the url will be
   ``git@github.com:john-doe/portal.git``. Now clone the forked project to your
   system files::

      $ git clone git@github.com:john-doe/portal.git

#. Install the project locally for development using `this guide from project
   README <https://github.com/systers/portal#setup-for-developers>`_.
#. Running tests and flake8 successfully with no errors or failures ensures
   that you have installed everything correctly.


Make a Contribution
-------------------
Say you have decided to fix a bug or implement a new feature. This guide will
show you step by step how to make a contribution to Systers Portal.

#. Systers Portal stable branch is ``master``. Periodically we make a release
   when the codebase is stable and can be used in production. ``Develop``
   branch is the branch that has all the latest changes and should be used as
   a base branch for development. And so enter the ``portal`` directory and
   checkout to ``develop`` branch. ::

      $ cd portal
      $ git checkout develop

#. Choose a task to work on. It can be a beginners task or a sophisticated
   feature you want to implement for Portal. For beginners we have tasks
   with `easy TODO tag on GitHub issues <https://github.com/systers/portal/issues>`_.
#. Create a new feature branch from ``develop`` branch. The feature branch
   should have a short and relevant name. ::

      $ git checkout -b <feature-branch-name>

#. Work on the task. Write tests if necessary. When you consider the task
   done, you should check the following:

      #. PEP8 style - ``flake8 systers_portal``. If ``flake8`` gives you warnings,
         please correct them. There should be nothing on output.
      #. Tests - ``python systers_portal/manage.py test --settings=systers_portal.settings.testing``.
         This command will run all the tests. If a test will fail or give
         errors, please check the traceback and correct the issues. Rerun the
         tests.
      #. Check test coverage::

            $ coverage run systers_portal/manage.py test --settings=systers_portal.settings.testing
            $ coverage report

         If the total coverage percentage is lower than the number that appears
         on the coverage badge on GitHub, then write tests to keep it on the
         same level or improve the test coverage.

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

#. Make sure you have the latest ``develop`` branch before pushing the feature
   branch. For that checkout to ``develop`` and pull the latest changes. If
   ``develop`` branch was updated, you should switch back to your feature branch
   and rebase your work against ``develop``. Solve conflicts, if there are any. ::

      $ git checkout develop
      $ git pull origin develop
      $ git checkout <feature-branch-name>
      $ git rebase develop

#. Push the feature branch::

      $ git push origin <feature-branch-name>


Make a Pull Request
-------------------
We use peer code review to accept or reject the changes made by contributors.
It helps to prevent many mistakes and guarantee project quality. For that
we use GitHub pull requests.

#. Go to GitHub and make a pull request. Choose a relevant title, add description
   if necessary and point to the task you have solved. The source branch of the
   pull request should be your feature branch and the target branch should be
   ``develop`` branch. Review your pull request and make sure everything is
   alright.
#. Someone from the team will review your code, provide feedback and if
   everything is ok, will merge your changes. If asked to make any changes,
   update the pull request by one of the two strategies presented below.
#. Don't forget to `sync your fork <https://help.github.com/articles/syncing-a-fork/>`_
   in case the upstream repo was updated.

Update a Pull Request
---------------------
Quite often the reviewer will leave comments and ask you to make some changes
to the initial code. There are 2 strategies how to update your pull request.

**Update same pull request**

#. Checkout on the feature branch - the source branch of the pull request.
#. Work on enhancements and suggestions.
#. Make a commit with ``amend`` option. It will update your last commit and will
   change the SHA-1 of that commit. ::

      $ git add <file1> <file2>
      $ git commit -amend

#. Make a force push to the feature branch. This will update the pull request
   automatically. But will not notify the reviewer about it, so consider leaving
   a comment about it in the pull request. The benefit is that the reviewer
   can see a diff between the previous submission and the new one.

**Create a new pull request**

#. Checkout on ``develop`` branch and create a new feature branch with an
   incremented version value at the end of the feature branch name. ::

      $ git checkout develop
      $ git checkout -b <feature-branch-name>2

#. Apply the same changes you have made on the first version of the feature
   branch, additionally applying enhancements and suggestions left by the
   reviewer.
#. Make a commit::

      $ git add <file1> <file2>
      $ git commit -m "relevant commit message"

#. Push the feature branch to GitHub and create a pull request.
#. Close the previous pull request manually.


Continuous Integration with Travis
----------------------------------

Travis CI Systers Portal - https://travis-ci.org/systers/portal

Coveralls Systers Portal - https://coveralls.io/r/systers/portal

For continuous integration we use Travis CI service. Every time we make a push
to Systers Portal repo, Travis builds our project and runs the tests. It also
notifies us about any errors or failures, that way preventing us from breaking
the project.

Along with Travis CI, we use code test coverage metric using coveralls service.
Please note that high coverage is not a guarantee for good tests.
