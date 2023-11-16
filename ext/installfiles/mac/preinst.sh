#!/bin/bash

export PATH=/bin:/usr/bin:/sbin:/usr/sbin

rm -f /tmp/zt1-gui-restart.tmp
for i in `ps axuwww | tr -s ' ' ',' | grep -F '/Applications/BackOne.app' | grep -F -v grep | cut -d , -f 1,2 | xargs`; do
	u=`echo $i | cut -d , -f 1`
	p=`echo $i | cut -d , -f 2`
	if [ ! -z "$u" -a "0$p" -gt 0 ]; then
		kill $p >>/dev/null 2>&1
		sleep 0.5
		kill -9 $p >>/dev/null 2>&1
		echo "$u" >>/tmp/zt1-gui-restart.tmp
	fi
done
for i in `ps axuwww | tr -s ' ' ',' | grep -F '/Applications/BackOne.app' | grep -F -v grep | cut -d , -f 1,2 | xargs`; do
	u=`echo $i | cut -d , -f 1`
	p=`echo $i | cut -d , -f 2`
	if [ ! -z "$u" -a "0$p" -gt 0 ]; then
		kill $p >>/dev/null 2>&1
		sleep 0.5
		kill -9 $p >>/dev/null 2>&1
		echo "$u" >>/tmp/zt1-gui-restart.tmp
	fi
done
chmod 0600 /tmp/zt1-gui-restart.tmp

cd "/Applications"
rm -rf "BackOne.app"
rm -rf "BackOne.app"

if [ -d '/Library/Application Support/BackOne' ]; then
	cd '/Library/Application Support/BackOne'
	# ensure that file locking doesn't cause issues with replacing the binary
	rm -f backone
	rm -f MacEthernetTapAgent
fi

exit 0
