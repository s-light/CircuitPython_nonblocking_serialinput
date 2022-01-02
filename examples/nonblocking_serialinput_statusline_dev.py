#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: Copyright (c) 2021 Stefan Krüger s-light
#
# SPDX-License-Identifier: Unlicense

"""Development things,"""

import time
import board
import digitalio
import nonblocking_serialinput as nb_serialin

##########################################
# globals
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

##########################################
# menu

my_input = nb_serialin.NonBlockingSerialInput()

##########################################
# main


def main():
    """Main."""
    # wait for serial terminal to get ready..
    time.sleep(1)
    print("")
    print("nonblocking_serialinput_simpletest.py")
    print(42 * "*")

    runtime_print_next = time.monotonic()
    runtime_print_intervall = 1.0
    running = True
    while running:
        # input handling
        my_input.update()
        input_string = my_input.input()
        if input_string is not None:
            # print("input_string: {}".format(repr(input_string)))
            # we have at least a empty string.
            if "exit" in input_string:
                print("Stop Program running.")
                running = False
            elif "hello" in input_string:
                print("World :-)")
            else:
                print("type 'exit' to stop the program.")
        # live sign
        if runtime_print_next < time.monotonic():
            runtime_print_next = time.monotonic() + runtime_print_intervall
            print("{: > 7.2f}s".format(time.monotonic()))
            led.value = not led.value


##########################################
if __name__ == "__main__":
    main()

##########################################
