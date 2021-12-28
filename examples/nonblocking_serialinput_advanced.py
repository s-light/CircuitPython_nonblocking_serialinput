#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Stefan Krüger for s-light
#
# SPDX-License-Identifier: Unlicense

"""Simple Minimal example of CircuitPython_nonblocking_serialinput library usage."""

import time
import sys
import board
import nonblocking_serialinput as nb_serialin

##########################################
# globals
my_input = nb_serialin.NonBlockingSerialInput()


class MyProjectMainClass(object):
    """This is just the Container Class for my Project."""

    def __init__(self, arg):
        super(MyProjectMainClass, self).__init__()
        self.arg = arg


##########################################
# menu


def print_help(self):
    """Print Help."""
    profile_list = ""
    # for name, profile in self.profiles.items():
    #     profile_list += "  {}\n".format(profile.title)
    # ^--> random order..
    for name in self.profiles_names:
        current = ""
        if self.profiles[name] is self.profile_selected:
            current = "*"
        profile_list += "  {: 1}{}\n".format(current, self.profiles[name].title_short)
    print(
        "you do some things:\n"
        "- 't': toggle print runtime ({print_runtime})\n"
        "- 's': set print runtime intervall ({intervall: > 7.2f})\n"
        "- 'pn' select next profil\n"
        "{profile_list}"
        "- 'calibrate'\n"
        "- 'start' reflow cycle\n"
        "- 'stop'  reflow cycle\n"
        "".format(
            profile_list=profile_list,
            heater_target=self.reflowcontroller.heater_target,
        ),
        end="",
    )
    self.print_temperature()


def check_input(self):
    """Check Input."""
    input_string = input()
    # sys.stdin.read(1)
    if "pn" in input_string:
        self.reflowcontroller.profile_select_next()
    if "pid p" in input_string:
        value = nb_serialin.parse_value(input_string, "pid p")
        if value:
            self.reflowcontroller.pid.P_gain = value
    if "h" in input_string:
        value = nb_serialin.parse_value(input_string, "h")
        if nb_serialin.is_number(value):
            self.reflowcontroller.heater_target = value
    # prepare new input
    self.print_help()
    print(">> ", end="")


@staticmethod
def input_parse_pixel_set(input_string):
    """parse pixel_set."""
    # row = 0
    # col = 0
    # value = 0
    # sep_pos = input_string.find(",")
    # sep_value = input_string.find(":")
    # try:
    #     col = int(input_string[1:sep_pos])
    # except ValueError as e:
    #     print("Exception parsing 'col': ", e)
    # try:
    #     row = int(input_string[sep_pos + 1 : sep_value])
    # except ValueError as e:
    #     print("Exception parsing 'row': ", e)
    # try:
    #     value = int(input_string[sep_value + 1 :])
    # except ValueError as e:
    #     print("Exception parsing 'value': ", e)
    # pixel_index = 0
    pass


##########################################
# functions


def main_update(self):
    """Do all the things your main code want's to do...."""
    pass


##########################################
# main


def main():
    """Main."""
    # wait some time untill the computer / terminal is ready
    for index in range(10):
        print(".", end="")
        time.sleep(0.5 / 10)
    print("")
    print(42 * "*")
    print("Python Version: " + sys.version)
    print("board: " + board.board_id)
    print(42 * "*")
    print("run")

    running = True
    while running:
        try:
            my_input.update()
        except KeyboardInterrupt as e:
            print("KeyboardInterrupt - Stop Program.", e)
            running = False
        else:
            main_update()


##########################################
if __name__ == "__main__":
    main()

##########################################
