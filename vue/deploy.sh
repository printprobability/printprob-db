#!/bin/bash

npm run build
rsync -avh --delete dist/ vm012.bridges2.psc.edu:/data/vue/