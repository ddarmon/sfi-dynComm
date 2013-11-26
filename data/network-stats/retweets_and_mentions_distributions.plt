set terminal postscript color
set log xy

set output 'incoming_info_distribution.eps'
set xlabel 'x = number of retweets made + mentions received per user'
set ylabel 'number of x'
p 'incoming_info_distribution.txt' w p pt 7 lt 7 notitle

set output 'outgoing_info_distribution.eps'
set xlabel 'x = number of retweets received + mentions made per user'
set ylabel 'number of x'
p 'outgoing_info_distribution.txt' w p pt 7 lt 7 notitle

set output 'retweets_made_distribution.eps'
set xlabel 'x = number of retweets made per user'
set ylabel 'number of x'
p 'retweets_made_distribution.txt' w p pt 7 lt 7 notitle

set output 'mentions_made_distribution.eps'
set xlabel 'x = number of mentions made per user'
set ylabel 'number of x'
p 'mentions_made_distribution.txt' w p pt 7 lt 7 notitle

set output 'retweets_received_distribution.eps'
set xlabel 'x = number of retweets received per user'
set ylabel 'number of x'
p 'retweets_received_distribution.txt' w p pt 7 lt 7 notitle

set output 'mentions_received_distribution.eps'
set xlabel 'x = number of mentions received per user'
set ylabel 'number of x'
p 'mentions_received_distribution.txt' w p pt 7 lt 7 notitle
