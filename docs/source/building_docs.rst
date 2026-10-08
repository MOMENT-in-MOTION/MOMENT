Building the Documentation
==========================

Install the documentation dependencies from the repository root:

.. code-block:: console

   python -m pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints

Generate API pages and build the HTML site:

.. code-block:: console

   cd docs
   sphinx-apidoc --implicit-namespaces --force --maxdepth 2 --templatedir source/_templates/apidoc -o source ../src
   sphinx-build -b html source build/html

The finished site is in ``docs/build/html``. Open ``index.html`` through a
local HTTP server to use Sphinx search reliably. Regenerate the API pages after
changing the source package structure; CI performs both steps automatically.