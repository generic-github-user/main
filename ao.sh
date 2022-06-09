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

#IFS=$'\n'
# why do these need to be quoted?
for img in "$sources"/*."$imt"; do
	mv -nv $img ./img_archive | tee -a ./aolog
done

mkdir -p aoarchive; [ aosearch* ] && mv -nv aosearch* ./aoarchive
mkdir -p textlike; [ ./*.txt ] && mv -nv ./*.txt textlike
mkdir -p vid_archive; [ "$sources"/*."$vidtypes" ] && mv -nv "$sources"/*."$vidtypes" vid_archive

cp ~/Desktop/ao.sh ~/Desktop/ao

tst={private,dht}
#echo **/*.${tst}
#for img in $(eval echo "**/*.$imgtypes"); do
paths=($restrict/**/*.$imt)
IFS=

limit=20
result=
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
	--dry )
		dry=1
	;;
	--verbose | v )
		verbose=1
	;;
	--open | -o )
		shift
		echo "Displaying results"
		d="./aosearch ($(date))"
		#mkdir $d; ln -s $result $d/$
		mkdir $d
		#cat $result | while read line; do
		#while LANG=C IFS= read line; do
		echo $result | while read line; do
			echo "linking ${line}"
			ln -s $(realpath $line) $d/$(basename $line)_link
		#done < $result
		done
		dolphin $d
	;;
esac; shift; done
if [[ "$1" == '--' ]]; then shift; fi

#for img in **/*.$(eval echo $imgtypes); do
#	echo "${img},$(sha1sum $img)" | tee -a $indexname

