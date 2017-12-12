#!/bin/sh
exec > /var/log/temp-and-humidity.log 2>&1
while :; do
	#(sleep 10;/usr/bin/sudo SENSOR_NAME="$@" /usr/bin/python sensor_reader.py)&
	/usr/bin/sudo SENSOR_NAME="$@" /usr/bin/python sensor_reader.py
        done
