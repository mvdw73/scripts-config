#!/usr/bin/env bash
#
# Script to warm-swap disks in 3-bay enclosure. Will rescan the SATA bus
# since the controller doesn't appear to support direct hot-swapping.
#
# Need to run this every time disks are inserted/removed.
#
# Needs to be run as root, but we don't check for that as it will just 
# fail with permission denied.
#
for i in 1 2 3 4 5 6 ; do
	echo "0 0 0" > /sys/class/scsi_host/host${i}/scan
done

