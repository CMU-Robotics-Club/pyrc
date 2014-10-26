Installation
**************************

.. note::
  Currently pyrc has only been tested on python3.4.  It will likely work on other versions
  however these versions have not been tested.  If you have bugs using other versions or have tested
  it on a different version and it works please file a ticket at `pyrc Issues Page <https://github.com/CMU-Robotics-Club/pyrc/issues>`_


Git & Setup.py
=========================

::

  git clone https://github.com/CMU-Robotics-Club/pyrc
  cd pyrc/
  ./setup.py install


.. note::
  If you are modifying pyrc files you should also run

  ::

    ./setup.py develop

  which creates a symbolic link between your local files and the pyrc
  package installed system wide.  This means you do not have to run `install`
  every time you update a file.
