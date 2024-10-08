#!/bin/bash
export PATH="/Library/Application Support/BackOne:/bin:/usr/bin:/sbin:/usr/sbin"
/usr/bin/killall MacEthernetTapAgent >>/dev/null 2>&1
exec backone
