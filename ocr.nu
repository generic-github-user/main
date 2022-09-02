#!/usr/bin/env nu
def main [path: string] {
		let db_path = "~/Desktop/imdb"
		mkdir $db_path
		echo "Processing"
		let db = (ls $db_path --short-names).name
		# echo $db
		let imgs = (glob $"($path)/*.{png,jpg,jpeg}")
		for i in $imgs {
				echo $i
				let md5 = (open $i | hash md5)
				if $md5 not-in $db {
							tesseract $i - | save $"($db_path)/($md5)"
				}
		}
}
