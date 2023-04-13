#!/usr/bin/env python
"""
Script for fetching from SBS On Demand. Necessary since they changed the way they deliver the
output file, and the input URL is not simple any more.
"""

# Standard Library imports go here
import argparse
import logging
import sys
import os

import subprocess

# External library imports go here
#
# Standard Library from-style imports go here
from pathlib import Path

# External library from-style imports go here
#
# Ideally we all live in a unicode world, but if you have to use something
# else, you can set it here
ENCODE_IN = 'utf-8'
ENCODE_OUT = 'utf-8'

# Set up a global logger. Logging is a decent exception to the no-globals rule.
# We want to use the logger because it sends to standard error, and we might
# need to use the standard output for, well, output. We'll set the name of the
# logger to the name of the file (sans extension).
log = logging.getLogger(Path(__file__).stem)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('baseurl', help="The URL to fetch")
    parser.add_argument('-v', '--verbose', 
                           help="Display verbose messages from this program",
                           action='store_true')
    parser.add_argument('-q', '--quiet', 
                           help="Pass through the 'quiet' parameter to yt-dlp",
                           action='store_true')
    parser.add_argument('-m', '--move', 
                           help="Move into sub-dirs after downloading",
                           action='store_true')

    return parser.parse_args()

def main():
    args = parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    exe = "yt-dlp"
    logging.debug("Using yt-dlp executable")

    if args.quiet:
        exeparams = "-q"
    else:
        exeparams = ""

    # Sanity check that we have passed in a "correct" URL:
    logging.debug(f"Baseurl: {args.baseurl}")
    
    urlparts = args.baseurl.split("/")
    logging.debug(f"URLParts: {urlparts}")
    if urlparts[0] != "https:":
        logging.info("Bad URL - must start with 'https'")
        exit(1)
    if urlparts[2] != "www.sbs.com.au":
        logging.info("Bad URL - domain must be sbs.com.au")
        exit(1)
    if urlparts[3] != "ondemand":
        logging.info("Bad URL - expected to be from SBS 'ondemand'")
        exit(1)
    # magicnum is the unique part of the sbs download URL at the end
    # https://www.sbs.com.au/ondemand/watch/$magicnum
    magicnum = urlparts[-1]
    # fullname is the full name of the episode, in the format "<series>-sx-epy"
    fullname = urlparts[-2].split('-')
    logging.debug(f"Full URL name: {fullname}")
    # Check if the series is correct format:
    try:
        if fullname[-2][0].lower() != 's':
            logging.warning(f"Series string not in correct format, not a series")
            series = None
        else:
            series = int(fullname[-2][1:])
            logging.debug(f"Series is {series}")
        if fullname[-1][0:2].lower() != "ep":
            logging.warning(f"Episode string not in correct format, not an episode")
            episode = None
        else:
            episode = int(fullname[-1][2:])
            logging.debug(f"Episode is {episode}")
    except IndexError: # Not a series
        series = None
        episode = None

    downloadurl = "https://www.sbs.com.au/ondemand/watch/" + magicnum
    logging.debug(f"Download URL: {downloadurl}")
    logging.debug("Starting Download")
    cp = subprocess.run([exe, exeparams, downloadurl])
    if cp.returncode != 0:
        logging.info(f"{exe} returned non zero return code: {cp.returncode}")
        # But we push on anyway, because it's probably not fatal...
        # exit(cp.returncode)
    else:
        logging.debug(f"{exe} exited successfully")
    # Now rename the downloaded file to match the original SBS schema:
    logging.debug("Renaming file to match old SBS Schema")
    fnames = [_ for _ in Path('.').glob(f'*{magicnum}*.mp4')]
    if len(fnames) != 1:
        logging.info("Can't determine filename uniquely - aborting")
        exit(1)
    else:
        fname = fnames[0]
        logging.debug(f"Downloaded file: {fname}")
    fnamebase = str(fname).split('[')[0].strip()
    if series is not None:
        newname = f"{fnamebase} S{series:02d}E{episode:02d}.mp4"
    else:
        newname = f"{fnamebase}.mp4"
    logging.debug(f"Renaming {fname} to {newname}")
    os.rename(fname, newname)

    if(args.move):
        destdir = f"{fnamebase.strip()}/Season {series:02d}"
        try:
            os.makedirs(destdir)
            logging.debug(f"Creating dir {destdir}")
        except OSError:
            pass
        logging.debug(f"Moving {newname} into {destdir}")
        os.rename(newname, destdir + "/" + newname)

if __name__ == "__main__":
    main()
