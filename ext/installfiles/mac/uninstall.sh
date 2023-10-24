#!/bin/bash

export PATH=/bin:/usr/bin:/sbin:/usr/sbin

if [ "$UID" -ne 0 ]; then
	echo "Must be run as root; try: sudo $0"
	exit 1
fi

if [ ! -f '/Library/LaunchDaemons/com.backone.plist' ]; then
	echo 'BackOne does not seem to be installed.'
	exit 1
fi

cd /

echo 'Stopping any running BackOne service...'
launchctl unload '/Library/LaunchDaemons/com.backone.plist' >>/dev/null 2>&1
sleep 1
killall -TERM backone >>/dev/null 2>&1
sleep 1
killall -KILL backone >>/dev/null 2>&1

echo "Removing BackOne files..."

rm -rf '/Applications/BackOne.app'
#rm -rf '/Applications/ZeroTier.app'
rm -f '/usr/local/bin/backone' '/usr/local/bin/backone-idtool' '/usr/local/bin/backone-cli' '/Library/LaunchDaemons/com.backone.plist'

cd '/Library/Application Support/BackOne'
if [ "`pwd`" = '/Library/Application Support/BackOne' ]; then
	rm -rf *.d *.sh *.log *.old *.kext *.conf *.pkg *.dmg *.pid *.port *.save *.bin planet backone-* devicemap
fi

echo 'Uninstall complete.'
echo
echo 'Your identity and secret authentication token have been preserved in:'
echo '  /Library/Application Support/BackOne'
echo
echo 'You can delete this folder and its contents if you do not intend to re-use'
echo 'them.'
echo

exit 0
