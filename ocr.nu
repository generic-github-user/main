#!/usr/bin/env nu
def main [
				path: string
				--recursive
				--depth: int = 1
		] {
		let db_path = "/home/alex/Desktop/imdb"
		mkdir $db_path
		echo "Processing"
		let db = (ls $db_path --short-names).name
		# echo $db

		let gl = (if $recursive { "**/*" }
		else { "*" } )
		cd $path
		# let pattern = $"\(?i\)($gl).{png,jpg,jpeg}"
		let pattern = $"($gl).{png,PNG,jpg,JPG,jpeg,JPEG}"
		echo $pattern

		let imgs = (glob $pattern --depth $depth)
		echo ($imgs | length)

		for i in $imgs {
				echo $i
				let md5 = (open $i | hash md5)
				if $md5 not-in $db {
							tesseract $i - | save $"($db_path)/($md5)"
				}
		}
}
