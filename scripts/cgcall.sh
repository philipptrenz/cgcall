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
DAEMON_OPTS1="--config-file $CONFIG"

NAME2=cgcall_py
PIDFILE2=/var/run/$NAME2.pid
DAEMON2=/usr/bin/python3
DAEMON_OPTS2="$DIR/scripts/get_recordings.py $CONFIG"

export PATH="${PATH:+$PATH:}/usr/sbin:/sbin:/home/pi/cgcall:"


start() {
  echo "Starting daemon: "$NAME1
  start-stop-daemon --start --make-pidfile --pidfile $PIDFILE1 --chdir $DIR --chuid pi:pi --startas /bin/bash -- -c "exec $DAEMON1 $DAEMON_OPTS1 > $DIR/log/$NAME1.log 2>&1 &"
  echo "Starting daemon: "$NAME2
  start-stop-daemon --start --make-pidfile --pidfile $PIDFILE2 --chdir $DIR --chuid pi:pi --startas /bin/bash -- -c "exec $DAEMON2 $DAEMON_OPTS2 > $DIR/log/$NAME2.log 2>&1 &"
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
  uninstall)
    uninstall
    ;;
  retart)
    stop
    start
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}"
esac