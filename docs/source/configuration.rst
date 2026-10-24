Configuration
=============

MOMENT reads generation settings from ``src/api_config.json`` by default. Use
the ``-c`` or ``--config`` command-line option to select a different JSON
configuration file:

.. code-block:: console

   python -m src.main path/to/metamodel.json --config path/to/api_config.json

The default configuration path is resolved relative to the installed project;
the path supplied with ``--config`` is resolved from the process's current
working directory.

The following table describes the values checked into the repository. Boolean
settings are represented as the strings ``"true"`` and ``"false"``.

.. list-table:: Generation settings
   :header-rows: 1
   :widths: 28 22 50

   * - Setting
     - Checked-in value
     - Effect
   * - ``GenerateGetters``
     - ``"true"``
     - Generate getter methods for fields.
   * - ``GenerateSetters``
     - ``"true"``
     - Generate setter methods for fields.
   * - ``GenerateConstructors``
     - ``"true"``
     - Generate class constructors.
   * - ``GenerateHasFunctions``
     - ``"true"``
     - Generate methods that report whether a field has a value.
   * - ``StrictPrivacy``
     - ``"true"``
     - Prefix generated fields with an underscore.
   * - ``UseDoubleUnderscore``
     - ``"false"``
     - Use two leading underscores for private fields when strict privacy is enabled.
   * - ``ExplicitTypeSafety``
     - ``"true"``
     - Generate runtime type checks in constructors and setters.
   * - ``NamingConvention``
     - ``"snake_case"``
     - Choose ``snake_case`` or ``camelCase`` for generated field and method names.
   * - ``AllowUnreachableClasses``
     - ``"true"``
     - Allow classes that cannot be reached from the root class.
   * - ``RelativeImports``
     - ``"true"``
     - Generate relative imports between generated modules and an ``__init__.py`` file.
   * - ``Inheritance``
     - ``"native"``
     - Choose ``native`` inheritance or ``manual`` field inheritance.
   * - ``ImportMode``
     - ``"merge"``
     - In ``merge`` mode, resolve ``import_link`` values as JSON model paths. In ``import`` mode, treat them as Python module names.
   * - ``SerializationFormat``
     - ``["json", "xml"]``
     - Enable serializer generation for the listed formats.

When using ``merge``, ``import_link`` values refer to JSON submodels. In
``import`` mode, they refer to external Python modules. The two forms are not
interchangeable; see :doc:`metamodel_format` for the model structure.