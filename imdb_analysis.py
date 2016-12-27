# the data is from: https://www.kaggle.com/deepmatrix/imdb-5000-movie-dataset
import pandas as pd
from collections import Counter
import numpy as np
import imdb_plot as iplot
import math
import imdb_scraping as iscrap
import imdb_util as iutil
import imdb_machine_learning as iml

data_path = 'C:/Users/rodri/OneDrive/Documentos/python/data/'

def get_dataset():
	df = pd.read_csv(data_path+'movie_metadata.csv')
	return df

def get_plot_keywords_count(df):
	c = Counter()
	plot_keywords = df['plot_keywords'].dropna()
	for words in plot_keywords:
		l = words.split('|')
		c.update(l)

	return c


# return a df showing the movie title, imdb score and plot keywords of the top X imdb scores
def top_x_imdb_scores(df, x=20):
	df.sort_values(by='imdb_score', ascending=False, inplace=True)
	df.reset_index(inplace=True)
	topX = df[['movie_title', 'imdb_score', 'plot_keywords']][:x]
	#print(top20)
	return topX

def group_by_imdb_score(df):
	imdb_score = df['imdb_score']
	df['imdb_label'] = pd.cut(imdb_score, 3, labels=['Low', 'Medium', 'High'])
	#print(df.head())
	return df

def imdb_vs_country(df):
	imdb_country = df[['country', 'imdb_score']]
	imdb_country = imdb_country.groupby('country').agg(['mean', 'count'])
	imdb_country.columns = ['imdb_mean', 'movies_count']
	print(imdb_country.sort_values(by='imdb_mean', ascending=False))

def imdb_vs_movie_year(df):
	imdb_movie_year = df[['imdb_score', 'title_year']]
	imdb_movie_year.dropna(inplace=True)
	imdb_movie_year = imdb_movie_year.groupby('title_year').agg(['mean', 'count'])
	imdb_movie_year.columns = ['imdb_mean', 'movies_count']
	print(imdb_movie_year)

def imdb_vs_movie_facebook_likes(df):
	df2 = df[['imdb_score', 'movie_facebook_likes', 'movie_title']]
	df2.dropna(inplace=True)
	df2 = df2.sort_values(by='movie_facebook_likes', ascending=False)
	print(df2[ df2['movie_facebook_likes'] > 0])

def imdb_vs_director_facebook_likes(df):
	df2 = df[['imdb_score', 'director_facebook_likes', 'director_name']]
	df2 = df2.groupby('director_name').agg('mean')
	df2 = df2.sort_values('director_facebook_likes', ascending=False)
	print(df2[ df2['director_facebook_likes'] > 0])

def imdb_vs_cast_facebook_likes(df):
	df2 = df[['imdb_score', 'cast_total_facebook_likes', 'movie_title']]
	df2 = df2.sort_values('cast_total_facebook_likes', ascending=False)
	print(df2[ df['cast_total_facebook_likes'] > 0] )

def get_genres_count(df):
	c = Counter()
	genres = df['genres'].dropna()
	for g in genres:
		g = g.split('|')
		c.update(g)
	#print(c)
	return c

def director_vs_number_of_movies(df):
	df2 = df[['director_name', 'movie_title', 'imdb_score']]
	df2 = df2.groupby('director_name')['movie_title', 'imdb_score'].agg(['count', 'mean'])
	df2.columns = ['movie_counts', 'imdb_mean']
	df2 = df2.sort_values(by='imdb_mean', ascending=False)
	print(df2)

'''
This is a superficial comparision between budget and gross. 
I'm not considering a bunch of facts like: 
	currency(Dollar, Real, etc)
	the 'value' of dollar in the course of time
'''
def budget_vs_gross(df):
	df2 = df[['movie_title', 'budget', 'gross']]
	df2['profit'] = df['gross'] - df['budget']
	df2.dropna(inplace=True)
	df2.drop_duplicates(['movie_title'], inplace=True)
	#print(df2)
	return df2

