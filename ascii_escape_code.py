#!/usr/bin/env python3
# coding=utf-8

# SPDX-FileCopyrightText: Copyright (c) 2021 Stefan Krüger s-light.eu
#
# SPDX-License-Identifier: MIT
"""
`ASCII_escape_code`
================================================================================

simple helper library for common ASCII escape codes

inspired / based on information from
    - https://en.wikipedia.org/wiki/ANSI_escape_code
    - https://www.geeksforgeeks.org/print-colors-python-terminal/


* Author(s): Stefan Krüger

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware `>= 7.0.0 for the supported boards.
    <https://github.com/adafruit/circuitpython/releases>`_
"""

# pylint: disable=invalid-name, too-few-public-methods

import time

##########################################
# helper functions


def create_seq(control, esc="\033["):
    """
    Control sequences function generator.

    :param string control: control characters.
    :param string esc: escape character. Default: ``\033[``
    :return lambda: function generator with predefined control sequences.
    """
    return lambda value="": "{esc}{value}{control}".format(
        esc=esc, value=value, control=control
    )


def create_color(color):
    """
    Create color sequences.

    :param string color: color number (as string).
    :return string: ready to use color control character string.
    """
    return create_seq("m")(color)


##########################################
# ASCIIControllsBase Class


class ASCIIControllsBase:
    """
    Base Class for ASCII Color and Control Characters.
    """

    esc = "\033["

    # @staticmethod
    # def create_seq(control, esc=esc):
    #     return lambda value: "{esc}{value}{control}".format(
    #         esc=esc, value=value, control=control
    #     )

    @classmethod
    def get_flat_list(cls, obj_dict=None):
        """Get a flattend list of all control characters in dict."""
        result = []
        if obj_dict is None:
            obj_dict = cls.__dict__
        # print("*"*42)
        # print("obj_dict", obj_dict)
        # print("*"*42)
        for attr_name, attr_value in obj_dict.items():
            if not attr_name.startswith("__"):
                # if type(attr_value) is str:
                #     value_str = attr_value.replace("\x1b", "\\x1b")
                # else:
                #     value_str = attr_value
                # print(
                #     "'{}' '{}': {}  "
                #     "".format(
                #         attr_name,
                #         type(attr_value),
                #         value_str,
                #     ),
                #     end=""
                # )
                if isinstance(attr_value, str):
                    # print(" STRING ")
                    result.append(attr_value)
                elif isinstance(attr_value, type):
                    # print(" TYPE ")
                    result.extend(cls.get_flat_list(attr_value.__dict__))
                else:
                    # print(" UNKNOWN ")
                    pass
        # print("*"*42)
        return result


