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
import usb_cdc

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/s-light/CircuitPython_nonblocking_serialinput.git"

##########################################
# NonBlockingSerialInput Class


class NonBlockingSerialInput(object):
    """docstring for NonBlockingSerialInput."""

    def __init__(
        self,
        *,  # force keyword arguments
        parse_input_fn=None,
        print_help_fn=None,
        serial=usb_cdc.console,
        encoding="utf-8",
        line_end_custom=None,
        universal_line_end_basic=True,
        universal_line_end_advanced=False,
    ):
        super(NonBlockingSerialInput, self).__init__()
        self.parse_input_fn = parse_input_fn
        self.print_help_fn = print_help_fn
        self.serial = serial
        self.encoding = encoding
        self.line_end_list = []
        if line_end_custom:
            self.line_end_list.extend(line_end_custom)
        if universal_line_end_basic:
            self.line_end_list.extend(self.universal_line_end_basic)
        if universal_line_end_advanced:
            self.line_end_list.extend(self.universal_line_end_advanced)

        # no block:
        self.serial.timeout = 0
        self.input_list = []

    def _parse_input_fallback(self, input_string):
        pass

    def _print_help_fallback(self):
        pass

    def memo(self):
        if self.serial_connected:
            self.print_help()
        # prepare new input
        self.print_help()
        print(">> ", end="")

    def _buffer_count_line_ends(self):
        result = 0
        for end in self.line_end_list:
            if end in self.input_buffer:
                result += 1
        return result

    def _buffer_endswith_line_end(self):
        # in python3 endswith() supports a tuple as argument
        # in micropython/CircuitPython we have to do it manually..
        # https://forum.micropython.org/viewtopic.php?t=4906
        #
        # we use a while loop to finish earlie
        # https://stackoverflow.com/a/59092738/574981
        result = None
        i = iter(self.line_end_list)
        while result is None and (end := next(i, None)) is not None:
            if self.input_buffer.endswith(end):
                result = end
        return result

    def _buffer_check_and_handle_line_ends(self):
        if self._buffer_count_line_ends():
            # we have at minimum one full command.
            # let us extract this.
            # buffer_endswith = self._buffer_endswith_line_end()
            # if buffer_endswith:
            #     # just split the lines and all is fine..
            #     pass
            # else:
            #     # we have to leave the last part in place..
            #     pass
            # self.input_list.extend(self.input_buffer.splitlines(self.line_end_list))
            lines, rest = self.splitlines_advanced(self.input_buffer)
            self.input_list.extend(lines)
            self.input_buffer = rest

    def input(self):
        """get oldest input string if there is any available. Otherwise None."""
        try:
            result = self.input_list.pop(0)
        except IndexError:
            result = None
        return result

    def update(self):
        """Main update funciton. please call as often as possible."""
        if self.serial.connected:
            available = self.serial.in_waiting
            while available:
                self.input_buffer += self.serial.read(available).decode(
                    encoding=self.encoding, errors="strict"
                )
                self._buffer_check_and_handle_line_ends()
                available = self.serial.in_waiting
        parsed_input = False
        while self.input_list:
            if self.parse_input_fn:
                # first in first out
                oldest_input = self.input_list.pop(0)
                self.parse_input_fn(oldest_input)
                parsed_input = True
        if parsed_input and self.print_help_fn:
            self.print_help_fn()


##########################################
# helper

# source for universal_line_end
# https://docs.python.org/3.8/library/stdtypes.html#str.splitlines
universal_line_end_basic = [
    # Line Feed
    "\n",
    # Carriage Return
    "\r",
    # Carriage Return + Line Feed
    "\r\n",
]
universal_line_end_advanced = [
    # Line Tabulation
    "\v",
    "\x0b",
    # Form Feed
    "\f",
    "\x0c",
    # File Separator
    "\x1c",
    # Group Separator
    "\x1d",
    # Record Separator
    "\x1e",
    # Next Line (C1 Control Code)
    "\x85",
    # Line Separator
    "\u2028",
    # Paragraph Seprator
    "\u2029",
]


def find_first_line_end(input_string, line_end_list=universal_line_end_basic, start=0):
    result = -1
    # print("input_string: {}".format(repr(input_string)))
    i = iter(line_end_list)
    while result is -1:
        try:
            line_end = next(i)
        except StopIteration:
            result = False
            # print("StopIteration")
        else:
            # print("line_end: {}".format(repr(line_end)))
            result = input_string.find(line_end, start)
        # print("result: {}".format(repr(result)))
    if result is False:
        result = -1
    return result


def splitlines_advanced(input_string, line_end_list):
    result = []
    rest = None
    # we have to do the splitting manually as we have a list of available seperators..
    pos_last = 0
    while (
        pos := find_first_line_end(input_string, line_end_list, start=pos_last)
    ) > -1:
        result.append(input_string[:pos])
        print("input_string[:pos]: {}".format(repr(input_string[:pos])))
        pos_last = pos
    if pos_last <= len(input_string):
        print("ping - rest")
    return (result, rest)


"""
debugging:
nbs.splitlines_advanced("Hallo\n Welt\bEin Wünder Schön€r Tag!", nbs.universal_line_end_basic)
import nonblocking_serialinput as nbs
nbs.find_first_line_end("Hallo\nWelt\rTest", start=0)
nbs.find_first_line_end("Hallo\nWelt\rTest", start=5)
nbs.find_first_line_end("Hallo\nWelt\rTest", start=6)
nbs.find_first_line_end("Hallo\nWelt\rTest", start=11)
"""


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
