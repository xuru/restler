restler
=======

Restler is an object Serialization library for the web. It supports
translating objects to JSON or XML. Currently, it is targeted at
Google App Engine. Documentation can be found at:
http://substrate-docs.appspot.com/restler.html

If you are using App Engine, you may also be interested in Substrate,
which packages Restler and several other useful libraries into an
application template: http://substrate-docs.appspot.com

Installation
------------

Install Restler from PyPi using easy_install or pip; or download the
package and run::

  python setup.py install

(Running ``setup.py`` requires setuptools.)

Running Tests
-------------

To run restler's tests::

  ./run_tests.py

Running tests requires unittest2 and the Google App Engine SDK.
  
Usage
-----

A db.Model instance can be serialized with the default settings using ``to_json`` or ``to_xml``.

>>> jean = Person(first_name="Jeanne", last_name="d'Arc", ssn="N/A")
>>> to_json(jean)
'{"first_name": "Jeanne", "last_name": "d\'Arc", "ssn": "N/A"}'

To include only certain fields, use a ``ModelStrategy``.

>>> person_strategy = ModelStrategy(Person).include("first_name", "last_name")
>>> to_json(jean, person_strategy)
'{"first_name": "Jeanne", "last_name": "d'Arc"}'

Or, to exclude specified fields:

>>> person_strategy = ModelStrategy(Person, include_all_fields=True).exclude("ssn")
>>> to_json(jean, person_strategy)
'{"first_name": "Jeanne", "last_name": "d'Arc"}'

For more details on customizing serialization, see the documentation.


TODO
----

- re-arrange so importing serializers does not require Google App Engine
- Support models other that App Engine's db.Model (Django models, dicts, plain old Python objects, etc.)
