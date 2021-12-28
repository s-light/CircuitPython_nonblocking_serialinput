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

runtime_print = True
runtime_print_next = time.monotonic()
runtime_print_intervall = 1.0

##########################################
# menu


def userinput_print_help(self):
    """Print Help."""
    global runtime_print
    global runtime_print_intervall
    print(
        "you do some things:\n"
        "- 't': toggle print runtime ({runtime_print})\n"
        "- 'time set:???': set print runtime intervall ({runtime_print_intervall: > 7.2f}s)\n"
        "- 'exit'  stop program\n"
        "".format(
            runtime_print=runtime_print,
            runtime_print_intervall=runtime_print_intervall,
        ),
        end="",
    )


def userinput_handling(input_string):
    """Check Input."""
    global runtime_print
    global runtime_print_intervall

    if "t" in input_string:
        runtime_print = not runtime_print
    if "time set" in input_string:
        value = nb_serialin.parse_value(input_string, "time set")
        if nb_serialin.is_number(value):
            runtime_print_intervall = value


##########################################
# functions


def main_update(self):
    """Do all the things your main code want's to do...."""
    global runtime_print
    global runtime_print_next
    global runtime_print_intervall

    if runtime_print:
        if runtime_print_next < time.monotonic():
            runtime_print_next = time.monotonic() + runtime_print_intervall
            print("{: > 7.2f}s)".format(time.monotonic()))


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
