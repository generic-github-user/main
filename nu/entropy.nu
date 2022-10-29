#!/usr/bin/env nu

let words = (open /usr/share/dict/words | lines
		| first 20000 | wrap word
		| find -p { |it| ($it.word | size | get chars) > 5 })

echo ($words | first 20)
echo $"Loaded ($words | length) words"

let wtable = ($words
		| upsert entropy {
						|it| (($it.word | gzip | bytes length)
								/ ($it.word | size | get chars))
				})
$wtable | sort-by entropy | first 10
