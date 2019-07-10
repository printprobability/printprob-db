#!/bin/bash
find . -name "*.tif" | parallel -j2 convert {} -set filename:f '%d/%t' -units PixelsPerInch -density 72 -quality 60 -resize 2000 '%[filename:f].jpg'
