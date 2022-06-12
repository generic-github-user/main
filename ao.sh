#!/bin/bash

# A simple script for organizing my desktop and other folders that tend to get cluttered
shopt -s nocaseglob
shopt -s globstar
shopt -s nullglob
shopt -s extglob
shopt -s dotglob

main=$HOME/Desktop
cd $main
restrict=("$HOME/Desktop/img_archive" "$HOME/Pictures")
echo $restrict

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
cp ~/Desktop/ao.sh ~/Desktop/ao

tst={private,dht}
#echo **/*.${tst}
#for img in $(eval echo "**/*.$imgtypes"); do
IFS=

limit=20
dry=0
verbose=0
result=
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
	# Execute a "dry run"; don't modify any files
	--dry )
		dry=1
	;;

	# Print additional information about what the program is doing
	--verbose | -v )
		verbose=1
	;;

	# Compress saved files into .tar.gz archives
	-z )
		compress=1
	;;

	--rose )
		IFS=$'\n'
		r=()
		shift
		n=${1-4}
		chars="#@"
		for x in $(seq 1 $n); do
			t=""; for y in $(seq 1 $n); do
			z=$(( ($RANDOM%100) * (x + y) ))
			if [ $z -gt 500 ]; then t+=$([ $z -gt 900 ] && echo -en "@@" || echo -n "##"); else t+="  "; fi
			done; r+=($(echo -n $t))
		done
#		echo $r
		half=$(for i in ${r[@]}; do echo -n $i; echo $i | rev; done)
		echo "$half"; echo "$half" | tac
#		!! | tac
	;;

	# Apply organization rules to restructure local files
	--cleanup )
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
	;;

	# Extract data from files to build databases
	--process )
		echo "Processing"
		paths=()
		for p in ${restrict[@]}; do
			echo $p
			paths+=($p/**/*.$imt)
		done

		echo $verbose
		echo "Found ${#paths[@]} files; filtering"
#		p=$(printf "%s\n" ${paths[@]})
#		paths=$(echo $p | grep -F -v -f $indexname)
		echo "Getting checksums for ${#paths[@]} files"
		if [[ $dry != 1 ]]
		then
			echo "fname${S}sha1${S}content" | tee -a ${indexname}
			for img in ${paths[@]:0:limit}; do
#				checksum=($(sha1sum ${img}))
				checksum=$(sha1sum $img | awk '{ print $1 }')
				if [[ $verbose == 1 ]]; then
					echo $img
					echo ${checksum}
					#echo $'\n'
				fi
				if ! $(grep -qF ${checksum} $indexname); then
					echo "$img$S\
						${checksum}$S\
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
		elif [[ $1 == text ]]; then
			# is there a nicer way to do this (implicit looping)?
			for t in ./*.$text_types; do
#				hash=($(sha1sum $t))
#				TODO: backup ao database
				hash=$(sha1sum $t | awk '{ print $1 }')
				log "Getting stats for $t"
				cat $dbfile | jq --arg name $t --arg path $(realpath $t) --arg h $hash --arg category text --arg lines $(wc -l < $t) --arg chars $(wc -m < $t) --arg words $(wc -w < $t) '.files += [{"name": $name, "path": $path, "sha1": $h, "category": $category, "lines": $lines|tonumber, "chars": $chars|tonumber, "words": $words|tonumber}]' > $dbfile
			done
		fi
		exit
	;;

	# Limit the number of results an action returns
	--limit | -l )
		shift; limit=$1
	;;

	# Find images containing the specified text
	--imfind )
		shift; target=$1
		echo "Searching for $target"
		# Based on https://unix.stackexchange.com/a/527499
		result=$(awk -v T="$target" -F $S '{ if ($3 ~ T) { print $1 } }' $indexname)
		echo $result
	;;

	# Open the selection by creating a temporary directory with symlinks to its files
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

	# Gather information about a directory and its contents
	--manifest | -m )
		shift
		cd $1
		echo "Generating directory listing of $(pwd)"
		python3.9 -c 'import os, json; print(json.dumps(os.listdir(".")))' > "ao_listing $(date).json"
		cd $main
	;;

	# Fetch a URL and archive the returned data
	--download | -d )
		keys=("starred", "repos", "followers", "following")

		for key in ${keys[@]}; do
			basepath="github/ao_request_$key $(date)"
			curl https://api.github.com/users/$github_user/$key > $basepath.json
			if [[ $compress == 1 ]]; then
				tar -czf $basepath.tar.gz $basepath.json --remove-files
			fi
		done
	;;

	# Count inputs or current selection
	--count | -c )
		echo $result | wc -l
	;;

esac; shift; done
if [[ "$1" == '--' ]]; then shift; fi

#for img in **/*.$(eval echo $imgtypes); do
#	echo "${img},$(sha1sum $img)" | tee -a $indexname


# TODO: store triggers that run command/function on event
