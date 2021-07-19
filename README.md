# subreddit sentiment analysis

This repository contains a script that performs a query search and scrapes comments from specified subreddits by date. I've used this analysis to perform sentiment analysis on comments related to vaccines in the r/conservative, r/politics, r/worldpolitics, r/conspiracy and r/COVID19 subreddits over the past year. Comments that were scraped contain a stemmed version of the word "vaccine" and belonged to a parent post that mentioned vaccines. 

I was initially curious to see if there was a meaningful difference in vaccine-related comments between r/conservative and r/politics given their substantially different political leanings. Because the data are quite noisy, I also included r/COVID19 and r/conspiracy to act as a positive and negative (pun intended) controls for this analysis. 

The praw and Pushshift API libraries were used to scrape the comments and comment data. The vaderSentiment library was used to quantify sentiment for each comment. pandas graphing functionality was used to visualize the results. 

I searched for vaccine-related comments (only under related posts) from the dates 2020-07-16 to 2021-07-18. The data are very noisy. For some days, I didn't find any relevant comments in a given subreddit, and for other days there were quite a few comments. A smoothing function was applied (pandas.df.rolling) to make the curves a bit more intepretable. The small gaps in the curves were filled in with linear interpolation. Since the initial time points couldn't be smoothed fully, I dropped the first 30 day's worth of data so that all of the visualized time points were treated consistently. Comment data from the date range 2020-08-15 to 2021-07-18 is visualized below. 

## Dependencies:
* Python 3.8
* sklearn
* nltk
* pandas
* time
* datetime
* praw
* psaw
* vaderSentiment
* iPython

## To run the code:
* Add your Reddit credentials to the reddit_credentials.txt file. 
* Run the 01-reddit_scraper.ipynb notebook
* Visualize the results in the 02-sentiment_analysis.ipynb file. 

## Results:

![Visualization of sentiment analysis](https://github.com/miRNA183/subreddit_sentiment_analysis/blob/main/images/sentiment_analysis.jpg?raw=true)
![Visualization of number of comments per day](https://github.com/miRNA183/subreddit_sentiment_analysis/blob/main/images/post_count.jpg?raw=true)

