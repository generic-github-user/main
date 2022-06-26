#!/bin/bash
# Update todo list

main=todo.txt
cd ~/Desktop
# Move completed tasks to archive
grep -- "--" $main | sed -e 's/--//g' | tee >(cat - >> "complete.txt") >(echo "$(wc -l) completed tasks moved")
grep -va -- "--" $main | sponge $main
# Clone recurring tasks to main todo list
IFS=$'\n'
grep -e "-f d" -e "-daily" recurring.txt | sed -e "s/$/ $(date +'%a, %b %d')/" | grep -xvf $main -f "complete.txt" >> $main
# Make a quick and dirty backup of the todo list(s)
if [[ $1 == '-b' ]]; then
	targets="todo complete recurring"
	IFS=$' '
	#for t in "${targets[@]}"; do
	for t in $targets; do
		b="todo_backups/${t}_$(date +%s).tar.gz"
		tar czf "$b" "$t.txt"
		echo "Backed up $(wc -c < $b) bytes to $b"
	done
fi
