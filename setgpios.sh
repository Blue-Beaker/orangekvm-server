#! /bin/bash
# This is an example if your board needs some pull-up or pull-downs for CH9329 chip to work.
echo 11 > /sys/class/gpio/export
echo 0 > /sys/class/gpio/gpio11/active_low
echo out > /sys/class/gpio/gpio11/direction
echo 12 > /sys/class/gpio/export
echo 1 > /sys/class/gpio/gpio12/active_low
echo out > /sys/class/gpio/gpio12/direction
