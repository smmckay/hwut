" getpot mode for VIM
syntax region String   start='\"' end='\"'    skip='\\\"'
syntax region Comment  start='#'  end='\n'
syntax region Section  start='\[' end='\]'
syntax region VariableExpansion   start='\${' end='}'
" 
highlight String            ctermfg=magenta              guifg=magenta
highlight Comment           ctermfg=red                  guifg=DarkRed
highlight VariableExpansion ctermfg=green  ctermbg=white guifg=DarkGreen
highlight Section           ctermfg=yellow ctermbg=green guifg=Yellow     guibg=DarkGreen
