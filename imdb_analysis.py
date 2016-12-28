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


# Data Analysis
# (OK) imdb vs country |  imdb vs movie year |  imdb vs facebook popularity 
#  imdb vs director facebook popularity |  imdb vs cast facebook popularity
#  imdb vs genre |  genre vs movies count |  director vs number of movies |  director vs imdb score
#  comparision between budget and gross

df = iutil.get_dataset()
imdb_vs_country(df, False)
imdb_vs_movie_year(df, True)