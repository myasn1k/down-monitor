#!/bin/bash

MUTEX="/tmp/down-monitor-mutex"

if test -f $MUTEX;
then
	exit
else
	touch $MUTEX
	/usr/local/bin/docker-compose up --abort-on-container-exit
	rm $MUTEX
fi
