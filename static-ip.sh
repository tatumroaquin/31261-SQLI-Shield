#!/bin/bash
config=/etc/dhcpcd.conf

rule="source-directory\s\/etc\/network\/interfaces.d"

case $1 in
   on)
   sudo echo "iface wlan0 inet static
   address 192.168.0.105
   netmask 255.255.255.0
   gateway 192.168.0.1" >> $config
      ;;
   off)
      sudo cp $config temp.txt
      sudo head -n -4 temp.txt > $config
      sudo rm temp.txt
esac
