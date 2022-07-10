" Based loosely on https://superuser.com/a/844060

"au BufNewFile,BufRead,BufReadPost todo.txt set syntax=todo
"syntax match todoLink /https:\/\/.*\s\+/
syntax match todoLink 'https:\/\/\S\+'
"hi def link simpleValue String
highlight todoLink ctermfg=cyan guifg=#00ffff

syntax match todoStar '\*'
highlight todoStar ctermfg=darkblue cterm=bold

syn match todoComp '--\|-cc\|-archive'
highlight todoComp ctermfg=green cterm=bold

syn match todoDur '-d \S\+'
hi todoDur ctermfg=lightcyan cterm=bold

syn match todoTime '-t \S\+'
hi todoTime ctermfg=darkred cterm=bold

syn match todoFreq '-f \w\|-daily\|-weekly\|-monthly'
hi todoFreq ctermfg=lightred

syn match todoTag ' #\w\+'
hi todoTag ctermfg=darkmagenta

"let b:current_syntax = 'todo'
