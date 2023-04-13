#!/usr/bin/env bash

# Script to change a single SBS filename of the form "foo - Sx Epy-<random>.mp4" into "foo - SxxEyy.mp4"

# Takes a single filename and returns the new filename.
ls *.mp4 | while read f ; do 
	mv -v "$f" "$(echo $f | \
		sed -e 's/-[a-zA-Z0-9_,]*.mp4/.mp4/g' | \
		sed -E 's/S([1-9]) /S0\1/g' | \
		sed -E 's/ Ep([1-9])/Ep\1/g' | \
		sed -E 's/Ep([1-9][ .])/E0\1/g' | \
		sed -E 's/Ep([1-9][0-9][ .])/E\1/g')"
	done

for f in *.mp4 ; do 
	DIR="$(echo "$f" | sed -- "s_ S0\([0-9]\)[- 0-9a-zA-Z\',\!]*.mp4_/Season \1_g")"
	if $(echo $DIR | grep .mp4) ; then
		echo "$DIR contains mp4"
	else
		mkdir -p "$DIR"
		mv -v "$f" "$DIR"
	fi
done

