#!/usr/bin/env python3
# coding=utf-8

# SPDX-FileCopyrightText: Copyright (c) 2021 Stefan Krüger s-light.eu
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

**Software and Dependencies:**

* Adafruit CircuitPython firmware `>= 7.0.0 for the supported boards.
    <https://github.com/adafruit/circuitpython/releases>`_
    * Core Module `usb_cdc:
    <https://circuitpython.readthedocs.io/en/latest/shared-bindings/usb_cdc/index.html>`_
"""

import time

# import supervisor
import usb_cdc
import ansi_escape_code as terminal

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/s-light/CircuitPython_nonblocking_serialinput.git"

# pylint: disable=too-many-instance-attributes

##########################################
# NonBlockingSerialInput Class


class NonBlockingSerialInput:
    """Non Blocking Serial Input Class.

    This CircuitPython helper class can be used as non-blocking *drop-in* for the build
    in ``input()`` method.
    And also as event / callback based handling.
    It implements the full input buffer handling and line-end parsing.

    all parameters are keyword parameters.

    :param function input_handling_fn: function to call if there is one ore more
        fully received new lines. ``input_handling(input_string: string)``
        Default: None
    :param function print_help_fn:function to call when a help text should be printed
        fully received new lines. ``print_help()``
        Default: None
    :param ~usb_cdc.Serial serial: serial connection object to use
        Default: usb_cdc.console
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
        [`\n`, '\r', '\r\n']
        Default: True
    :param bool use_universal_line_end_advanced:  use a advanced default set of line_ends
        ['\v', '\f', '\x1c',...]
        Default: False
    :param bool verbose: print debugging information in some internal functions. Default to False

    """

    def __init__(
        self,
        *,  # force keyword arguments
        input_handling_fn=None,
        print_help_fn=None,
        serial=usb_cdc.console,
        echo=True,
        echo_pre_text=">> ",
        statusline=False,
        statusline_fn=None,
        statusline_intervall=1,
        encoding="utf-8",
        line_end_custom=None,
        use_universal_line_end_basic=True,
        use_universal_line_end_advanced=False,
        verbose=False,
    ):
        super()
        self.input_handling_fn = input_handling_fn
        self.print_help_fn = print_help_fn
        self.serial = serial
        self.echo = echo
        self.echo_pre_text = echo_pre_text
        self.statusline = statusline
        if statusline_fn:
            self.statusline_fn = statusline_fn
        else:
            self.statusline_fn = self._statusline_fn_default
        self.statusline_intervall = statusline_intervall
        self.statusline_next_update = time.monotonic()
        self.encoding = encoding
        self.line_end_list = []
        if line_end_custom:
            self.line_end_list.extend(line_end_custom)
        if use_universal_line_end_basic:
            self.line_end_list.extend(universal_line_end_basic)
        if use_universal_line_end_advanced:
            self.line_end_list.extend(universal_line_end_advanced)
        self.verbose = verbose

        # no block:
        self.serial.timeout = 0
        self.input_buffer = ""
        self.input_list = []

    ##########################################
    # output handling
    # statusline
    # echo

    @staticmethod
    def _statusline_fn_default():
        """Default statusline"""
        return "uptime:{uptime: >8.2f}".format(uptime=time.monotonic())

    def _statusline_update_check_intervall(self):
        """Update the Statusline if intervall is over."""
        if self.statusline_next_update <= time.monotonic():
            self.statusline_next_update = time.monotonic() + self.statusline_intervall
            self.statusline_print()

    def _get_statusline(self):
        return self.statusline_fn()

    def _get_echo_line(self):
        text = "{echo_pre_text}{input_buffer}".format(
            echo_pre_text=self.echo_pre_text,
            input_buffer=self.input_buffer,
        )
        return text

    def statusline_print(self):
        """Update the Statusline."""
        if self.statusline:
            move = ""
            # earease line
            move += terminal.ANSIControl.cursor.previous_line(1)
            move += terminal.ANSIControl.erase_line(2)

            # reprint echo
            line = self._get_statusline()

            # move back to bottom of screen
            moveback = terminal.ANSIControl.cursor.next_line(1)

            # execute all the things ;-)
            print(
                "{move}"
                "{line}"
                "{moveback}"
                "".format(
                    move=move,
                    line=line,
                    moveback=moveback,
                ),
                end="",
            )

    def echo_print(self):
        """Update the echho line."""
        if self.echo:

            move = ""
            # line_count = 1
            # if self.statusline:
            #     # jump over statusline
            #     line_count += 1
            # # eareas
            # move += terminal.ANSIControl.cursor.previous_line(line_count)
            # move += terminal.ANSIControl.cursor.previous_line(0)
            move += terminal.ANSIControl.erase_line(2)
            move += terminal.ANSIControl.cursor.horizontal_absolute(1)

            # reprint line
            line = self._get_echo_line()

            # move back to bottom of screen
            moveback = ""
            # line_count = 1
            # if self.statusline:
            #     # jump over statusline
            #     line_count += 1
            # moveback = terminal.ANSIControl.cursor.next_line(line_count)

            text = (
                "{move}"
                "{line}"
                "{moveback}"
                "".format(
                    move=move,
                    line=line,
                    moveback=moveback,
                )
            )
            # execute all the things ;-)
            print(text, end="")

    def print(self, *args):
        # def print(self, *args, end="\n"):
        """
        Print information & variables to the connected serial.

        This is a *drop in replacement* for the global print function.
        it is needed for the statusline handling to work.
        (we need to move the cursor...)

        currently it is not supported to print without newline at  end.

        :param object *args: things to print
        """
        # :param bool end: line end character to print. Default: "\n"
        if self.echo or self.statusline:
            move = ""
            # if self.statusline:
            #     # earease statusline
            #     move += terminal.ANSIControl.cursor.previous_line(1)
            #     move += terminal.ANSIControl.erase_line(2)
            if self.echo:
                # earease echoline
                # move += terminal.ANSIControl.cursor.previous_line(1)
                move += terminal.ANSIControl.erase_line(2)
            move += terminal.ANSIControl.cursor.horizontal_absolute(1)
            # print("\n\n\n{}\n\n\n".format(repr(move)))
            # print(repr(terminal.ANSIControl.cursor.previous_line(1)))
            # print(repr(terminal.ANSIControl.erase_line(2)))
            print(move, end="")
            # *normally print output
            print(*args)
            # print(*args, end=end)
            # print statement is finished.
            # now we have to reprint echo & statusline
            if self.echo:
                print(self._get_echo_line(), end="")
                # print(self._get_echo_line())
            # if self.statusline:
            #     print(self._get_statusline(), end="")
            # if not self.echo and not self.statusline:
            #     # add new end
            #     print()
        else:
            # print(*args, end)
            print(*args)

    # def out(self):
    #     pass

    ##########################################
    # input handling

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
            lines, rest = splitlines_advanced(self.input_buffer, self.line_end_list)
            self.input_list.extend(lines)
            if self.verbose:
                print("lines: {}; rest: {}".format(repr(lines), repr(rest)))
                print("self.input_list: {}".format(repr(self.input_list)))
            if rest:
                self.input_buffer = rest
            else:
                self.input_buffer = ""

    def _buffer_handle_backspace(self):
        if "\x08" in self.input_buffer:
            while (pos := self.input_buffer.find("\x08")) > -1:
                # strip character before backspace and backspace itself.
                self.input_buffer = (
                    self.input_buffer[: pos - 1] + self.input_buffer[pos + 1 :]
                )

    def _buffer_handle_cursor_position(self):
        # # TODO: implement Cursor position managment
        # if "\x08" in self.input_buffer:
        #     while (pos := self.input_buffer.find("\x08")) > -1:
        #         # strip character before backspace and backspace itself.
        #         self.input_buffer = (
        #             self.input_buffer[: pos - 1] + self.input_buffer[pos + 1 :]
        #         )
        pass

    def input(self):
        """
        Input.

        get oldest input string if there is any available. Otherwise an emtpy string.

        :return string: if available oldest input_line. Otherwise `""`
        """
        try:
            result = self.input_list.pop(0)
            self.print(result)
            if self.verbose:
                self.print("result: {}".format(repr(result)))
        except IndexError:
            result = None
        return result

    ##########################################
    # main handling

    def update(self):
        """Main update funciton. please call as often as possible."""
        if self.serial.connected:
            available = self.serial.in_waiting
            while available:
                raw = self.serial.read(available)
                text = raw.decode(self.encoding)
                # self._buffer_handle_cursor_position()
                self.input_buffer += text
                self._buffer_handle_backspace()
                if self.echo:
                    # self.serial.write(raw)
                    self.echo_print()
                # decode: keyword argeuments and errors not supported by CircuitPython
                # encoding=self.encoding,
                # errors="strict",
                self._buffer_check_and_handle_line_ends()
                available = self.serial.in_waiting
        parsed_input = False
        if self.input_handling_fn:
            while self.input_list:
                # first in first out
                oldest_input = self.input_list.pop(0)
                self.print(oldest_input)
                self.input_handling_fn(oldest_input)
                parsed_input = True
        if parsed_input and self.print_help_fn:
            self.print_help_fn()
        if self.statusline:
            self._statusline_update_check_intervall()


##########################################
# helper

"""
source for universal_line_end
https://docs.python.org/3.8/library/stdtypes.html#str.splitlines

