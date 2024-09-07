========
tomlhold
========

Overview
--------

A holder for TOML data.

Installation
------------

To install tomlhold, you can use `pip`. Open your terminal and run:

.. code-block:: bash

    pip install tomlhold

Example
-------

Here's a simple example.

.. code-block:: python

    import tomlhold
    h = tomlhold.Holder("foo = 42")
    print(h["foo"])

This will output:

.. code-block:: text

    42

License
-------

This project is licensed under the MIT License.

Links
-----

* `Download <https://pypi.org/project/tomlhold/#files>`_
* `Source <https://github.com/johannes-programming/tomlhold>`_

Credits
-------

- Author: Johannes
- Email: johannes-programming@mailfence.com

Thank you for using tomlhold!