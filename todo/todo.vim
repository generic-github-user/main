" Based loosely on https://superuser.com/a/844060

"au BufNewFile,BufRead,BufReadPost todo.txt set syntax=todo
"syntax match todoLink /https:\/\/.*\s\+/

let b:current_syntax = "todo"

syntax match todoLink 'https\?:\/\/\S\+'
"hi def link simpleValue String
"highlight todoLink ctermfg=cyan guifg=#00ffff
"highlight todoLink *Underlined
hi def link todoLink Underlined

syntax match todoStar '\*'
"highlight todoStar ctermfg=darkblue cterm=bold
hi def link todoStar Operator

syn match todoComp '--\|-cc\|-archive'
"highlight todoComp ctermfg=green cterm=bold
hi def link todoComp Structure

syn match todoDur '-d \S\+'
"hi todoDur ctermfg=lightcyan cterm=bold
hi def link todoDur Constant

syn match todoTime '-t \S\+'
"hi todoTime ctermfg=darkred cterm=bold
hi def link todoTime Special

syn match todoFreq '-f \w\|-daily'
"hi todoFreq ctermfg=lightred

syn match todoTag ' #\S\+'
"hi todoTag ctermfg=darkmagenta
hi def link todoTag Type

"let b:current_syntax = 'todo'