class ASCIIColors(ASCIIControllsBase):
    """
    ASCII Color and Font-Effects Control Characters.

    reset all colors with ASCIIColors.reset;
    two sub classes
        * ``fg`` for foreground
        * ``bg`` for background;
    use as ASCIIColors.subclass.colorname:
    ```
    ASCIIColors.fg.red
    ASCIIColors.bg.green
    ```

    the generic formatings
        * bold
        * disable
        * underline
        * reverse
        * strike through
        * invisible
    work with the main class:
    ``ASCIIColors.bold``
    """

    # reset = ASCIIControllsBase.esc + "0m"
    """
    reset

    :return string: ready to use sequences.
    """
    reset = create_color("0")
    """
    bold

    :return string: ready to use sequences.
    """
    bold = create_color("01")
    """
    disable

    :return string: ready to use sequences.
    """
    disable = create_color("02")
    """
    underline

    :return string: ready to use sequences.
    """
    underline = create_color("04")
    """
    reverse

    :return string: ready to use sequences.
    """
    reverse = create_color("07")
    """
    strikethrough

    :return string: ready to use sequences.
    """
    strikethrough = create_color("09")
    """
    invisible

    :return string: ready to use sequences.
    """
    invisible = create_color("08")

    # class fg:
    #     """Forderground Colors."""
    #
    #     black = create_color("30m")
    #     red = create_color("31m")
    #     green = create_color("32m")
    #     orange = create_color("33m")
    #     blue = create_color("34m")
    #     purple = create_color("35m")
    #     cyan = create_color("36m")
    #     lightgrey = create_color("37m")
    #     darkgrey = create_color("90m")
    #     lightred = create_color("91m")
    #     lightgreen = create_color("92m")
    #     yellow = create_color("93m")
    #     lightblue = create_color("94m")
    #     pink = create_color("95m")
    #     lightcyan = create_color("96m")
    #
    # class bg:
    #     """Background Colors."""
    #
    #     black = create_color("40m")
    #     red = create_color("41m")
    #     green = create_color("42m")
    #     orange = create_color("43m")
    #     blue = create_color("44m")
    #     purple = create_color("45m")
    #     cyan = create_color("46m")
    #     lightgrey = create_color("47m")

    class fg:
        """Forderground Colors."""

        """
        Forderground black

        :return string: ready to use sequences.
        """
        black = ASCIIControllsBase.esc + "30m"
        red = ASCIIControllsBase.esc + "31m"
        green = ASCIIControllsBase.esc + "32m"
        orange = ASCIIControllsBase.esc + "33m"
        blue = ASCIIControllsBase.esc + "34m"
        purple = ASCIIControllsBase.esc + "35m"
        cyan = ASCIIControllsBase.esc + "36m"
        lightgrey = ASCIIControllsBase.esc + "37m"
        darkgrey = ASCIIControllsBase.esc + "90m"
        lightred = ASCIIControllsBase.esc + "91m"
        lightgreen = ASCIIControllsBase.esc + "92m"
        yellow = ASCIIControllsBase.esc + "93m"
        lightblue = ASCIIControllsBase.esc + "94m"
        pink = ASCIIControllsBase.esc + "95m"
        lightcyan = ASCIIControllsBase.esc + "96m"

    class bg:
        """Background Colors."""

        black = ASCIIControllsBase.esc + "40m"
        red = ASCIIControllsBase.esc + "41m"
        green = ASCIIControllsBase.esc + "42m"
        orange = ASCIIControllsBase.esc + "43m"
        blue = ASCIIControllsBase.esc + "44m"
        purple = ASCIIControllsBase.esc + "45m"
        cyan = ASCIIControllsBase.esc + "46m"
        lightgrey = ASCIIControllsBase.esc + "47m"


class ASCIIControl(ASCIIControllsBase):
    """
    ASCII Cursor movement.

    please make sure your terminal supports these...
    tested with `GTKTerm:
    <https://circuitpython.readthedocs.io/en/latest/shared-bindings/usb_cdc/index.html>`_

    usage example:
    .. code-block:: python
        ASCIIControl.erease_line()
        ASCIIControl.cursor.up(5)
    """

    ED = erase_display = create_seq("J")
    EL = erase_line = create_seq("K")
    SU = scroll_up = create_seq("S")
    SD = scroll_down = create_seq("T")
    DSR = device_status_report = create_seq("n")("6")

    class cursor:
        """Cursor Movement."""

        """
        CUU - CUrsor Up

        :param string value: Lines to move up.
        :return string: ready to use sequences.
        """
        CUU = up = create_seq("A")
        CUD = down = create_seq("B")
        CUF = forward = create_seq("C")
        CUB = back = create_seq("D")
        CNL = next_line = create_seq("E")
        CPL = previous_line = create_seq("F")
        CHA = horizontal_absolute = create_seq("G")
        CUP = position = create_seq("H")


##########################################


def filter_ascii_controlls(data):
    """
    Remove ASCII controll characters.

    :param string data: input data to filter.
    :return string: filtered result.
    """
    code_list = []
    code_list.extend(ASCIIColors.get_flat_list())
    code_list.extend(ASCIIControl.get_flat_list())
    for list_entry in code_list:
        data = data.replace(list_entry, "")
    return data


def test_filtering():
    """
    Test for filter_ascii_controlls.

    print some test cases.
    """
    test_string = (
        ASCIIColors.fg.lightblue
        + "Hello "
        + ASCIIColors.fg.green
        + "World "
        + ASCIIColors.fg.orange
        + ":-)"
        + ASCIIColors.reset
    )
    print("test_string", test_string)
    test_filtered = filter_ascii_controlls(test_string)
    print("test_filtered", test_filtered)


def test_control():
    """
    Test for control sequences.

    print some test cases.
    """

    test_string = (
        ASCIIColors.fg.lightblue
        + "Hello "
        + ASCIIColors.fg.green
        + "World "
        + ASCIIColors.fg.orange
        + ":-)"
        + ASCIIColors.reset
    )
    print("test_string", test_string)
    print("test_string", test_string)
    print("test_string", test_string)
    time.sleep(1)
    test_string = (
        ASCIIControl.cursor.previous_line(2)
        + "WOOO"
        + ASCIIControl.cursor.next_line(1)
        + ASCIIControl.erase_line()
        + ":-)"
    )
    print(test_string)
