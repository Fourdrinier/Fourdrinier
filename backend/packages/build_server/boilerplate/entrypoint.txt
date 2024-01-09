#!/bin/bash

allocated_ram=$1
mv /downloads/* /minecraft/mods/
java -Xmx$allocated_ram -jar /minecraft/server.jar nogui