# scripts-config
Scripts and config for desktop use

## aliases

Some useful aliases too short to make into their own scripts:

### audioreset

Resets the audio on my HP Z440 after returning from sleep so it comes from the USB device.

### fixlinks

Fixes all the links in a "links" file pointing to SBS on demand, so the download file is correct. Deprecated by `fetch-sbs.py`.

### mplayer

Just some useful config params for mplayer

## fetch-sbs.py

Script to fetch a video file from an SBS on demand URL, and prettify the resultant filename. Also optionally moves it into a subdirectory like "Series Name/Season xx".

Requires an updated sbs.py download helper for yt-dlp.

Use with a links file containing a list of SBS download links, and xjobs to parallelise:

```bash
cat links | xjobs -j3 -- fetch-sbs.py -q -m
```

## fix-sbs.sh

Fixes the filename of an sbs file as downloaded, to remove cruft from the end and move into subdirectory. Deprecated by the above.

## killanddel.sh

Script to kill an ongoing youtube-dl process, and cleanup the temporary files generated. Relies on the downloaded file have some unique identifier just before the `.mp4` output, which is passed to the script as the parameter.

## warmswap.sh

Resets & rescans the SATA bus so when your motherboard doesn't support hotswapping, you can still use hotswap bays without rebooting.

