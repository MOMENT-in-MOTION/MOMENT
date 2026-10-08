MOMENT
======

MOMENT generates Python APIs from JSON metamodels. This documentation covers
installation, command-line use, configuration, and the Python API.

Getting started
---------------

Install the application dependencies from the repository root:

.. code-block:: console

   python -m pip install -r requirements.txt

Save a metamodel as ``library.json``. A minimal model contains a root class:

.. code-block:: json

   {
     "name": "Library",
     "classes": [
       {
         "name": "Library",
         "attributes": [],
         "associations": [],
         "inherits": []
       }
     ]
   }

Generate the Python API from the repository root:

.. code-block:: console

   python -m src.main library.json

Generated files are written to ``output/`` by default. Choose another output
directory with ``-o`` and enable debug logging with ``-v``:

.. code-block:: console

   python -m src.main library.json --output generated -v

Metamodels and configuration
----------------------------

Metamodel JSON can define ``name``, ``enums``, and ``classes``. Classes may
contain ``attributes``, ``associations``, and ``inherits``. Attributes and
associations describe their multiplicity using values such as ``[1]`` or
``[0..*]``. Associations identify their target with ``target`` and can specify
``COMPOSITION`` or ``REFERENCE`` as their association type.

The generation settings are read from ``src/api_config.json``. In particular:

* ``ImportMode``: ``merge`` resolves links to JSON submodels; ``import`` emits
  references to external Python modules.
* ``NamingConvention``: selects ``snake_case`` or ``camelCase`` field naming.
* ``Inheritance``: selects ``native`` or ``manual`` inheritance handling.
* ``AllowUnreachableClasses``: controls whether classes unreachable from the
  root class are accepted.

When using ``merge``, association ``import_link`` values should identify JSON
submodel files. When using ``import``, they should identify Python module names.

Building the documentation
--------------------------

Install the documentation tools and build HTML from the repository root:

.. code-block:: console

   python -m pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints
   sphinx-apidoc --implicit-namespaces --force -o docs/source src
   sphinx-build -b html docs/source docs/build/html

The generated site is in ``docs/build/html``. Run the ``sphinx-apidoc`` command
again after changing the source package structure so the API pages stay current.

API reference
-------------

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   modules
   src.metamodel

