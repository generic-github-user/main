" Based loosely on https://superuser.com/a/844060

"au BufNewFile,BufRead,BufReadPost todo.txt set syntax=todo
"syntax match todoLink /https:\/\/.*\s\+/
syntax match todoLink 'https:\/\/\S\+'
"hi def link simpleValue String
highlight todoLink ctermfg=cyan guifg=#00ffff

syntax match todoStar '\*'
highlight todoStar ctermfg=darkblue cterm=bold

syn match todoComp '--'
highlight todoComp ctermfg=green cterm=bold
