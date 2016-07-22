==================
gbdx-task-template
==================

.. image:: https://circleci.com/gh/michaelconnor00/gbdx-task-template/tree/master.svg?style=shield
    :target: https://circleci.com/gh/michaelconnor00/gbdx-task-template/tree/master

.. image:: https://badge.fury.io/py/gbdx-task-template.svg
    :target: https://badge.fury.io/py/gbdx-task-template

A super class template for custom tasks to be run using gbdx-cloud-harness, see https://github.com/TDG-Platform/cloud-harness.

Development
-----------

**Contributing**

Please contribute! Please make pull requests directly to master. Before making a pull request, please:

* Ensure that all new functionality is covered by unit tests.
* Verify that all unit tests are passing.
* Ensure that all functionality is properly documented.t
* Ensure that all functions/classes have proper docstrings so sphinx can autogenerate documentation.
* Fix all versions in setup.py (and requirements.txt)

**Run Tests**

Tests use `pytest`_ framework

.. _pytest: http://pytest.org/latest/contents.html

::

  py.test [...]
  python -m pytest [...]


**Create a new version**

To create a new version::

    bumpversion ( major | minor | patch )
    git push --tags

Don't forget to update the changelog
