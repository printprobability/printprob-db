#!/bin/bash

# anon_12037841_196602_53height_modestandbrotherly

PP_TOKEN=`cat ~/token.txt`

# Generate list of page files to download
cd /pylon5/hm560ip/mpwillia/line_extractions/complete/$1
find pages/ -regextype posix-extended -regex '.+([0-9]{3}|r)\.tif' > ~/imagefiles.txt
cd ~

rsync -avh --files-from ~/imagefiles.txt /pylon5/hm560ip/mpwillia/line_extractions/complete/$1/ bridges@printprobdb.library.cmu.edu:/vol/images/mpwillia/line_extractions/complete/$1/

python3 backlog.py -e https://printprobdb.library.cmu.edu/api/ -t $PP_TOKEN -r /pylon5/hm560ip/ $1
