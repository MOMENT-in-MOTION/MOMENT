Getting Started
===============

Install MOMENT's application dependencies from the repository root:

.. code-block:: console

   python -m pip install -r requirements.txt

The example model defines a ``Library`` class with a required string field:

.. literalinclude:: ../examples/library.json
   :language: json

Generate the Python API into a separate directory:

.. code-block:: console

   python -m src.main docs/examples/library.json --output generated

The output directory contains ``class_code.py`` and, when configured, other
generated modules such as ``enum_code.py`` and ``serializer.py``. With the
repository's default relative-import setting, the directory is also a Python
package. Import and use the generated class from the repository root:

.. code-block:: python

   from generated.class_code import Library

   library = Library(name="Central Library")
   print(library.get_name())

Use ``-o`` or ``--output`` to choose another output directory. Add ``-v`` to
enable verbose logging. Use ``-c`` or ``--config`` to select another API
configuration JSON file. Run ``python -m src.main --help`` for command-line
help.