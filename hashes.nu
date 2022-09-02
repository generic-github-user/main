#!/usr/bin/env nu

let words = (open /usr/share/dict/words | lines | first 20000 | wrap word)
echo $"Loaded ($words | length) words"
let hashed = ($words
		| upsert hash { |it| $it.word | hash md5 }
		| upsert entropy { |it| $it.hash | gzip | bytes length })
$hashed | sort-by entropy | first 10
# let best = ($hashed.entropy | arg-min)
# $hashed | get $best
