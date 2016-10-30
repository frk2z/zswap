#!/bin/sh
cp zswap.py /usr/local/bin/zswap
if [ -e /usr/local/bin/zswap ]
then
	echo zswap.py copied to /usr/local/bin/zswap
	if [ ! -x /usr/local/bin/zswap ]
	then
		chmod +x /usr/local/bin/zswap
	fi
else
	echo Unable to copy zswap.py to /usr/local/bin/zswap
fi
