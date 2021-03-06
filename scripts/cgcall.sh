#!/bin/sh
### BEGIN INIT INFO
# Provides:          cgcall
# Required-Start:    $local_fs $network $named $time $syslog
# Required-Stop:     $local_fs $network $named $time $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       A SIP audio player for audio records
### END INIT INFO

DIR="/home/pi/cgcall"
CONFIG="$DIR/cgcall.cfg"

NAME1=cgcall
PIDFILE1=/var/run/$NAME1.pid
DAEMON1=$DIR/cgcall
DAEMON_OPTS1="--config $CONFIG"

NAME2=cgcall_py
PIDFILE2=/var/run/$NAME2.pid
DAEMON2=/usr/bin/python3
DAEMON_OPTS2="$DIR/scripts/get_recordings.py $CONFIG"

export PATH="${PATH:+$PATH:}/usr/sbin:/sbin:/home/pi/cgcall:"


start() {
  echo "Starting daemon: "$NAME1
  start-stop-daemon --start --pidfile $PIDFILE1 --make-pidfile --chdir $DIR --chuid pi:pi --background --startas $DAEMON1 -- $DAEMON_OPTS1
  echo "Starting daemon: "$NAME2
  start-stop-daemon --start --pidfile $PIDFILE2 --make-pidfile --chdir $DIR --chuid pi:pi --background --startas $DAEMON2 -- $DAEMON_OPTS2
}

stop() {
  echo "Stopping daemon: "$NAME1
  start-stop-daemon --stop --pidfile $PIDFILE1 --remove-pidfile
  echo "Stopping daemon: "$NAME2
  start-stop-daemon --stop --pidfile $PIDFILE2 --remove-pidfile
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}"
esac
