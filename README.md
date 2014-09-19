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

Now a small amount of configuration is needed.





