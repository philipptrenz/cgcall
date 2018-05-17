#!/bin/bash
#
#=================================================================================
# Name        : cgcall.sh
# Version     : 0.1
#
# Copyright (C) 2012 by Andre Wussow, 2012, desk@binerry.de
#
# Description :
#     Sample Script for controlling cgcall.
#
# Dependencies:
#	- pjsip
# 	- espeak
#
# References:
# https://github.com/philipptrenz/cgcall
#
#================================================================================
#This script is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.
#
#This script is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#================================================================================

DIR="/home/pi/cgcall"
CONFIG="$DIR/cgcall.cfg"

NAME1=cgcall
PIDFILE1=/var/run/$NAME1.pid
DAEMON1=$DIR/cgcall
DAEMON_OPTS1="--config-file $CONFIG"

NAME2=cgcall_py
PIDFILE2=/var/run/$NAME2.pid
DAEMON2=/usr/bin/python3
DAEMON_OPTS2="$DIR/scripts/get_recordings.py $CONFIG"


export PATH="${PATH:+$PATH:}/usr/sbin:/sbin:/home/pi/cgcall:"

case "$1" in
  start)
    echo "Starting daemon: "$NAME1
	start-stop-daemon --start --make-pidfile --pidfile $PIDFILE1 --chdir $DIR --chuid pi:pi --startas /bin/bash -- -c "exec $DAEMON1 $DAEMON_OPTS1 > $DIR/log/$NAME1.log 2>&1"
	echo "Starting daemon: "$NAME2
	start-stop-daemon --start --make-pidfile --pidfile $PIDFILE2 --chdir $DIR --chuid pi:pi --startas /bin/bash -- -c "exec $DAEMON2 $DAEMON_OPTS2 > $DIR/log/$NAME2.log 2>&1"
    echo "."
	;;
  stop)
    echo "Stopping daemon: "$NAME1
	start-stop-daemon --stop --pidfile $PIDFILE1 --remove-pidfile
	echo "Stopping daemon: "$NAME2
	start-stop-daemon --stop --pidfile $PIDFILE2 --remove-pidfile
    echo "."
	;;

  *)
	echo "Usage: "$1" {start|stop}"
	exit 1
esac

exit 0
