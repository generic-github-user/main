#!/bin/bash

# A simple script for organizing my desktop and other folders that
# tend to get cluttered

# I decided to name it ao(.sh) ("autoorganize"), but its
# functionality quickly expanded beyond organization

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

imgtypes={png,jpg,jpeg,webp,gif}
imt='@(png|jpg|jpeg|webp|gif)'
vidtypes='@(mov|mp4)'
IFS=$'\n'

S="::"
#sources="@(~/Desktop|~/Downloads|~/Desktop/January)"
#sources='@(.|/home/alex/Downloads|January)'

sources="$HOME/@(Downloads|Desktop)"

# Output a message to stdout and the log file
log() {
	echo "$1" | tee -a aolog
}

# Group files by their extension(s)
group_ftype() {
	echo "$@"
	IFS=$' \t\n'
	for arg in "$@"; do
		#log "Grouping $sources/*.$arg"
		log "Grouping *.$arg"
		mkdir -p group/${arg}s
		#[ "$sources/*.$arg" ] && mv -nv $sources/*.$arg group/${arg}s | tee -a aolog
		[[ $(echo $sources/*.$arg) ]] && mv -nv $sources/*.$arg group/${arg}s | tee -a ./aolog
	done
}

# Generate a JSON object with information about the specified file
# or directory
file_stats() {
	stat $1 -c "{\"owner\": \"%U\", \"size\": %s, \"birth_time\": %W, \"accessed\": %X, \"modified\": %Y, \"changed\": %Z}"
#	stat $1 -c "{ owner: \"%U\", size: %s, birth_time: %W, accessed: %X, modified: %Y, changed: %Z }"
}

# A stopgap to mitigate any severe mistakes I make before the more
# comprehensive backup system is ready
backup_db() {
	d="$main/ao_db_backups"
	mkdir -p $d
	p="$d/ao_db_$(date +%s).tar.gz"
	log "Backing up $dbfile to $p"
	tar cvzf $p $dbfile
}

# Send a database to standard input
read_db() {
	cat $dbfile
}

# Store standard input in the specified database
write_db() {
	log "Propagating values to local database ($1)"
	cat - > $1.temp
	cp $1.temp $1
	log "Done"
}

# Safely rename/move file, appending a number if the name conflicts
# with an existing file
move() {
	t=$2
	if [[ -e $t ]]; then
		t="${2%.*}_$(date +%s%3N).${2##*.}"
		log "$2 already exists, renaming to $t"
	fi
	mv -nv "$1" "$t" | tee -a ./aolog
}

# Display documentation from a JSON object specifying information
# about a function or command
pdocs() {
	#read v
	v=$(</dev/stdin)
	tput setaf 1
	#echo -n "$v" | jq -rj '.name'
	printf '%10s   ' $(echo -n "$v" | jq -rj '.name')
	tput setaf 2
	printf '%10s   ' $(echo -n "$v" | jq -rj '.returntype')
	tput sgr0
	#echo -n "$v" | jq -r '.info'
	printf '%s\n' $(echo -n "$v" | jq -r '.info')
	params=$(echo -n "$v" | jq -c '.params[]')
	if [[ ! "$params" ]]; then
		repeat ' ' 12;
		echo -n 'No parameters'
	fi
	echo $params | while read p; do
		tput setaf 3; repeat ' ' 12; printf '%10s    ' $(echo -n $p | jq -rj '.name'); tput sgr0
		tput setaf 2; printf '%-20s    ' $(echo -n $p | jq -rj '.type'); tput sgr0
		printf '%s\n' $(echo -n $p | jq -r '.info')
	done
	#echo "Usage"
	echo
}

#cp ~/Desktop/ao.sh ~/Desktop/ao

IFS=

RED='\033[0;31m'
NC='\033[0m'

#cat $dbfile | jq --argjson rinfo $rinfo 'if has("runs") then .runs += [$rinfo] else .runs = []' > $dbfile.temp

#rinfo=$(jo -p time=$(date +%s) args=$(echo "$@"))
#cat $dbfile | jq --argjson rinfo $rinfo '.runs += [$rinfo]' > $dbfile.temp
#cp $dbfile.temp $dbfile

limit=20
dry=0
verbose=0
result=

# Global variable to track subcommand argument offset; rather
# than parsing all the subcommands and their arguments ahead of
# time using some kind of grammar (as you might in a language
# like Python), the code is written to "consume" the arguments
# left to right and discard all prior inputs (except those passed
# using pipes or stored as intermediary results).
gshift=0

P="ao/docinfo.json"
echo '' > "$P.temp"

# Generate documentation using a command name and string with usage
# information about that command
doc() {
	if [[ $verbose == 1 ]]; then log "Building documentation for $1"; fi
	dn=$1; di=$2; dp=''
	shift 2
	while [[ $1 ]]; do case $1 in
		-r )
			shift
			dr="$1"
		;;
		-p )
			#log "Received parameter"
			shift
			i=$3; if [[ $i == -r ]]; then i=''; fi
			dp+="$(jo name=$1 type=$2 info=$i)"
		;;
	esac; shift; done
	#echo $dp | jq -s '.'
	jo name=$dn info=$di returntype=$dr params="$(echo $dp | jq -s '.')" >> "$P.temp"
	# TODO: move this
	cat "$P.temp" | jq -s '. | sort_by(.name)' > $P
	if [[ $verbose == 1 ]]; then log "Done"; fi
}

doc help "Display help information; lists subcommands if no argument is given"\
	-r string
help_() {
	L=$(cat "ao/docinfo.json" | jq 'length')
	IFS=$'\n'
	if [[ $1 ]]; then
		gshift=$((gshift+1))
		jq -r --arg n $1 '.[] | select(.name == $n)' $P | pdocs
	else
		tput bold; echo "ao"; tput sgr0
		for i in $(seq 0 $(( $L - 1 ))); do
			jq -r --argjson z $i '.[$z]' $P | pdocs #| less -r
		done
		echo '----------'
	fi
}

doc status "Display information about the main ao database"\
	-r string
status_() {
	log "Database size: $(stat -c %s $dbfile) bytes, $(wc -l < $dbfile) lines"
}

doc dry "Execute a \"dry run\"; don't modify any files"\
	-r null
dry_() {
	dry=1
}

doc verbose "Print additional information about what the program is doing"\
	-r null
verbose_() {
	verbose=1
}

doc compress "Compress saved files into .tar.gz archives"\
	-r null
compress_() {
	compress=1
}

doc recursive "Recursively match subdirectories and files (as ** would)"\
	-r null
recursive_() {
	log "Setting option recursive"
	recursive=1
}

doc plain "Plain output; strips away the outermost layer of JSON formatting for compatibility between bash and jq"\
	-r null

plain_() {
	plain=1
}

doc rose "Display a randomly generated mosaic, for fun"\
	-p size int "The size of the output"\
	-r string
rose_() {
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
}

doc cleanup "Apply organization rules to restructure local files"\
	-r null
cleanup_() {
	log 'Organizing'
	printf "%s\n" $sources

	# why do these need to be quoted?
	for img in $sources/*.$imt; do
		move $img "./img_archive/$(basename $img)"
	done

	mkdir -p aoarchive; [ aosearch* ] && mv -nv aosearch* ./aoarchive
	mkdir -p textlike; [ ./!(notes|todo).txt ] && mv -nv ./!(notes|todo).txt textlike
	mkdir -p vid_archive; [ "$sources"/*."$vidtypes" ] && mv -nv "$sources"/*."$vidtypes" vid_archive
	IFS=$' \t\n'
	group_ftype "pdf" pgn dht docx ipynb pptx
}

doc ffind "Find a file in the database (based on its name)"\
	-p name string "The file name"
ffind_() {
	shift
	read_db | jq --arg target $1 '[.filenodes[] | select(.name | contains($target)) | .path]' > ao_output.json.temp
	cat ao_output.json.temp | jq '.'
	read_db | jq --argjson x "$(cat ao_output.json.temp)" 'if .outputs then . else .outputs=[] end | .outputs += [$x]' | write_db $dbfile
}

doc extract "Move a database path to a separate \"block\" and store a reference in the original database"\
	-p path string "The section of the database to transfer"
extract-property_() {
	shift
	block="db_block_$1.json"
	read_db | jq --arg path $1 '.[$path]' > $block
	read_db | jq --arg path $1 --arg b $block '.[$path] = {type: "block", path: $b}' | write_db $dbfile
}

doc note "Subcommands associated with notetaking functionality"
note_() {
	shift
#		backup_db
	case $1 in
		add )
			shift
			echo $1 >> notes.txt
			cat db_block_notes.json | jq --arg c "$1" --argjson t $(date +%s) '. += [{content: $c, time: $t}]' > db_block_notes.json.temp
			cp db_block_notes.json.temp db_block_notes.json
		;;

		find )
			shift
			cat db_block_notes.json | jq --arg target $1 '[.[] | select(.content | contains($target)) | .content]' > ao_output.json.temp
			cat ao_output.json.temp | jq '.'
#				cat $dbfile | jq --slurpfile x ao_output.json.temp 'if .outputs then . else outputs=[] end | .outputs += [$x]' > $dbfile.temp
		;;
	esac
}

doc process "Extract data from files to build databases"\
	-p target "string: one of [images, text]"\
	-r null
process_() {
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

	# Process image files
	if [[ $dry != 1 && $1 == images ]]
	then
		echo "fname${S}sha1${S}content" | tee -a ${indexname}
		for img in ${paths[@]:0:limit}; do
			checksum=$(sha1sum $img | awk '{ print $1 }')
			if [[ $verbose == 1 ]]; then
				echo $img
				echo $checksum
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
	# Process text files
	elif [[ $1 == text ]]; then
		# is there a nicer way to do this (implicit looping)?
		for t in ./*.$text_types; do
#				TODO: backup ao database
			hash=$(sha1sum $t | awk '{ print $1 }')
			log "Getting stats for $t"
			cat $dbfile | \
				jq --arg name $t --arg path $(realpath $t) --arg h $hash --arg category text --arg lines $(wc -l < $t) --arg chars $(wc -m < $t) --arg words $(wc -w < $t) \
				'.files += [{"name": $name, "path": $path, "sha1": $h, "category": $category, "lines": $lines|tonumber, "chars": $chars|tonumber, "words": $words|tonumber}]' > $dbfile
		done
	fi
	exit
}

doc limit "Limit the number of results an action returns"\
	-p n int\
	-r null
limit_() {
	shift; limit=$1
}

doc imfind "Find images containing the specified text"\
	-p query string "The text you want to search for"\
	-r "[filepath]"
imfind_() {
	shift; target=$1
	if [[ $verbose == 1 ]]; then echo "Searching for $target"; fi
	# Based on https://unix.stackexchange.com/a/527499
	# result=$(awk -v T="$target" -F $S '{ if ($3 ~ T) { print $1 } }' $indexname)
	cat $indexname | jq --arg t $target '[.[] | select(.content | contains($t)) | .fname]' | if [[ $plain == 1 ]]; then jq -r '.[]'; else jq; fi | tee ao_result.json
	#echo $result
}

doc open "Open the selection by creating a temporary directory with symlinks to its files"\
	-r null
open_() {
	shift
	echo "Displaying results"
	d="./aosearch ($(date))"
	mkdir $d
	result=$(cat ao_result.json | jq -r '.[]')
	echo $result | while read line; do
		echo "linking ${line}"
		ln -s $(realpath $line) $d/$(basename $line)_link
	done
	dolphin $d
}

doc manifest "Gather information about a directory and its contents"\
	-p path "string (filepath)"\
	-r null
manifest_() {
	IFS=$'\n'
	shift
	cd $1
	log "Generating directory listing of $(pwd)"
#		"python3.9" -c 'import os, json; print(json.dumps(os.listdir(".")))' > "ao_listing $(date).json"
	backup_db

	if [[ $recursive == 1 ]]; then paths=(**/*.*)
	else paths=(*.*); fi

	log "Found ${#paths[@]} files"
	echo '' > ao_batch.json.temp
	for f in ${paths[@]}; do
		log "Tracking $f"
		hash=$(sha1sum $f | awk '{ print $1 }')
		jo -p stats=$(file_stats $f) name=$f path=$(realpath $f) sha1=$hash time=$(date +%s) >> ao_batch.json.temp
	done
	read_db | jq --slurpfile b ao_batch.json.temp '.files += $b' | write_db $dbfile
#		rm ao_batch.json.temp

	cd $main
}

doc summarize "Compute a summary of a specified property/path over the database"\
	-p key "string (JSON path)" "The database path to aggregate"\
	-r json
summarize_() {
	shift
	backup_db
	read_db | jq "
		if .summaries then . else .summaries = {} end | 
		.summaries[\"$1\"] = ($1 | {sum: add, mean: (add/length), min: min, max: max})
	" | write_db $dbfile
	#| tee $dbfile.temp
	cat $dbfile | jq ".summaries[\"$1\"]"
}

doc update "Merge file snapshots into filenodes"\
	-r null
update-filenodes_() {
	backup_db
	shift
	IFS=$'\n'
	for i in $(seq 0 $limit); do
		log "Updating snapshot $i"
		read_db | jq --argjson i $i --arg t $(date +%s) '
			if .files[$i].processed then . else (
				if .filenodes then . else (.filenodes = []) end | 
				.files[$i].path as $p | 
				(.files | map(.path == $p) | index(true)) as $nodes | 
				(.files[$i] * {snapshots: [$i], time: $t}) as $fnode | 
				if ($nodes | length) != 0
					then .filenodes[$nodes] += $fnode
					else .filenodes += [$fnode] 
				end | .files[$i].processed = true
			) end' | write_db $dbfile
	done
}

doc download "Fetch a URL and archive the returned data"\
	-r null
download_() {
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
}

doc count "Count inputs or current selection"\
	-r int
count_() {
	echo $result | wc -l
}

# Execute subcommands
while [[ $1 ]]; do
	if [[ "$(cat "ao/docinfo.json" | jq -r '.[].name')" =~ "$1" ]]; then
		$1_ "${@:2}"
		shift $gshift
		gshift=0
	fi
	shift
done
if [[ "$1" == '--' ]]; then shift; fi

notify-send -u low "ao.sh" "ao.sh has finished executing"

#for img in **/*.$(eval echo $imgtypes); do
#	echo "${img},$(sha1sum $img)" | tee -a $indexname


# TODO: store triggers that run command/function on event
# TODO: add command for generating static documentation
