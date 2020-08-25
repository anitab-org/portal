---
id: coding-standard
title: Coding Standards
---


# Portal Coding Standards

Having python as then major development language, the following are the coding practices and standards which are being used in the project.

## Style Guide for Python

### [The PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/)

- The documentation gives coding conventions for the Python code comprising the standard library in the main Python distribution. Please see the companion informational PEP describing style guidelines for the C code in the C implementation of Python.
- This style guide evolves over time as additional conventions are identified and past conventions are rendered obsolete by changes in the language itself.

## Docstrings

Docstrings are used to make the code more understandable for contributors. PEP 257 [Docstring Convention](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) is being used as a docstring style guide.

## Testing

- Django unit tests are written to test the backend.
- Coverage reports are collected by [coveralls](https://coveralls.io/)
- Django-selenium tests are written for Web Driver Testing.

***Django-nose is used which helps in:***

- Testing just your apps by default, not all the standard ones that happen to be in INSTALLED_APPS
- Running the tests in one or more specific modules (or apps, or classes, or folders, or just running a specific test)
- Obviating the need to import all your tests into tests/__init__.py. This not only saves busy-work but also eliminates the possibility of accidentally shadowing test classes.
- Taking advantage of all the useful nose plugins
- Fixture bundling, an optional feature which speeds up your fixture-based tests by a factor of 4
- Reuse of previously created test DBs, cutting 10 seconds off startup time
- Hygienic TransactionTestCases, which can save you a DB flush per test
- Support for various databases. Tested with MySQL, PostgreSQL, and SQLite. Others should work as well.

***

# Particulars to be careful about
