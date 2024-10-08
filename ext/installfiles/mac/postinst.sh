#!/bin/bash

export PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin

cd "/Library/Application Support/BackOne"

if [ ! -f authtoken.secret ]; then
	head -c 1024 /dev/urandom | md5 | head -c 24 >authtoken.secret
	chown 0 authtoken.secret
	chgrp 0 authtoken.secret
	chmod 0600 authtoken.secret
fi

if [ -f backone.pid ]; then
	kill `cat backone.pid`
	sleep 1
	killall MacEthernetTapAgent
	sleep 1
	killall -9 MacEthernetTapAgent
	sleep 1
	if [ -f backone.pid ]; then
		kill -9 `cat backone.pid`
		rm -f backone.pid
	fi
fi
launchctl load /Library/LaunchDaemons/com.backone.plist >>/dev/null 2>&1
sleep 1

rm -f backone-cli backone-idtool
ln -sf backone backone-cli
ln -sf backone backone-idtool
if [ ! -d /usr/local/bin ]; then
	mkdir -p /usr/local/bin
fi
cd /usr/local/bin
rm -f backone-cli backone-idtool
ln -sf "/Library/Application Support/BackOne/backone" backone-cli
ln -sf "/Library/Application Support/BackOne/backone" backone-idtool

if [ -f /tmp/zt1-gui-restart.tmp ]; then
	for u in `cat /tmp/zt1-gui-restart.tmp`; do
		if [ -f '/Applications/BackOne.app/Contents/MacOS/BackOne' ]; then
			su $u -c '/usr/bin/open /Applications/BackOne.app &' >>/dev/null 2>&1 &
		else
			su $u -c '/usr/bin/open /Applications/BackOne.app &' >>/dev/null 2>&1 &
		fi
	done
fi
rm -f /tmp/zt1-gui-restart.tmp

exit 0
