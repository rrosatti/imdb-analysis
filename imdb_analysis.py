# the data is from: https://www.kaggle.com/deepmatrix/imdb-5000-movie-dataset
import pandas as pd
from collections import Counter
import numpy as np
import imdb_plot as iplot
import imdb_util as iutil
import math

data_path = 'C:/Users/rodri/OneDrive/Documentos/python/data/'

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

# return values of countries with at least 5 movies
def imdb_vs_country(df, plot=False):
	df2 = df[['country', 'imdb_score']]
	df2 = df2.groupby('country').agg(['mean', 'count'])
	df2.columns = ['imdb_mean', 'movies_count']
	df2 = df2.sort_values(by='imdb_mean', ascending=False)
	df2 = df2[ df2['movies_count'] > 4]
	if plot:
		iplot.plot_imdb_vs_country(df2)
	return df2

# return values of years with at least 5 movies
def imdb_vs_movie_year(df, plot=False):
	df2 = df[['imdb_score', 'title_year']]
	df2.dropna(inplace=True)
	df2 = df2.groupby('title_year').agg(['mean', 'count'])
	df2.columns = ['imdb_mean', 'movies_count']
	df2 = df2[ df2['movies_count'] > 4]
	if plot:
		iplot.plot_imdb_vs_movie_year(df2)
	return df2

# return only the movies with at least 1 facebook like (so, 'old' movies won't appear here)
def imdb_vs_movie_facebook_likes(df, plot=False):
	df2 = df[['movie_title', 'imdb_score', 'movie_facebook_likes']]
	df2.dropna(inplace=True)
	df2 = df2.sort_values(by='movie_facebook_likes', ascending=False)
	df2 = df2[ df2['movie_facebook_likes'] > 0]
	if plot:
		iplot.plot_imdb_vs_movie_facebook_likes(df2)
	return df2

# it will return the top20 most liked directors (by default)
def imdb_vs_director_facebook_likes(df, plot=False, top=20):
	df2 = df[['director_name', 'imdb_score', 'director_facebook_likes']]
	df2 = df2.groupby('director_name').agg('mean')
	df2 = df2.sort_values('director_facebook_likes', ascending=False)
	df2 = df2[ df2['director_facebook_likes'] > 0][:top]
	if plot:
		iplot.plot_imdb_vs_director_facebook_likes(df2)
	return df2

# it will return the top20 most liked casts (by default)
def imdb_vs_cast_facebook_likes(df, plot=False, top=20):
	df2 = df[['movie_title', 'imdb_score', 'cast_total_facebook_likes']]
	df2 = df2.sort_values('cast_total_facebook_likes', ascending=False)
	df2 = df2[ df['cast_total_facebook_likes'] > 0][:top]
	if plot:
		iplot.plot_imdb_vs_cast_facebook_likes(df2)
	return df2

# it will return the top 20 (default) directors that directed more movies
def director_vs_number_of_movies(df, plot=False, top=20):
	df2 = df[['director_name', 'movie_title', 'imdb_score']]
	df2 = df2.groupby('director_name')['movie_title', 'imdb_score'].agg(['count', 'mean'])
	df2.columns = ['movie_count', 'imdb_mean']
	df2 = df2.sort_values(by='movie_count', ascending=False)[:top]
	if plot:
		iplot.plot_director_vs_number_of_movies(df2)
	return df2

def get_movie_count_by_genre(df):
	genres_list = df['genres'].tolist()
	genre_counter = Counter()
	for genres in genres_list:
		g = genres.split('|')
		genre_counter.update(g)
	return genre_counter

# it will return the top 10 (default) most scored genres
def imdb_vs_genre(df, plot=False, top=10):
	df2 = df[['genres', 'imdb_score']]
	
	genres_list = df['genres'].tolist()
	imdb_score_list = df['imdb_score'].tolist()
	
	genre_counter = get_movie_count_by_genre(df)

	# get the imdb score sum for each genre
	imdb_sum_by_genre = {}
	for genres, imdb_score in zip(genres_list, imdb_score_list):
		for g in genres.split('|'):
			if imdb_sum_by_genre.get(g):
				imdb_sum_by_genre[g] += imdb_score
			else:
				imdb_sum_by_genre[g] = imdb_score
	
	# calculate the imdb score mean for each genre
	# reverse=True - Descending order
	imdb_mean_by_genre = {key: value/genre_counter[key] for (key, value) in imdb_sum_by_genre.items()}

	# sort dict: it will return a list of tuples
	sorted_genres = sorted(imdb_mean_by_genre.items(), key=lambda x:x[1], reverse=True)
	sorted_genres = sorted_genres[:top]
	
	if plot:
		iplot.plot_imdb_vs_genre(sorted_genres)
	return sorted_genres

def genre_vs_movie_count(df, plot=False, top=10):
	genre_movies_count = get_movie_count_by_genre(df)
	top_genres = genre_movies_count.most_common(top)
	if plot:
		iplot.plot_genre_vs_movie_count(top_genres)
	return top_genres

# return the top 20 (default) most scored directors (only the ones what has at least 3 movies on IMDB site)
def director_vs_imdb(df, plot=False, top=20):
	df2 = df[['director_name', 'movie_title', 'imdb_score']]
	df2 = df2.groupby('director_name')['movie_title', 'imdb_score'].agg(['count', 'mean'])
	df2.columns = ['movie_count', 'imdb_mean']
	df2 = df2.sort_values(by='imdb_mean', ascending=False)
	df2 = df2[ df2['movie_count'] > 2 ][:top]
	df2 = df2[['imdb_mean']]
	if plot:
		iplot.plot_director_vs_imdb(df2)
	return df2

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
	print(df2)
	return df2

def most_profitable_movies(df, plot=False, top=20):
	df2 = budget_vs_gross(df)
	df2 = df2.sort_values(by='profit', ascending=False)[:top]
	if plot:
		iplot.plot_most_profitable_movies(df2)
	return df2

# Data Analysis
# (OK) imdb vs country |  (OK) imdb vs movie year |  (OK) imdb vs facebook popularity 
# (OK) imdb vs director facebook popularity |  (OK) imdb vs cast facebook popularity
# (OK) imdb vs genre |  (OK) genre vs movies count | (OK) director vs number of movies | (OK) director vs imdb score
# (OK) comparision between budget and gross

df = iutil.get_dataset()
#imdb_vs_country(df, True)
#imdb_vs_movie_year(df, True)
#imdb_vs_movie_facebook_likes(df, True)
#imdb_vs_director_facebook_likes(df, True)
#imdb_vs_cast_facebook_likes(df, True)
#imdb_vs_genre(df, True)
#genre_vs_movie_count(df, True)
#director_vs_number_of_movies(df, True)
#director_vs_imdb(df, True)
most_profitable_movies(df, True)
