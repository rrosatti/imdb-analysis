# the data is from: https://www.kaggle.com/deepmatrix/imdb-5000-movie-dataset
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from collections import Counter
import numpy as np

style.use('fivethirtyeight')

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

def plot_top_10_plot_keywords(c):
	labels = []
	values = []
	for con in c.most_common(10):
		labels.append(con[0])
		values.append(con[1])

	fig, ax = plt.subplots()
	N = len(values)
	index = np.arange(10)
	width = 0.35
	plt.bar(index, values, width, color='g', align='center')
	plt.title('Top 10 plot keywords')
	plt.xticks(index, labels)
	plt.show()

# return a df showing the movie title, imdb score and plot keywords of the top 20 imdb scores
def top_20_imdb_scores(df):
	df.sort_values(by='imdb_score', ascending=False, inplace=True)
	df.reset_index(inplace=True)
	top20 = df[['movie_title', 'imdb_score', 'plot_keywords']][:20]
	#print(top20)
	return top20

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

df = get_dataset()

plot_keywords = get_plot_keywords_count()
#plot_top_10_plot_keywords(plot_keywords)

#top_20_imdb_scores(df)
#group_by_imdb_score(df)
imdb_vs_country(df)

# imdb vs country | imdb vs movie year | imdb vs facebook popularity 
# imdb vs director facebook popularity | imdb vs actor/actresses facebook popularity

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