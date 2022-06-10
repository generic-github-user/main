#!/bin/bash

# A simple script for organizing my desktop and other folders that tend to get cluttered
shopt -s nocaseglob
shopt -s globstar
shopt -s nullglob
shopt -s extglob
shopt -s dotglob

restrict='@(img_archive)'

#ls -al > ao_ls.txt
ls -al >> ./aolog
indexname=./imgindex.csv

imgtypes={png,jpg,jpeg,webp,gif}
imt='@(png|jpg|jpeg|webp|gif)'
vidtypes='@(mov|mp4)'
IFS=$'\n'

S="::"
#sources="@(~/Desktop|~/Downloads|~/Desktop/January)"
#sources='@(.|/home/alex/Downloads|January)'

main=$HOME/Desktop
sources="$HOME/@(Downloads|Desktop)"
echo $sources

log() {
	echo $1 | tee -a aolog
}

group_ftype() {
	for arg in "$@"; do
		log "Grouping $sources/*.$1"
		mkdir -p ${arg}s
		[[ $sources/*.$arg ]] && mv -nv $sources/*.$arg ${arg}s | tee -a aolog
	done
}

log Organizing
printf "%s\n" $sources

# why do these need to be quoted?
for img in $sources/*.$imt; do
	mv -nv $img ./img_archive | tee -a ./aolog
done

mkdir -p aoarchive; [ aosearch* ] && mv -nv aosearch* ./aoarchive
mkdir -p textlike; [ ./*.txt ] && mv -nv ./*.txt textlike
mkdir -p vid_archive; [ "$sources"/*."$vidtypes" ] && mv -nv "$sources"/*."$vidtypes" vid_archive
group_ftype pdf pgn dht docx ipynb pptx

cp ~/Desktop/ao.sh ~/Desktop/ao

tst={private,dht}
#echo **/*.${tst}
#for img in $(eval echo "**/*.$imgtypes"); do
paths=($restrict/**/*.$imt)
IFS=

limit=20
dry=0
verbose=0
result=
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
	--dry )
		dry=1
	;;
	--verbose | -v )
		verbose=1
	;;
	--process )
		echo $verbose
		echo "Found ${#paths[@]} files; filtering"
#		p=$(printf "%s\n" ${paths[@]})
#		paths=$(echo $p | grep -F -v -f $indexname)
		echo "Getting checksums for ${#paths[@]} files"
		if [[ $dry != 1 ]]
		then
			echo "fname${S}sha1${S}content" | tee -a ${indexname}
			for img in ${paths[@]:0:limit}; do
				checksum=$(sha1sum $img)
				if [[ $verbose == 1 ]]; then
					echo $img
					echo $checksum
				fi
				if ! $(grep -qF $checksum $indexname); then
					echo "$img$S\
						$checksum$S\
						$(tesseract $img stdout | tr -d '\n')" >> $indexname
				#| tee -a "$indexname"
				#echo $info | tee -a $indexname
					# TODO
					# echo $info | cut -c1-50 | echo
					#$info >> $indexname
				elif [[ $verbose == 1 ]]; then
					echo "Already processed"
				fi
				if [[ $verbose == 1 ]]; then echo $'\n'; fi
			done
		fi
		exit
	;;
	--limit | -l )
		shift; limit=$1
	;;
	--imfind )
		shift; target=$1
#		echo "Searching for $target"
		# Based on https://unix.stackexchange.com/a/527499
		result=$(awk -v T="$target" -F $S '{ if ($3 ~ T) { print $1 } }' $indexname)
		echo $result
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


# TODO: store triggers that run command/function on event
