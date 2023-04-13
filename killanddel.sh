#!/usr/bin/env bash
#
# Script to kill a download, and delete the interim files associated with it.
# Should be run in the same directory as the download is occuring to.
#
# Requires a parameter to identify the file being downloaded (usually a 
# number or code just before the .mp4 part of the filename

# Check we have a code:
if [ "XX"$1 == "XX" ] ; then
	echo "No parameters"
	exit 0
fi

# Check the file is being downloaded, and there's only one:
if [ -f *${1}.mp4.part  ] ; then
	echo "Killing and deleting code $1"
else
	echo "No part file found with code $1"
	exit 1
fi

# First kill the process
echo "Killing process..."
kill $(ps aux | grep $1 | grep dl | grep -v grep | awk -- '{ print $2 }')
echo "Cleaning files:"
rm -v *${1}.mp4.*

