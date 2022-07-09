#!/bin/bash
# Update todo list

set -e
source ~/Desktop/ao/ao_config.sh

# Move completed tasks to archive
cd $todopath
grep -f cflags -- $tmain | sed -e 's/--//g' | tee >(cat - >> $todopath/complete.todo) >(echo "$(wc -l) completed tasks moved")
grep -va -f cflags -- $tmain | sort -n | sponge $tmain
echo -e ""

# Clone recurring tasks to main todo list
echo "Importing recurring tasks"
IFS=$'\n'
filter='s/ -cc//g;s/\s*$//'
sed -E -e "$filter" complete.todo > complete.temp.todo
sed -E -e "$filter" $tmain > todo.temp.todo
grep -e "-f d" -e "-daily" $main/recurring.todo | sed -e "s/$/ -t $(date +'%m-%d')/" | grep -Fxv -f todo.temp.todo -f complete.temp.todo | tee -a $tmain
#rm -v todo.temp.todo complete.temp.todo
echo -e ""

#echo $(pwd)
# Make a quick and dirty backup of the todo list(s)
if [[ $1 == '-b' ]]; then
	targets="$tmain $todopath/complete.todo $main/recurring.todo"
	IFS=$' '
	#for t in "${targets[@]}"; do
	#for t in $targets; do
	b="todo_backups/todos_$(date +%s).tar.gz"
	tar vczf "$todopath/$b" ${targets[@]}
	echo "Backed up $(wc -c < $b) bytes to $b"
	#done
fi

sort -n $tmain | sponge $tmain
