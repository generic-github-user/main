#!/bin/bash
# Update todo list

cd ~/Desktop
# Move completed tasks to archive
grep -- "--" todo.txt | sed -e 's/--//g' | tee >(cat - >> "complete.txt") >(echo "$(wc -l) completed tasks moved")
grep -va -- "--" todo.txt | sponge todo.txt
# Clone recurring tasks to main todo list
IFS=$'\n'
grep -e "-f d" -e "-daily" recurring.txt | sed -e "s/$/ $(date +'%a, %b %d')/" | grep -xvf todo.txt -f "complete.txt" >> todo.txt
# Make a quick and dirty backup of the todo list
b="todo_backups/todo_$(date +%s).tar.gz"
tar czf $b todo.txt
echo "Backed up $(wc -c < $b) bytes to $b"
