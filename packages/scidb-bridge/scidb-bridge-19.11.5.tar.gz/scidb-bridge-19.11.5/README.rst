SciDB-Bridge: Python Library to access externally stored SciDB data
===================================================================

.. image:: https://img.shields.io/badge/SciDB-19.11-blue.svg
    :target: https://forum.paradigm4.com/t/scidb-release-19-11/2411

.. image:: https://img.shields.io/badge/arrow-3.0.0-blue.svg
    :target: https://arrow.apache.org/release/3.0.0.html


Requirements
------------

- Python ``3.5.x``, ``3.6.x``, ``3.7.x``, ``3.8.x``, ``3.9.x``, or ``3.10.x``
- SciDB ``19.11`` or newer
- SciDB-Py ``19.11.4`` or newer
- Apache PyArrow ``3.0.0``
- Boto3 ``1.14.12`` for Amazon Simple Storage Service (S3) support


Installation
------------

Install latest release::

  pip install scidb-bridge

Install development version from GitHub::

  pip install git+http://github.com/paradigm4/bridge.git#subdirectory=py_pkg


Contributing
------------

Check code style before committing code

.. code:: bash

  pip install pycodestyle
  pycodestyle py_pkg

For Visual Studio Code see `Linting Python in Visual Studio Code <https://code.visualstudio.com/docs/python/linting>`_
