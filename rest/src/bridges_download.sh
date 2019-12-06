#!/bin/bash

# anon_12037841_196602_53height_modestandbrotherly

# Generate list of page files to download
ssh bridges.psc.edu "cd /pylon5/hm560ip/mpwillia/line_extractions/complete/$1 && find pages/ -regextype posix-extended -regex '.+([0-9]{3}|r)\.tif'" > imagefiles.txt

rsync -avh --files-from imagefiles.txt bridges.psc.edu:/pylon5/hm560ip/mpwillia/line_extractions/complete/$1/ /Users/mlincoln/Development/printprobability/pp-images/mpwillia/line_extractions/complete/$1/

rsync -avh bridges.psc.edu:/pylon5/hm560ip/srijhwan/broken_type_new/output_$1 /Users/mlincoln/Development/printprobability/pp-images/srijhwan/broken_type_new/.
