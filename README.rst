========
myr.base
========

.. image:: https://travis-ci.org/Vnet-as/myr-base.svg?branch=master
   :target: https://travis-ci.org/Vnet-as/myr-base

.. image:: https://codecov.io/gh/Vnet-as/myr-base/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Vnet-as/myr-base


Base package for ``myr-stack`` tasks

Installation
============

Development
-----------

Create `virtualenv <https://virtualenv.pypa.io/en/stable/>`_ and activate it,
then proceed to install ``myr-base`` for development:

.. code-block:: bash

    $ git clone https://github.com/Vnet-as/myr-base.git
    $ cd myr-base
    $ pip install -e .

Usage
=====

.. code-block:: python

    from myr.base.app import MyrApp

    # just wrapper around Celery
    app = MyrApp()

    # create tasks as usual Celery tasks
    @app.task
    def sometask():
        do_something()


Do not forget to also run Celery beat, so the auto-announcing feature works.

.. code-block:: bash

    $ celery beat -A app
