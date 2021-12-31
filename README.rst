Introduction
============


.. image:: https://readthedocs.org/projects/circuitpython-nonblocking-serialinput/badge/?version=latest
    :target: https://circuitpython-nonblocking-serialinput.readthedocs.io/
    :alt: Documentation Status


.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/s-light/CircuitPython_nonblocking_serialinput/workflows/Build%20CI/badge.svg
    :target: https://github.com/s-light/CircuitPython_nonblocking_serialinput/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython helper library to handle serial user input in an nonblocking way.


Dependencies
=============
This helper library depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install nonblocking_serialinput

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. literalinclude:: ./examples/nonblocking_serialinput_simpletest.py
    :caption: examples/nonblocking_serialinput_simpletest.py
    :linenos:


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/s-light/CircuitPython_nonblocking_serialinput/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
