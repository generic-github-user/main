#!/bin/bash
# Update todo list

cd ~/Desktop
# Move completed tasks to archive
grep -- "--" todo.txt | sed -e 's/--//g' | tee >(cat - >> "complete.txt") >(echo "$(wc -l) completed tasks moved")
grep -va -- "--" todo.txt | sponge todo.txt
