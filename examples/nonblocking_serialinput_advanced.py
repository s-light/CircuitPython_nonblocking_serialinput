#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: Copyright (c) 2021 Stefan Krüger for s-light
#
# SPDX-License-Identifier: Unlicense

"""Simple Minimal example of CircuitPython_nonblocking_serialinput library usage."""

import time
import sys
import board
import digitalio
import nonblocking_serialinput as nb_serialin

##########################################
# globals
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

running = True

runtime_print = True
runtime_print_next = time.monotonic()
runtime_print_intervall = 1.0

##########################################
# menu


def userinput_print_help():
    """Print Help."""
    global runtime_print
    global runtime_print_intervall
    print(
        "you can change some things:\n"
        "- 'tr': toggle print runtime ({runtime_print})\n"
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
    global running
    global runtime_print
    global runtime_print_next
    global runtime_print_intervall

    if "tr" in input_string:
        runtime_print = not runtime_print
    if "time set" in input_string:
        print("time set:")
        value = nb_serialin.parse_value(input_string, "time set")
        if nb_serialin.is_number(value):
            runtime_print_intervall = value
            runtime_print_next = time.monotonic() + runtime_print_intervall
    if "exit" in input_string:
        print("Stop Program running.")
        running = False


my_input = nb_serialin.NonBlockingSerialInput(
    input_handling_fn=userinput_handling,
    print_help_fn=userinput_print_help,
)

##########################################
# functions


def main_update():
    """Do all the things your main code want's to do...."""
    global runtime_print
    global runtime_print_next
    global runtime_print_intervall

    if runtime_print:
        if runtime_print_next < time.monotonic():
            runtime_print_next = time.monotonic() + runtime_print_intervall
            print("{: > 7.2f}s".format(time.monotonic()))
            led.value = not led.value


##########################################
# main


def main():
    """Main."""
    # wait some time untill the computer / terminal is ready
    for i in range(10):
        print(".", end="")
        time.sleep(0.5 / 10)
    print("")
    print(42 * "*")
    print("nonblocking_serialinput_advanced.py")
    print("Python Version: " + sys.version)
    print("board: " + board.board_id)
    print(42 * "*")
    print("run")

    global running
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
