#!/bin/bash
# Update todo list

set -e
main=.todo
cd ~/Desktop

# Move completed tasks to archive
grep -e '--' -e ' -archive' -e ' -cc' -- $main | sed -e 's/--//g' | tee >(cat - >> "complete.todo") >(echo "$(wc -l) completed tasks moved")
grep -va -e '--' -e ' -archive' -e ' -cc' -- $main | sponge $main
echo -e ""

# Clone recurring tasks to main todo list
echo "Importing recurring tasks"
IFS=$'\n'
filter='s/ -archive| -cc| -daily| -[fd] \S+| #\w+//g;s/\s*$//'
sed -E -e "$filter" complete.todo > complete.temp.todo
sed -E -e "$filter" $main > todo.temp.todo
grep -e "-f d" -e "-daily" recurring.todo | sed -E -e "$filter" | sed -e "s/$/ $(date +'%a, %b %d')/" | grep -xvf "todo.temp.todo" -f "complete.temp.todo" | tee -a $main
rm -v todo.temp.todo complete.temp.todo
echo -e ""

# Make a quick and dirty backup of the todo list(s)
if [[ $1 == '-b' ]]; then
	targets="$main complete.todo recurring.todo"
	IFS=$' '
	#for t in "${targets[@]}"; do
	for t in $targets; do
		b="todo_backups/${t}_$(date +%s).tar.gz"
		tar vczf "$b" "$t"
		echo "Backed up $(wc -c < $b) bytes to $b"
	done
fi
