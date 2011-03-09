==============================================
Tinydocs: A minimalistic documentation system.
==============================================

Installation
============
To run tinydocs you must have the follow installed:

 * Python 2.5+
 * virtualenv 1.4.7+

Setting up environment
----------------------

Create a virtual environment where tinydocs dependencies will live::

    $ virtualenv --no-site-packages tinydocs
    $ source {path_to_virtual_envs}/tinydocs/bin/activate
    (tinydocs)$

Install tinydocs project dependencies::

    (tinydocs)$ pip install -r requirements/development.txt

If you are setting up a production environment use
``requirements/production.txt`` instead.

Running a web server
--------------------
In development you should run::

    (tinydocs)$ python tinydocs.py

