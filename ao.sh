#!/bin/bash

# A simple script for organizing my desktop and other folders that tend to get cluttered
# I decided to name it ao(.sh) ("autoorganize"), but its functionality quickly expanded beyond organization

shopt -s nocaseglob
shopt -s globstar
shopt -s nullglob
shopt -s extglob
shopt -s dotglob

set -e

source ao_config.sh
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

file_stats() {
	stat $1 -c "{\"owner\": \"%U\", \"size\": %s, \"birth_time\": %W, \"accessed\": %X, \"modified\": %Y, \"changed\": %Z}"
#	stat $1 -c "{ owner: \"%U\", size: %s, birth_time: %W, accessed: %X, modified: %Y, changed: %Z }"
}

backup_db() {
	d="$main/ao_db_backups"
	mkdir -p $d
	p="$d/ao_db_$(date +%s).tar.gz"
	log "Backing up $dbfile to $p"
	tar cvzf $p $dbfile
}

#cp ~/Desktop/ao.sh ~/Desktop/ao

IFS=

RED='\033[0;31m'
NC='\033[0m'

rinfo=$(jo -p time=$(date +%s) args=$(echo "$@"))
#cat $dbfile | jq --argjson rinfo $rinfo 'if has("runs") then .runs += [$rinfo] else .runs = []' > $dbfile.temp
cat $dbfile | jq --argjson rinfo $rinfo '.runs += [$rinfo]' > $dbfile.temp
cp $dbfile.temp $dbfile

limit=20
dry=0
verbose=0
result=
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
	--status )
		log "Database size: $(stat -c %s $dbfile) bytes, $(wc -l < $dbfile) lines"
	;;

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

	--recursive | -r )
		log "Setting option recursive"
		recursive=1
	;;

	--rose )
		IFS=$'\n'
		r=()
		shift
		n=${1-4}
		chars=".*#@"
		for x in $(seq 1 $n); do
			t=""; for y in $(seq 1 $n); do
			z=$(( ($RANDOM%100) * (x + y) ))
			#w=$(( $(echo "${r[@]}" | sort -nr | head -n1 ) * 2 / 3 ))
			if [ $z -gt $(( 50 * n * 2 )) ];
				then t+=$([ $z -gt 900 ] && echo -en "@@" || echo -n "##"); else t+="  "; fi
				index=$(( z * ${#chars} / (100 * n * 2) ))

#				echo -en "${chars:$index:1} ";
#				then t+="${chars:$index:1}"; else t+="  "; fi
			done; r+=($(echo -en "$t"))
		done
#		echo $r
		half=$(for i in ${r[@]}; do echo -en "$i"; echo -e "$i" | rev; done)
		echo -e "$half"; echo -e "$half" | tac
#		!! | tac
	;;

	# Apply organization rules to restructure local files
	--cleanup )
		log 'Organizing'
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
		shift

		log "Processing $1"
		
		paths=()
		for p in ${restrict[@]}; do
			echo $p
			paths+=($p/**/*.$imt)
		done

		echo $verbose
		echo "Found ${#paths[@]} files; filtering"
#		paths=$(echo $p | grep -F -v -f $indexname)
		echo "Getting checksums for ${#paths[@]} files"
		if [[ $dry != 1 && $1 == images ]]
		then
			echo "fname${S}sha1${S}content" | tee -a ${indexname}
			for img in ${paths[@]:0:limit}; do
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
		mkdir $d
		echo $result | while read line; do
			echo "linking ${line}"
			ln -s $(realpath $line) $d/$(basename $line)_link
		done
		dolphin $d
	;;

	# Gather information about a directory and its contents
	--manifest | -m )
		IFS=$'\n'
		shift
		cd $1
		log "Generating directory listing of $(pwd)"
		"python3.9" -c 'import os, json; print(json.dumps(os.listdir(".")))' > "ao_listing $(date).json"
		backup_db

#		cp ao_db.json ao_db.temp.json
		if [[ $recursive == 1 ]]; then paths=(**/*.*)
		else paths=(*.*); fi

		batch='[]'
		log "Found ${#paths[@]} files"
		for f in ${paths[@]}; do
			#log "Tracking $f"
			echo "Tracking $f" > /dev/tty
			hash=$(sha1sum $f | awk '{ print $1 }')
			info=$(jo -p stats=$(file_stats $f) name=$f path=$(realpath $f) sha1=$hash time=$(date +%s))
			batch=$(echo "$batch" | jq --argjson finfo "$info" '. += [$finfo]')
		done
		echo $batch | jq '.' > ao_batch.json.temp
		cat $dbfile | jq --slurpfile b ao_batch.json.temp '.files += $b[]' > $dbfile.temp
		log "Propagating values to local database"
		cp $dbfile.temp $dbfile
#		rm ao_batch.json.temp
		log "Done"

		cd $main
	;;

	--summarize )
#		cat $dbfile | jq --arg path $1 
		shift
		backup_db
		cat $dbfile | jq "if .summaries then . else .summaries = {} end | .summaries[\"$1\"] = ($1 | {sum: add, mean: (add/length), min: min, max: max})" > $dbfile.temp
		#| tee $dbfile.temp
		cp $dbfile.temp $dbfile
		cat $dbfile | jq ".summaries[\"$1\"]"
	;;

	--update-filenodes )
		backup_db
		shift
		IFS=$'\n'
		for i in $(seq 0 $limit); do
			log "Updating snapshot $i"
	#		cat $dbfile | jq --argjson i $1 'if any(.filenodes; .path == .files[$i].path) ' > $dbfile.temp
	#		cat $dbfile | jq --argjson i $1 --arg t $(date +%s) '(if has(".filenodes") == false then .filenodes = [] else . end) | select(.filenodes[].path == .files[$i].path) as $nodes | (.files[$i] + {snapshots: [$i], time: $t}) as $fnode | if ($nodes | length) != 0 then $nodes[0] += $fnode else .filenodes += [$fnode] end' > $dbfile.temp
			cat $dbfile | jq --argjson i $i --arg t $(date +%s) 'if .files[$i].processed then . else (if .filenodes then . else (.filenodes = []) end | .files[$i].path as $p | (.files | map(.path == $p) | index(true)) as $nodes | (.files[$i] * {snapshots: [$i], time: $t}) as $fnode | if ($nodes | length) != 0 then .filenodes[$nodes] += $fnode else .filenodes += [$fnode] end | .files[$i].processed = true) end' > $dbfile.temp

			log "Propagating values to local database ($dbfile)"
			cp $dbfile.temp $dbfile
		done
	;;

	--convert )

	;;

	# Fetch a URL and archive the returned data
	--download | -d )
		keys=("starred", "repos", "followers", "following")

		for key in ${keys[@]}; do
			basepath="github/ao_request_$key $(date)"
			query=https://api.github.com/users/$github_user/$key
			if [[ $verbose == 1 ]]; then log "Querying $query"; fi
			curl $query > $basepath.json
			if [[ $compress == 1 ]]; then
				tar -czf $basepath.tar.gz $basepath.json --remove-files
			fi
			sleep $delay
		done
	;;

	# Count inputs or current selection
	--count | -c )
		echo $result | wc -l
	;;

esac; shift; done
if [[ "$1" == '--' ]]; then shift; fi

notify-send -u low "ao.sh" "ao.sh has finished executing"

#for img in **/*.$(eval echo $imgtypes); do
#	echo "${img},$(sha1sum $img)" | tee -a $indexname


# TODO: store triggers that run command/function on event
