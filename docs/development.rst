Development
****************************

Building the Documentation
===========================

.. note::
  You must have installed `sphinx` and `sphinx_rtd_theme` before
  you can build the documentation.  These packages can be obtained through
  `pip`.

::

  cd docs/
  make clean
  make apidoc
  make html
  make push
