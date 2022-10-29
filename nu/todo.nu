#!/usr/bin/env nu

def main [
				--dry
		] {
		if $dry { echo "(dry run)" }

		let path = "/home/alex/Desktop/todo.yaml"
		let bpath = $"(date format '%Y-%m-%d_%H-%M-%S').yaml"
		echo $"Backing up to ($bpath)"
		cp $path $"./todo-backup/($bpath)"
		
		#let todos = (open $path | from yaml)
		let todos = (open $path)
		#$todos | append 
		let output = ($todos | upsert other (
				$todos.other | append (
				for t in $todos.recurring.daily {
						# instantiated todo item
						let inst = $"($t) \((date format '%Y-%m-%d')\)"
						# echo $inst
						if $inst not-in $todos.other {
								echo $inst
								# let todos.other = ($todos.other | append $inst)
						}
				}
		)))
		echo $output
		if $dry {
				echo ($output | to yaml)
		} else {
				$output | save $path
		}
}
