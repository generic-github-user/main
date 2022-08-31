# https://www.nushell.sh/cookbook/parsing_git_log.html
git log --pretty=%h»¦«%s»¦«%aN»¦«%aE»¦«%aD -n 25 | lines
		| split column "»¦«" commit subject name email date
		| upsert date {|d| $d.date | into datetime}
		| sort-by date
