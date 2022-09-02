let src = ls ./**/*.py
$src | merge { $src | each { |file| $file.name | open --raw | size } }
		| to md | save sloc-output.md
