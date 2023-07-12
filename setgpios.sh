#! /bin/bash
# This is an example if your board needs some pull-up or pull-downs for CH9329 chip to work.
echo 2 > /sys/class/gpio/export
echo 0 > /sys/class/gpio/gpio2/active_low
echo out > /sys/class/gpio/gpio2/direction
echo 3 > /sys/class/gpio/export
echo 1 > /sys/class/gpio/gpio3/active_low
echo out > /sys/class/gpio/gpio3/direction
