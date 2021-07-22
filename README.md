# subreddit sentiment analysis

This repository contains a script that performs a query search and scrapes comments ~250 of the most active subreddits by date. I've used this analysis to perform sentiment analysis on comments related to vaccines in thessubreddits over the past year. Comments that were scraped contain a stemmed version of the word "vaccine" and belonged to a parent post that mentioned vaccines. 

I was initially curious to see if there was a meaningful difference in vaccine-related comments between r/conservative and r/politics given their substantially different political leanings. The search has now been expanced significantly to see who is posting the most vaccine-related comments with negative sentiment and where they prefer to post it. 

The praw and Pushshift API libraries were used to scrape the comments and comment data. The vaderSentiment library was used to quantify sentiment for each comment. pandas graphing functionality was used to visualize the results. 

I searched for vaccine-related comments (only under related posts) from the dates 2020-07-16 to 2021-07-20. The data are very noisy. For some days, I didn't find any relevant comments in a given subreddit, and for other days there were quite a few comments. A smoothing function was applied (pandas.df.rolling) to make the curves a bit more intepretable. The small gaps in the curves were filled in with linear interpolation. Since the initial time points couldn't be smoothed fully, I dropped the first 30 day's worth of data so that all of the visualized time points were treated consistently. Comment data from the date range 2020-08-15 to 2021-07-20 is visualized below. 

SKLearn's k-means clustering was used to cluster the data. Once the data were clustered into three clusters (positive, neutral, and negative sentiment) using k-means, some broader analysis of the trends in the data were examined. These data were plotted using PRISM 8.4. Because some of the analysis involves associating specific user id's with large numbers of negative comments, I've left some of this code out of the repository as I don't want to make it easy to target these specific Redditors. 

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
* Run the 01-reddit_scraper.ipynb notebook to collect the raw data needed for this project. 
* Visualize the results in the 02-sentiment_analysis.ipynb file. 
* Cluster the data and analyze patterns of posting in 03-clustering_analysis.ipynb file. 

## Results:

![Visualization of sentiment analysis](https://github.com/miRNA183/subreddit_sentiment_analysis/blob/main/images/sentiment_analysis.jpg?raw=true)
![Visualization of number of comments per day](https://github.com/miRNA183/subreddit_sentiment_analysis/blob/main/images/post_count.jpg?raw=true)
![Visualization of sentiment distributions](https://github.com/miRNA183/subreddit_sentiment_analysis/blob/main/images/sentiment_distributions.jpg?raw=true)
![Word cloud of vaccine-related comments with negative sentiment](https://github.com/miRNA183/subreddit_sentiment_analysis/blob/main/images/neg_comment_wordcloud.jpg?raw=true)

