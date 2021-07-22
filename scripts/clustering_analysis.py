# import libraries
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

class GetClusters():

	def __init__(self, query, sentiment):

		self.query = query # define query
		self.subreddits = [] # list to hold available subreddits
		self.sentiment = sentiment # sentiment to focus queries on
		self.clustering_df = pd.DataFrame() # dataframe to hold compliled dataset
		self.cluster_distances = [] # list of clustering distances for elbow plot
		self.neg_df = pd.DataFrame() # dataframe to hold negative comment data
		self.pos_df = pd.DataFrame() # dataframe to hold positive comment data
		self.neg_author_list = []
		self.pos_author_list = []

		
	def get_subreddit_data(self):
		"""Opens specified CSV files."""

		with open("subreddit_list.txt") as f:

			content = f.readlines()

		content = [x.strip() for x in content] 

		subreddits = []

		for subreddit in content:
   			
			subreddits.append(subreddit)

			self.subreddits = subreddits



	def collect_data(self):
		"""Opens specified CSV files and adds them
		to clustering_df"""

		for subreddit in self.subreddits:

			filepath = "data/"+str(subreddit)+'_'+str(self.query)+'.csv'
			temp_df = pd.pandas.read_csv(filepath)
			temp_df["subreddit"] = subreddit
			
			try:

				self.clustering_df = pd.concat([self.clustering_df, temp_df], axis =0)

			except:

				self.clustering_df = temp_df


	def get_cluster_distances(self):
		"""Collects sum of squared distances for cluster values
		1-10 using kmeans clustering."""
		
		K = range(1,10)
		array = np.array(self.clustering_df[self.sentiment]).reshape(-1, 1)

		for k in K:

			km = KMeans(n_clusters=k)
			km = km.fit(array)
			self.cluster_distances.append(km.inertia_)

	def plot_cluster_distances(self):
		"""Plots cluster distances. """

		df = pd.DataFrame()
		df["Pooled subreddit data"] = self.cluster_distances
		df.index += 1
		df.plot(xlabel="Number of Clusters", ylabel="Sum of Square Distances",title="Elbow Plot for Sentiment Data")


	def cluster_data(self):
		"""Assigns clusters to each comment based on sentiment score."""

		km = KMeans(n_clusters=3, random_state=42)
		self.clustering_df["cluster"] = km.fit_predict(np.array(self.clustering_df["compound_sentiment"]).reshape(-1, 1))

	
	def label_clusters(self):
		"""Labels clusters as negative, neutral, or positive."""

		cluster_1 = self.clustering_df[self.sentiment].loc[self.clustering_df["cluster"] == 0].mean()
		cluster_2 = self.clustering_df[self.sentiment].loc[self.clustering_df["cluster"] == 1].mean()
		cluster_3 = self.clustering_df[self.sentiment].loc[self.clustering_df["cluster"] == 2].mean()

		cluster_means = [cluster_1, cluster_2, cluster_3]
		neutral = [cluster_1, cluster_2, cluster_3]

		positive_index = cluster_means.index(max(cluster_means))
		negative_index = cluster_means.index(min(cluster_means))
		

		self.clustering_df.loc[self.clustering_df["cluster"] == positive_index, "cluster"] = "positive"
		self.clustering_df.loc[self.clustering_df["cluster"] == negative_index, "cluster"] = "negative"

		self.clustering_df["cluster"].loc[(self.clustering_df["cluster"]!="positive") & (self.clustering_df["cluster"]!="negative")] = "neutral"



	def main(self):
		"""Wrapper function."""
	
		self.get_subreddit_data()
		self.collect_data()
		self.get_cluster_distances()
		self.plot_cluster_distances()
		self.cluster_data()
		self.label_clusters()

		self.clustering_df.to_csv("cluster_data/cluster_dataframe.csv")

		return self.clustering_df