:attribute list: universal_line_end_basic
:attribute list: universal_line_end_advanced
"""
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


# def find_first_line_end(input_string, line_end_list=None, start=0, return_line_end=False):
def find_first_line_end(input_string, line_end_list=None, start=0):
    """
    Find first line_end from line_end_list in input_string.

    :param string input_string: input search
    :param list line_end_list: list with strings to search for.
    :param int start: start position for search. (default = 0)
    :return int: index of first found line_end; `-1` if nothing is found.
    """
    result = None
    if line_end_list is None:
        line_end_list = universal_line_end_basic
    for line_end in line_end_list:
        index = input_string.find(line_end, start)
        # print("line_end: {: >10}; index: {}".format(repr(line_end), index))
        # just remember the first / smallest index
        if index > -1:
            if result is None:
                result = index
            else:
                result = min(index, result)
    if result is None:
        result = -1
    return result


def splitlines_advanced(input_string, line_end_list=None):
    """
    Split lines in input_string at all line_ends in line_end_list.

    This function searches for the all occurenc of all of strings in line_end_list.
    then splits at these points. the resulting list is returned.
    this also returns empty string segments.
    the search happens in the order of line_end_list.
    if the string does not end with a line_end symbol this last part will be returned in `rest`

    :param string input_string: input to split
    :param list line_end_list: list with strings where the splitting should happen.
    :return tuple: Tuple (result_list, rest);
    """
    if line_end_list is None:
        line_end_list = universal_line_end_basic
    result_list = []
    rest = None
    # we have to do the splitting manually as we have a list of available seperators..
    pos_last = 0
    while (
        pos := find_first_line_end(input_string, line_end_list, start=pos_last)
    ) > -1:
        # print("pos: {}".format(repr(pos)))
        # print("input_string[pos_last:pos]: {}".format(repr(input_string[pos_last:pos])))
        result_list.append(input_string[pos_last:pos])
        pos_last = pos + 1
        # print("pos_last: {}".format(repr(pos_last)))
    # print("pos_last: {}".format(repr(pos_last)))
    # print("len(input_string): {}".format(repr(len(input_string))))
    if pos_last < len(input_string):
        # print("  rest handling:")
        # print("input_string[pos_last:]: {}".format(repr(input_string[pos_last:])))
        rest = input_string[pos_last:]
    return (result_list, rest)


"""
debugging:
import nonblocking_serialinput as nbs
nbs.splitlines_advanced("Hallo\n Welt\r")

nbs.splitlines_advanced("Hallo\n Welt\rTag!")
nbs.splitlines_advanced("Hallo\n Welt\bEin Wünder Schön€r Tag!")

import nonblocking_serialinput as nbs
nbs.find_first_line_end("Hallo\nWelt\rTest", start=0)
nbs.find_first_line_end("Hallo\nWelt\rTest", start=5)
nbs.find_first_line_end("Hallo\nWelt\rTest", start=6)
nbs.find_first_line_end("Hallo\nWelt\rTest", start=11)
"""


def parse_value(input_string, pre_text=""):
    """
    Parse Value from input_string.

    known values are numbers (`float()` is used), None, True, False

    :param string input_string: input to parse
    :param string pre_text: text at start of input_string to ignore. defaults to ""
    :return float | None | True | False: parsed value
    """
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
        except ValueError as error:
            print(
                "Exception parsing '{pre_text}': {error}".format(
                    pre_text=pre_text,
                    error=error,
                )
            )
    return value


def is_number(value):
    """
    Return true if string is a number.

    based on
    https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float

    :param string value: input to check
    :return bool: True if value is a number, otherwise False.
    """
    try:
        float(value)
    except TypeError:
        # return NaN
        return False
    else:
        return True
