set terminal postscript color solid
set output 'twitter_distributions.eps'
set log xy
#p 'mentions_made_distribution.txt' w p ti 'mentions made', 'mentions_received_distribution.txt' w p ti 'mentions received', 'retweets_made_distribution.txt' w p ti 'retweets made', 'retweets_received_distribution.txt' w p ti 'retweets received'
#, 'incoming_info_distribution.txt' w p ti 'incoming information flow', 'outgoing_info_distribution.txt' w p ti 'outgoing information flow'
#p 'in_degree_distribution.txt' w p ti 'in-degree (nb followees)', 'out_degree_distribution.txt' w p ti 'out-degree (nb followers)'
p 'nb_tweets_distribution.txt' w p ti 'nb tweets', 'nb_hashtags_distribution.txt' w p ti 'nb hashtags'
