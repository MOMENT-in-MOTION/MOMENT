Metamodel Format
================

A metamodel is a JSON object with a model ``name`` and lists of ``classes``
and, optionally, ``enums``. Each class has a ``name`` and may define
``attributes``, ``associations``, and ``inherits``.

Attributes define a ``name``, an ``attribute_type`` (``STRING``, ``INT``, or
``BOOL``), and a ``multiplicity``. They can also define a ``default_value``.
Multiplicity uses lower and upper bounds: ``[1]`` for exactly one,
``[0..1]`` for optional, ``[0..*]`` for zero or more, and ``[1..*]`` for one or
more.

Associations define a ``name``, a ``target``, a ``multiplicity``, and an
``association_type`` of ``COMPOSITION`` or ``REFERENCE``. An optional
``import_link`` identifies an external model or Python module, depending on the
configured import mode. Classes can list superclass names in ``inherits``.

For a complete minimal example, see :download:`library.json
<../examples/library.json>`:

.. literalinclude:: ../examples/library.json
   :language: json

Enums contain a ``name`` and a list of string ``values``. The first class in the
``classes`` list is the root class. Reachability is determined from this class
when ``AllowUnreachableClasses`` is disabled.