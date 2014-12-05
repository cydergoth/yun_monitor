#!/bin/sh
HOSTNAME="${COLLECTD_HOSTNAME:-localhost}"
INTERVAL="${COLLECTD_INTERVAL:-60}"
  
while sleep "$INTERVAL"; do
     curl -q http://localhost/arduino/onewire/x 2>/dev/null | awk -F "," -v host=$HOSTNAME -v iv=$INTERVAL  'NR > 1 { printf "PUTVAL \"%s/temp/temp-%s\" interval=%s N:%s\n",host,$1,iv,$3 } '
done
