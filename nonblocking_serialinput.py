# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Stefan Krüger for s-light
#
# SPDX-License-Identifier: MIT
"""
`nonblocking_serialinput`
================================================================================

CircuitPython helper library to handle serial user input in an nonblocking way.


* Author(s): Stefan Krüger

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware `>= 7.0.0 for the supported boards.
    <https://github.com/adafruit/circuitpython/releases>`_
    * Core Module `usb_cdc:
    <https://circuitpython.readthedocs.io/en/latest/shared-bindings/usb_cdc/index.html>`_
"""

import time
import board
import supervisor

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/s-light/CircuitPython_nonblocking_serialinput.git"

##########################################
# NonBlockingSerialInput Class


class NonBlockingSerialInput(object):
    """docstring for NonBlockingSerialInput."""

    def __init__(self, arg):
        super(NonBlockingSerialInput, self).__init__()
        self.arg = arg


def memo(self):
    if supervisor.runtime.serial_connected:
        self.print_help()
    # prepare new input
    self.print_help()
    print(">> ", end="")


##########################################
# helper


def parse_value(self, input_string, pre_text):
    value = None
    # strip pre_text
    # ignore error 'whitespace before :'
    # pylama:ignore=E203
    input_string = input_string[len(pre_text) + 1 :]
    if "None" in input_string:
        value = None
    elif "False" in input_string:
        value = False
    elif "True" in input_string:
        value = True
    else:
        try:
            value = float(input_string)
        except ValueError as e:
            print(
                "Exception parsing '{pre_text}': {error}".format(
                    pre_text=pre_text,
                    error=e,
                )
            )
    return value


def is_number(s):
    """
    Return true if string is a number.

    based on
    https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
    """
    try:
        float(s)
    except TypeError:
        # return NaN
        return False
    else:
        return True
