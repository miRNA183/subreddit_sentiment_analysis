# Import libraries
import pandas as pd
import time
import datetime as dt
import praw
from nltk.stem import PorterStemmer
from psaw import PushshiftAPI
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.stem import PorterStemmer

class Scraper():

	def __init__(self, start_date, end_date, subreddit, query, client_id, client_secret, user_agent, username, password):

		current_date = dt.datetime.strptime(start_date, '%Y-%m-%d') # current date to analyze
		self.current_date = current_date.date()
		next_date = self.current_date # next date to analyze
		self.next_date = self.current_date + dt.timedelta(days=1)
		end_date = dt.datetime.strptime(end_date, '%Y-%m-%d') # last day to analyze
		self.end_date = end_date.date()
		self.subreddit = subreddit # select subreddit to scrape
		self.query = query # define query
		self.client_id = str(client_id)
		self.client_secret = str(client_secret)
		self.user_agent = str(user_agent)
		self.username = str(username)
		self.password = str(password)
		self.reddit = "" # reddit praw instance
		self.api = ""
		self.timestamp_1 = "" # holds time stamp for day being analyzed
		self.timestamp_2 = "" # holds time stamp for next day
		cols = ['id', 'date', 'author', 'comment', 'score', 'pos_sentiment', 
		'neg_sentiment', 'neu_sentiment', 'compound_sentiment']
		self.df = pd.DataFrame(columns=cols)
		self.id_list = [] # list holds id's for relevant posts
		self.stemmer = "" # holds stemmer object
		self.sentiment_analyzer = "" # holds sentiment analyzer object


	def start_praw(self):
		"""Initialize Reddit praw instance
		"""
		self.reddit = praw.Reddit(client_id=self.client_id, \
                     client_secret=self.client_secret, \
                     user_agent=self.user_agent, \
                     username=self.username, \
                     password=self.password)
		self.api = PushshiftAPI()
		self.stemmer = PorterStemmer()
		self.sentiment_analyzer = SentimentIntensityAnalyzer()

	
	def get_timestamp(self):
		"""Converts dates into timestamps for convenient lookup."""

		self.timestamp_1 = int(dt.datetime.timestamp(dt.datetime.strptime(str(self.current_date), '%Y-%m-%d')))
		self.timestamp_2 = int(dt.datetime.timestamp(dt.datetime.strptime(str(self.next_date), '%Y-%m-%d')))

	def next_day(self):
		"""Iterates to next day for analysis."""

		self.current_date += dt.timedelta(days=1)
		self.next_date += dt.timedelta(days=1)
		self.id_list, self.timestamp_1, self.timestamp_2 = [], "", ""

	def get_sentiment(self, comment):
		"""Calculates positive, negative, and compound sentiment for input comment.
		This function returns a dictionary with sentiment scores."""

		sentiment_dict = self.sentiment_analyzer.polarity_scores(comment)

		return sentiment_dict



	def get_daily_posts(self):
		"""Return list of post ID's that match date range and query in subreddit."""

		results = list(self.api.search_submissions(after=self.timestamp_1, before=self.timestamp_2, 
                                          subreddit=str(self.subreddit), 
                                          filter=['id'], 
                                          q=str(self.query),
                                          size=100))
		for submission in results:
			self.id_list.append(submission.id)

	def find_comments(self):
		"""Iterates through comments in each post to find comments that refer to query."""

		for item in self.id_list:
			submission = self.reddit.submission(item)
			submission.comments.replace_more(limit=100)
			for comment in submission.comments.list():
				comment_words = [self.stemmer.stem(word) for word in comment.body.split()]
				if self.stemmer.stem(str(self.query)) in comment_words:
					sentiment_dict = self.get_sentiment(comment.body)
					temp_list = [comment.id, self.current_date, comment.author, comment.body, comment.score,
					sentiment_dict["pos"], sentiment_dict["neg"], sentiment_dict["neu"], sentiment_dict["compound"]]
					self.df.loc[len(self.df)] = temp_list

	def save_dataframe(self):
		"""Saves current self.df object as CSV file."""

		self.df.to_csv(str(self.subreddit)+'_'+str(self.query)+'.csv', index = False)


	def main(self):
		"""Main wrapper function."""
		self.start_praw()
		while self.current_date != self.end_date:
			print(self.current_date)
			self.get_timestamp()
			self.get_daily_posts()
			self.find_comments()
			self.next_day()
		self.save_dataframe()
		









