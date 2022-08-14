#!/bin/bash

## Build front end
npm run build

## Either get SSH_USER environment variable for the username or default to 'sviswana' username
export SSH_USER=${SSH_USER:-sviswana}

## Rsync the `dist` directory contents
# Make sure the 'group' gets read/write permissions
# '--perms' is necessary for '--chmod' to work
rsync -avh --recursive --perms --no-times --chmod=Du=rwx,Dg=rwx,Do=rx,Fu=rw,Fg=rw,Fo=r --delete dist/ ${SSH_USER}@vm012.bridges2.psc.edu:/data/vue/
