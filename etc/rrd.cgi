#!/usr/bin/rrdcgi
<HTML>
<HEAD><TITLE>Reptile House</TITLE></HEAD>
<BODY>
<H1>Reptile House</H1>
<P>
<RRD::GRAPH
 --imginfo '<IMG SRC=/sd/%s WIDTH=%lu HEIGHT=%lu >'
 /www/sd/memory.png --lazy --title="Memory" 
 DEF:free=/mnt/sda1/data/collectd/rrd/Arduino/memory/memory-free.rrd:value:AVERAGE 
 DEF:used=/mnt/sda1/data/collectd/rrd/Arduino/memory/memory-used.rrd:value:AVERAGE 
 LINE2:free#00a000:"Free"
 LINE2:used#0000a0:"Used"
 >
 
<RRD::GRAPH
  --imginfo '<IMG SRC=/sd/%s WIDTH=%lu HEIGHT=%lu>'
  /www/sd/df.png --lazy --title="Disk Free"
  DEF:sda1=/mnt/sda1/data/collectd/rrd/Arduino/df/df-mnt-sda1.rrd:free:AVERAGE
  LINE2:sda1#00a000:"sda1"
  >
</P>
</BODY>
</HTML>
