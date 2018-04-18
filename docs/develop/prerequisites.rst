Prerequisites
=============

Before diving into development, please take a minute to check if you have all
the necessary tools and skills to get started. You should be familiar with the
following:

* Windows\Unix environment (GNU/Linux, OS X, etc) 
* Git version control system: committing, pushing, pulling, branching
* Python programming language
* Django framework
* HTML, CSS, JavaScript for front-end coding
* Unittesting
* PEP8

If you don't know yet any of these, please take some time to read about,
understand and practise the tools.

Unix System
-----------

Unix systems are so far the most developer-friendly environments. If you don't
have a Unix system installed on your machine, try out
`Ubuntu <http://www.ubuntu.com/download/desktop>`_. It is a free operating system
with constant updates, friendly X Window System and comes with Python pre-installed.
From the developer's perspective you should be comfortable using a terminal.
Theoretically is it possible to stick with Windows OS, though none or very little
assistance will be provided for OS specific issues.

Windows System
--------------

If you are not familiar with any unix system and want to get started on windows that's fine.

Git
---

If you have never heard of git, go ahead and read the
`first 3 chapters of Pro Git book <http://git-scm.com/doc>`_. On the same page you
can find cheatsheets, video lessons and a reference manual.

Python
------

Please be sure you speak fluent Python, as it is the main language Systers Portal
is written in. Essentially you should know how to invoke Python interpreter,
manipulate numbers, strings, lists, tuples, dictionaries, sets, use control flow
tools (if, for, break, continue, pass), I/O operations, errors and exceptions,
classes, inheritance. It is a plus if you know about decorators, regular
expressions, generators, iterators.

Django
------

Django is one of the most popular Python web framework. Django official website
contains pretty detailed `documentation <https://docs.djangoproject.com/en/>`_. At
first try out the tutorial and build a small app. After you feel confident about
Django, scroll through Systers Portal codebase to check your understanding. If
some parts seem complicated, go back to the documentation to focus on a specific
topic or layer.


HTML, CSS, JavaScript
---------------------

The good news is that the front-end of Systers Portal is kept as simple as possible.
You should be comfortable with writing HTML, CSS and maybe a bit of JavaScript.

Unittesting
-----------

"Untested code is broken code", that's why we try to write unittests for every
new functionality. Testing helps us validate the functionality we already have
and check whether the new code is implemented correctly. For that we use the
Django unittest module. There are plenty of good resource on unittesting, but you
can start with `Django testing <https://docs.djangoproject.com/en/1.7/topics/testing/>`_.

PEP8
----

PEP8 is the style guide for Python code. We are following the guide throughout
the whole codebase and check everything against a PEP8 linter. So please take
some time to read through this document - https://www.python.org/dev/peps/pep-0008.
