Aflowey
========

|PyPI| |Status| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/aflowey.svg
   :target: https://pypi.org/project/aflowey/
   :alt: PyPI
.. |Status| image:: https://img.shields.io/pypi/status/aflowey.svg
   :target: https://pypi.org/project/aflowey/
   :alt: Status
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/aflowey
   :target: https://pypi.org/project/aflowey
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/aflowey
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/aflowey/latest.svg?label=Read%20the%20Docs
   :target: https://aflowey.readthedocs.io/
   :alt: Read the documentation at https://aflowey.readthedocs.io/
.. |Tests| image:: https://github.com/jerkos/aflowey/workflows/Tests/badge.svg
   :target: https://github.com/jerkos/aflow/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/jerkos/aflowey/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/jerkos/aflowey
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


Features
--------

* Utilities to describe and execute flow with coroutine functions
* Easily launch several flows simultaneously
* Strong focus on readability

https://aflowey.readthedocs.io

Requirements
------------

* python 3.7 +

This library is easier to use with third party libraries for manipulating function
such as fn_ (flip function, function composition...), and tenacity_ (retry library).


Installation
------------

You can install *Aflowey* via pip_ from PyPI_:

.. code:: console

   $ pip install aflowey


Usage
-----

Chain function to execute an async flow !


.. code:: python

    from aflowey import aflow, CANCEL_FLOW, aexec, flog, partial

    db = ... # get client db

    # add some other library
    from tenacity import retry

    async def fetch_url(url):
        return await ...

    def process_data(html):
        processed_data = ...  # process data
        if processed_data is None:
            return CANCEL_FLOW

        return processed_data

    async def insert_into_db(content):
        return await db.insert_one(content)

    def get_url_flow(url):
        # defining a flow for working with url
        return (
            aflow.from_args("http://goole.fr")
            >> retry(wait=2)(fetch_url)
            >> flog("url fetched", print_arg=True)
            >> process_data  # this one is synchronous but may included in the flow
            >> insert_into_db
        )

Execute the flow for one url:

.. code:: python

    result = await get_url_flow("http://google.com/...").run()


Execute several flows asynchronously:

.. code:: python

        from fn import flip

        name = "Marco"

        user_flow = (
            aflow.empty()
            >> partial(db.find_one, search={"username": name})
            >> User.from_dict
            # the impure indicate that this step does not return a new result
            # i.e the result of User.from_dict will be sended
            >> impure(partial(flip(setattr), datetime.now(), 'created_at'))
        )

        organization_id = "Not employed"

        organization_flow = (
            aflow.empty()
            >> partial(db_find_one, search={"organization_id": organization_id})
            >> Organization.from_dict
        )

        urls = [
            "http://google.com/...",
            "http://google.com/...",
            "http://google.com/...",
            "http://google.com/...",
        ]

        url_flows = [get_url_flow(url) for url in urls]

        # execute all flow with asyncio gather method
        executor = aexec().from_flows(url_flows) | user_flow | organization_flow
        (url1, url2, url3, url4), user, organization = await executor.run()

It can be boring to create function that exactly matches arity of the flow.
Aflowey provide some higher order functions to help, see:

* lift: create a new method accepting transformed arguments
* F0: from a 0 argument function, create one argument function to fit the arity of the flow
* F1: create a new function with an extra parameter to process input of the flow step
* spread: create a new function which spread an iterable of arguments into the given function
* spread_kw: create a new function which spread kw arguments into the given function

The fn library provide other interesting functions like:

* flip
* first

If you have any other ideas...

Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_,
*Aflowey* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/jerkos/aflow/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://aflowey.readthedocs.io
.. _fn: https://github.com/kachayev/fn.py
.. _tenacity: https://github.com/jd/tenacity
