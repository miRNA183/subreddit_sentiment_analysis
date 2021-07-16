# subreddit sentiment analysis

This repository contains a script that performs a query search and scrapes comments from specified subreddits by date. I've used this analysis to take a look at the sentiments for comments related to vaccines in the r/conspiracy, r/conservative, r/politics, and r/COVID19 subreddits over the past year. Comments that were scraped contained a word related to "vaccine" and belonged to a parent post that mentioned vaccines. 

I was initially curious to see if there was a meaningful difference between r/conservative and r/politics given their substantially different political leanings. Because the data were noisy, I also included r/COVID19 and r/conspiracy to act as positive and negative controls for this analysis (respectively). 

The praw and Pushshift API libraries were used to scrape the comments and comment data. The vaderSentiment libarary was used to quantify sentiment for each comment. pandas graphing functionality was used to visualize the results. 

I searched for vaccine-related comments (only under vaccine related posts) from the dates 2020-07-15 to 2021-07-15. The data were very noisy. For some days, I didn't find any relevant comments in a given subreddit, and for other days there were quite a few comments. A smoothing function was applied (pandas.df.rolling) to make the curves a bit more intepretable. Since the initial time points couldn't be smoothed fully, I dropped the first 30 day's worth of data so that all time points were treated consistently. Comment data from the date range 2020-08-14 to 2021-07-15 is visualized below. 

## Dependencies:
* pandas
* time
* datetime
* praw
* psaw
* vaderSentiment
* iPython

## To run the code:
* Add your Reddit credentials to the reddit_credentials.txt file. 
* Run the reddit_scraper.ipynb notebook
* Visualize the results in the sentiment_analysis.ipynb file. 

## Results:

![Visualization of sentiment analysis](https://github.com/miRNA183/subreddit_sentiment_analysis/blob/main/sentiment_analysis.jpg?raw=true)