def keywords_weight(df):
	# get plot keywords count
	plot_count = get_plot_keywords_count(df)
	# drop all the rows where plot_keywords is empty (NaN)
	# NEW
	#df.dropna(subset=['plot_keywords'], inplace=True)
	df2 = df[['plot_keywords', 'imdb_score']]

	# loop through plot_keywords and imdb_score in order to get the imdb_score SUM for each word
	plot_imdb = {}
	plot_keywords = df2['plot_keywords'].tolist()
	imdb_score = df2['imdb_score'].tolist()
	for pltws, imdb in zip(plot_keywords, imdb_score):
		# NEW
		if pltws is not np.nan:
			for w in pltws.split('|'):
				if plot_imdb.get(w): 
					plot_imdb[w] += imdb
				else:
					plot_imdb[w] = imdb

	# get the MEAN imdb score for each word
	for w, s in plot_imdb.items():
		plot_imdb[w] = round(s/plot_count[w], 1)

	# convert from Counter (plot_count) to DataFrame
	df3 = pd.DataFrame.from_dict(plot_count, orient='index').reset_index()
	df3.columns = ['plot_keyword', 'count']
	df3.set_index('plot_keyword', inplace=True)
	
	# convert from dict (plot_imdb) to DataFrame
	df4 = pd.DataFrame.from_dict(plot_imdb, orient='index').reset_index()
	df4.columns = ['plot_keyword', 'imdb_score_mean']
	df4.set_index('plot_keyword', inplace=True)

	# join DataFrames
	df5 = df3.join(df4)
	
	# Let's measure the two criteria on similar numerical scale, and then assign the importance (weights) to those criteria
	# The scale I'll use is 0-100 for both variables (count and imdb score)
	# Step 1: get the max and min from each variable
	countMax = df5['count'].max()
	countMin = df5['count'].min()
	imdbMax = df5['imdb_score_mean'].max()
	imdbMin = df5['imdb_score_mean'].min()

	# Step 2: get the weight using the formula: (x-min)/(max-min)*100
	df5['count_weight'] = (df5['count']-countMin)/(countMax-countMin)*100
	df5['imdb_weight'] = (df5['imdb_score_mean']-imdbMin)/(imdbMax-imdbMin)*100

	# Step 3: Calculate the weighted average
	# Here I'll assume the weight of imdb is 75%. Hence, the weight of count will be 25%.
	df5['weighted_average'] = round( (.25*df5['count_weight'] + .75*df5['imdb_weight']), 1)

	df5 = df5['weighted_average']
	# convert df5 to dict
	weighted_avg = df5.to_dict()
	iutil.save_pickle(weighted_avg, 'weighted_plot_keywords.pickle')
	
	# apply the weighted average to plot_keywords in the original DF
	# remove the '\xa0' character from the movie titles
	df['movie_title'] = df.apply(lambda x: x['movie_title'].replace('\xa0', ''), axis=1)	
	movie_titles = df['movie_title'].tolist()
	df.set_index('movie_title', inplace=True)
	plot_keywords_weight = {}
	# loop through each list of words of each row, and then calculate the weight average
	for mt, pltws in zip(movie_titles, plot_keywords):
		# NEW
		if pltws is not np.nan:
			weight = 0
			for w in pltws.split('|'):
				weight += weighted_avg[w]
			_len = len(pltws.split('|'))
			plot_keywords_weight[mt] = round(weight/_len, 1)
		else:
			plot_keywords_weight[mt] = 0

	# convert from dict (plot_keywords_weight) to DataFrame
	df6 = pd.DataFrame.from_dict(plot_keywords_weight, orient='index')
	df6.columns = ['plot_keywords_weight']
	# join both tables
	df7 = df.join(df6)
	df7.reset_index(inplace=True)
	#print(df7)
	iutil.save_pickle(df7, 'imdb.pickle')

	return df7

def assign_plot_keywords_weight(df):
	filename = 'weighted_plot_keywords.pickle'
	# check whether the weighted plot keywords exists or not  
	if not iutil.file_exists(filename):
		df_temp = get_dataset()
		keywords_weight(df_temp)
	 
	keywords_dict = iutil.get_pickle(filename)
	plot_keywords = df['plot_keywords'].tolist()
	movies_name = df['movie_title'].tolist()

	# assign a wegiht to plot keywords for each movie
	new_keywords_dict = {}
	for words, mname in zip(plot_keywords, movies_name):
		if words is not None:
			i = 0
			weighted_sum = 0
			for w in words.split('|'):
				if keywords_dict.get(w):
					weight = keywords_dict[w]
					weighted_sum += weight
					i+=1
			if weighted_sum > 0:
				new_keywords_dict[mname] = weighted_sum/i
			else:
				new_keywords_dict[mname] = 0
		else:
			new_keywords_dict[mname] = 0

	# from dict to DataFrame
	df2 = pd.DataFrame.from_dict(new_keywords_dict, orient='index')
	df2.columns = ['plot_keywords_weight']
	
	df3 = df.set_index('movie_title').join(df2).reset_index()
	df3 = df3[['movie_title', 'movie_facebook_likes', 'cast_total_facebook_likes', 'plot_keywords', 'plot_keywords_weight']]
	#print(df3)
	return df3


# Preparing data for machine learning
if iutil.file_exists('imdb.pickle'):
	df = iutil.get_pickle('imdb.pickle')
else:
	df = get_dataset()
	df = df[['movie_title', 'movie_facebook_likes', 'cast_total_facebook_likes', 'plot_keywords', 'imdb_score']]
	df.drop_duplicates(['movie_title'], inplace=True)
	df = keywords_weight(df)

df2 = iscrap.get_new_movies_coming_soon()
df3 = assign_plot_keywords_weight(df2)
#print(df.head())
#print(df3.head())
iml.start(df, df3)

# Data Analysis
# (OK) imdb vs country | (OK) imdb vs movie year | (OK) imdb vs facebook popularity 
# (OK) imdb vs director facebook popularity | (OK) imdb vs cast facebook popularity
# (OK) imdb vs genre | (OK) genre vs movies count | (OK) director vs number of movies | (OK) director vs imdb score
# (OK) comparision between budget and gross

# Data to be scrapped
# movie_title (original title), movie_year, plot_keywords, movie_facebook_likes, director_name, director_facebook_likes, actor_1_name
# actor_1_facebook_likes (the same for actor 2 and 3)

# Machine Learning
# Features: movie_facebook_likes, cast_facebook_likes? (director, actor1, actor2, actor3), plot_keywords? (assign a weight to each word?)
# Label: imdb_score
