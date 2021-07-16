# subreddit sentiment analysis

This repository contains a script that performs a query search and scrapes comments from specified subreddits by date. I've used this analysis to take a look at the sentiments for comments related to vaccines in the r/conspiracy, r/conservative, r/politics, and r/COVID19 subreddits over the past year. Comments that were scraped contained a word related to "vaccine" and belonged to a parent post that mentioned vaccines. 

The praw and Pushshift API libraries were used to scrape the comments and comment data. The vaderSentiment libarary was used to quantify sentiment for each comment. pandas graphing functionality was used to visualize the results. 

## Dependencies:
* pandas
* time
* datetime
* praw
* psaw
* vaderSentiment
* iPython
