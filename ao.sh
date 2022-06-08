#!/bin/bash

# A simple script for organizing my desktop and other folders that tend to get cluttered
shopt -s nocaseglob
shopt -s globstar
#shopt -s nullglob
shopt -s extglob
shopt -s dotglob

restrict='@(img_archive)'

#ls -al > ao_ls.txt
ls -al >> ./aolog
indexname=./imgindex.csv

imgtypes={png,jpg,jpeg,webp,gif}
imt='@(png|jpg|jpeg|webp|gif)'
vidtypes='@(mov|mp4)'

S="::"
#sources="@(~/Desktop|~/Downloads|~/Desktop/January)"
sources='@(.|../Downloads|January)'
echo $sources
