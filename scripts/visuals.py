import pandas as pd

class DisplaySentimentData():

	def __init__(self, query, subreddits, sentiment):

		self.query = query # define query
		self.subreddits = list(subreddits)
		self.sentiment = sentiment
		self.sentiment_df = pd.DataFrame()
		self.count_df = pd.DataFrame()


	def collect_data(self):
		"""Opens specified CSV files."""

		for subreddit in self.subreddits:

			filepath = "data/"+str(subreddit)+'_'+str(self.query)+'.csv'
			temp_df = pd.pandas.read_csv(filepath)
			self.collect_sentiment_by_date(temp_df, subreddit)
			self.count_by_date(temp_df, subreddit)
			
	def collect_sentiment_by_date(self, df, subreddit):
		"""Collects sentiment data by date from dataframe and creates
		an average for each date. Data is smoothed with a rolling 30 
		day average."""

		sentiment_df = pd.DataFrame()
		sentiment_df["r/"+subreddit] = df.groupby("date")[self.sentiment].mean()
		sentiment_df = sentiment_df.rolling(30, min_periods=1)
		sentiment_df = sentiment_df.mean()
		try:
			self.sentiment_df = self.sentiment_df.join(sentiment_df, how="outer")
		except ValueError:
			self.sentiment_df = sentiment_df
	
	def count_by_date(self, df, subreddit):
		"""Creates feature with the number of posts per day."""

		count_df = pd.DataFrame()
		count_df["r/"+subreddit] = df.groupby("date")[self.sentiment].count()
		
		try:
			self.count_df = self.count_df.join(count_df, how="outer")
		except ValueError:
			self.count_df = count_df

	def plot_data(self):

		self.sentiment_df = self.sentiment_df.iloc[30:,:]
		self.sentiment_df = self.sentiment_df.interpolate()

		self.sentiment_df.plot(rot=0,xlabel="Date", 
             ylabel="Sentiment Score (higher is more positive)", fontsize=12,
             figsize=(11, 7), title="Sentiment Analysis of Comments Related to Vaccines")


		self.count_df = self.count_df.iloc[30:,:]
		self.count_df = self.count_df.interpolate()

		self.count_df.plot(rot=0,xlabel="Date", 
             ylabel="Number of Posts", fontsize=12, 
             figsize=(11, 7), title="Number of Comments Related to Vaccines")

	def main(self):

		"""Wrapper function."""

		self.collect_data()
		self.plot_data()


