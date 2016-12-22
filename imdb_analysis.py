# the data is from: https://www.kaggle.com/deepmatrix/imdb-5000-movie-dataset
import pandas as pd
from collections import Counter
import numpy as np
import imdb_plot as iplot

data_path = 'C:/Users/rodri/OneDrive/Documentos/python/data/'

def get_dataset():
	df = pd.read_csv(data_path+'movie_metadata.csv')
	return df

def get_plot_keywords_count():
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
	#print(df2)
	return df2

df = get_dataset()

#plot_keywords = get_plot_keywords_count()
#iplot.plot_top_10_plot_keywords(plot_keywords)

#top_20_imdb_scores(df)
#group_by_imdb_score(df)
#imdb_vs_country(df)
#imdb_vs_movie_year(df)
#imdb_vs_movie_facebook_likes(df)
#imdb_vs_director_facebook_likes(df)
#imdb_vs_cast_facebook_likes(df)
#c = get_genres_count(df)
#iplot.plot_top_x_genres(c, 15)
#director_vs_number_of_movies(df)
df2 = budget_vs_gross(df)
iplot.plot_top_x_profitable_movies(df2)

# (OK) imdb vs country | (OK) imdb vs movie year | (OK) imdb vs facebook popularity 
# (OK) imdb vs director facebook popularity | (OK) imdb vs cast facebook popularity
# (OK) imdb vs genre | (OK) genre vs movies count | (OK) director vs number of movies | (OK) director vs imdb score
# comparision between budget and gross

















# Analysis of correlation


'''
fig = plt.figure()
ax1 = plt.subplot2grid((2,1), (0,0))
ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)

df.sort('imdb_score', ascending=False, inplace=True)
df.reset_index(inplace=True)
#print(df.head())

df['imdb_score'][:10].plot(ax=ax1, label='IMDB Score', color='g')
df['movie_facebook_likes'][:10].plot(ax=ax2, label='Movie Facebook Likes', color='y')

plt.legend(loc=4)
plt.show()

print(df.head())

'''