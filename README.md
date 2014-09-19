HOWTO: Simple Monitoring on Arduino Yún 
=======================================

I wrote this little howto as a number of people are having issues with basic WWW functionality on the Arduino Yún

The intention is to give a simple introduction to the setting up some nice monitoring tools on the device and exposing them on the WWW page.

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
__________________

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

Display some results
--------------------

Collectd doesn't have any output features, but there is a very simple tool "rrdcgi" which can output graphs from the rrd databases collectd creates.

That tool uses a "cgi-bin" file (example in this GIT repo) which creates simple HTML pages with graphs in. 

Drop the _.cgi_ file into the /www/cgi-bin directory on the Arduino Yun






