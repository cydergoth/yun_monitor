HOWTO: Simple Monitoring on Arduino Yún 
=======================================

I wrote this little howto as a number of people are having issues with basic WWW functionality on the Arduino Yún

The intention is to give a simple introduction to the setting up some nice monitoring tools on the device and exposing them on the WWW page.

Example
-------
![Sample Image](https://github.com/cydergoth/yun_monitor/blob/master/example/Reptile%20House_files/memory.png)

Parition Arduino Yún SD
-----------------------

The Arduino Yún usually is paired with an SD card to expand the on-board storage space. This card is best setup with the partioning sketch from http://arduino.cc/en/Tutorial/ExpandingYunDiskSpace

Note that the Arduino should be connected to the host computer running the IDE via USB, and also configured to connect to the Internet via Wifi or Ethernet cable. After that just follow the instructions in the above tutorial to partition your SD card.

Install required software
-------------------------

Log into your Yún via SSH and run the following commands:

    root@Arduino:~# opkg update
    root@Arduino:~# opkg install collectd collectd-mod-df collectd-mod-exec collectd-mod-memory collectd-mod-rrdtool rrdcgi1 rrdtool1

This will install the CollectD statistics engine and the RRD "Round Robin Database" engine used to store the collected data.

Configure Collectd
------------------

Now a small amount of configuration is needed.

The collectd config file example for this HOWTO is located in this GIT repository. Drop it into the /etc/ directory of the Arduino Yun overwriting the one there, or modify the existing one to match.

Important parts to note are:

### Plugins 

    #LoadPlugin cpu
    LoadPlugin df
    #LoadPlugin disk
    #LoadPlugin interface
    #LoadPlugin load
    LoadPlugin memory
    #LoadPlugin network
    #LoadPlugin ping
    #LoadPlugin processes
    LoadPlugin rrdtool
    #LoadPlugin serial
    #LoadPlugin wireless
    
This section contains the three plugins we shall be enabling : df, memory and rrdtool. There are two types of plugin in collectd, input plugins and output plugins. The first two are input plugins and rrdtool is the output plugin. Usually you have many input plugins and only one output plugin. The other plugins are commented out ('#') and will be ignored.

### Output Configuration

Each plugin may have some configuration but for now we'll only configure the output plugin and use defaults for the others

    <Plugin rrdtool>
           DataDir "/mnt/sda1/data/collectd/rrd"
           CacheTimeout 120
           CacheFlush   900
    </Plugin>
    
Here we are telling collectd to store the output to the first (FAT16/32) partition of the SD card.

Start the collectd service
--------------------------

Before collectd will collect anything, you need to enable and start the collectd service

    root@Arduino:/# /etc/init.d/collectd enable
    root@Arduino:/# /etc/init.d/collectd start

Enabling the service ensures that it will start on future boots

Display some results
--------------------

Collectd doesn't have any output features, but there is a very simple tool "rrdcgi" which can output graphs from the rrd databases collectd creates.

That tool uses a ["cgi-bin" file] (https://github.com/cydergoth/yun_monitor/blob/master/cgi-bin/rrd.cgi) which creates simple HTML pages with graphs in. 

Drop the _.cgi_ file into the /www/cgi-bin directory on the Arduino Yun. You should make it executable with

    root@Arduino:/www/cgi-bin#  chmod +x rrd.cgi

Lets take a closer look at this file:

    #!/usr/bin/rrdcgi
    
This line tells the WWW browser to use the rrdcgi tool to interpret this file

    <HTML>
    <HEAD><TITLE>Reptile House</TITLE></HEAD>
    <BODY>
    <H1>Reptile House</H1>
    <P>
    
These lines are the standard HTML webpage introduction for a basic WWW page (no DTD, no CSS). ("Reptile House" is where this Yun will be controlling the temperatures)

    <RRD::GRAPH
       --imginfo '<IMG SRC=/sd/%s WIDTH=%lu HEIGHT=%lu >'
       
This line introduces a graph for RRD which will be accessed by the /sd/ url base path and have the smae name as in the next line

       /www/sd/memory.png --lazy --title="Memory" 
       
This line defines the file system location of the image file for the graph and the title. The "--lazy" option instructs rrcgi not to redraw the graph unless it needs to

       DEF:free=/mnt/sda1/data/collectd/rrd/Arduino/memory/memory-free.rrd:value:AVERAGE 
       DEF:used=/mnt/sda1/data/collectd/rrd/Arduino/memory/memory-used.rrd:value:AVERAGE 

Now we define two data streams for the graph

       LINE2:free#00a000:"Free"
       LINE2:used#0000a0:"Used"
       >
    
Finally we tell rrdcgi to draw two lines on the graph with the specified colors and legends. The "rrdcgi" tool supports a few more options, see the documentation on it for more details (http://manpages.ubuntu.com/manpages/hardy/man1/rrdcgi.1.html)

Note that we are using the rrdcgi1 module as we don't need any more sophisticated features

    <RRD::GRAPH
      --imginfo '<IMG SRC=/sd/%s WIDTH=%lu HEIGHT=%lu>'
      /www/sd/df.png --lazy --title="Disk Free"
      DEF:sda1=/mnt/sda1/data/collectd/rrd/Arduino/df/df-mnt-sda1.rrd:free:AVERAGE
      LINE2:sda1#00a000:"sda1"
      >
      
Now we have a second graph for the free disk space. Note: You can use "rrdtool info <file>" to see what the data streams inside the ".rrd" files are called. In the first graph there are two streams in different files both called "value", wheras the second graph refers to a steam called "free" - one of several in the same file. 

    </P>
    </BODY>
    </HTML>

Finally finishing with the standard HTML close tags.

Seeing the results
------------------

After giving it some time to collect data, say a few hours, see the results by going to

    http://192.168.0.14/cgi-bin/rrd.cgi 
    
(Replace 192.168.0.14 with the URL of your Arduino Yun on your local net. Note: don't use /arduino, that is for the bridge REST service)

