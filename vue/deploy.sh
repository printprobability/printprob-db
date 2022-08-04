#!/bin/bash

npm run build
rsync -avh --recursive --perms --chmod=Du=rwx,Dg=rwx,Do=rx,Fu=rw,Fg=rw,Fo=r dist/ vm01
2.bridges2.psc.edu:/data/vue/
