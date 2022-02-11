#!/usr/bin/env python3
# coding=utf-8

# SPDX-FileCopyrightText: Copyright (c) 2021 Stefan Krüger s-light.eu
#
# SPDX-License-Identifier: MIT
"""
`nb_in`
================================================================================

CircuitPython helper library to handle serial user input in an nonblocking way.
This File contains default Helpers.


* Author(s): Stefan Krüger

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware
    `>= 7.0.0 for the supported boards. <https://github.com/adafruit/circuitpython/releases>`_
    * Core Module ` ``usb_cdc``
    <https://circuitpython.readthedocs.io/en/latest/shared-bindings/usb_cdc/index.html>`_
* `CircuitPython_ansi_escape_code <https://github.com/s-light/CircuitPython_ansi_escape_code>`_
"""

import NonBlockingSerialInput
import usb_cdc

# pylint: disable=too-many-instance-attributes
# pylint: disable=too-few-public-methods

##########################################
# NonBlockingSerialInput Class


class NBSIConsole(NonBlockingSerialInput):
    r"""Non Blocking Serial Input Class.

    This CircuitPython helper class can be used as non-blocking *drop-in* for the build
    in ``input()`` method.
    And also as event / callback based handling.
    It implements the full input buffer handling and line-end parsing.

    all parameters are keyword parameters.

    :param function input_handling_fn: function to call if there is one ore more
        fully received new lines. ``input_handling(input_string: string)``
        Default: None
    :param function print_help_fn: function to call when a help text should be printed
        fully received new lines. ``print_help()``
        Default: None
    :param bool echo: enable/disable remote echo
        Default: True
    :param string echo_pre_text: Text to put on line start if echo is active
        Default: ">> "
    :param string statusline: enable/disable status line handling - `Not implemented yet - issue #1:
        <https://github.com/s-light/CircuitPython_nonblocking_serialinput/issues/1>`_
        Default: None
    :param function statusline_fn: callback function for statusline output.
        must return the string to use as statusline. ``def statusline_fn() string:``
        Default: "uptime:{runtime}"
    :param string statusline_intervall: time intervall in seconds to update the statusline
        Default: 1s
    :param string encoding: input string encoding
        Default: "utf-8"
    :param string, list line_end_custom: set custom line ends
        Default: None
    :param bool use_universal_line_end_basic: use a basic default set of line_ends
        ``['\n', '\r', '\r\n']``]
        Default: True
    :param bool use_universal_line_end_advanced:  use a advanced default set of line_ends
        ``['\v', '\f', '\x1c',...]``
        Default: False
    :param bool verbose: print debugging information in some internal functions. Default to False

    """

    def __init__(self, **kwds):
        kwds["serial"] = usb_cdc.console
        super().__init__(**kwds)


class NBSIData(NonBlockingSerialInput):
    r"""Non Blocking Serial Input Class.

    This CircuitPython helper class can be used as non-blocking *drop-in* for the build
    in ``input()`` method.
    And also as event / callback based handling.
    It implements the full input buffer handling and line-end parsing.

    all parameters are keyword parameters.

    :param function input_handling_fn: function to call if there is one ore more
        fully received new lines. ``input_handling(input_string: string)``
        Default: None
    :param function print_help_fn: function to call when a help text should be printed
        fully received new lines. ``print_help()``
        Default: None
    :param bool echo: enable/disable remote echo
        Default: True
    :param string echo_pre_text: Text to put on line start if echo is active
        Default: ">> "
    :param string statusline: enable/disable status line handling - `Not implemented yet - issue #1:
        <https://github.com/s-light/CircuitPython_nonblocking_serialinput/issues/1>`_
        Default: None
    :param function statusline_fn: callback function for statusline output.
        must return the string to use as statusline. ``def statusline_fn() string:``
        Default: "uptime:{runtime}"
    :param string statusline_intervall: time intervall in seconds to update the statusline
        Default: 1s
    :param string encoding: input string encoding
        Default: "utf-8"
    :param string, list line_end_custom: set custom line ends
        Default: None
    :param bool use_universal_line_end_basic: use a basic default set of line_ends
        ``['\n', '\r', '\r\n']``]
        Default: True
    :param bool use_universal_line_end_advanced:  use a advanced default set of line_ends
        ``['\v', '\f', '\x1c',...]``
        Default: False
    :param bool verbose: print debugging information in some internal functions. Default to False

    """

    def __init__(self, **kwds):
        kwds["serial"] = usb_cdc.data
        super().__init__(**kwds)
