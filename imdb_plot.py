import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import math

style.use('fivethirtyeight')

# c - plot keywords Counter
def plot_top_x_plot_keywords(c, x=10):
	labels = []
	values = []
	for con in c.most_common(x):
		labels.append(con[0])
		values.append(con[1])

	fig, ax = plt.subplots()
	N = len(values)
	index = np.arange(x)
	width = 0.35
	plt.bar(index, values, width, color='g', align='center')
	plt.title('Top 10 plot keywords')
	plt.xticks(index, labels)
	plt.show()

# c - genres Counter
def plot_top_x_genres(c, x=10):
	# convert Counter to Dict
	c = dict(c)
	# sort the dict
	# reverse=True - Descending order
	sDict = sorted(c.items(), key=lambda x:x[1], reverse=True)
	xs = []
	ys = []
	
	for t in sDict[:x]:
		xs.append(t[0])
		ys.append(t[1])
	
	x2 = [i for i in range(len(xs))]
	
	fig = plt.figure()
	ax1 = plt.subplot2grid((1,1), (0,0))

	ax1.bar(x2, ys, label='Total Movies', color='g')
	plt.xticks(x2, xs)

	for label in ax1.xaxis.get_ticklabels():
		label.set_rotation(60)

	# show values of each bar
	rects = ax1.patches
	i = 0
	for rect in rects:
		height = rect.get_height()
		# ha = horizontal alignment  |  va = vertical alignment
		ax1.text(rect.get_x() + rect.get_width()/2, height + 5, ys[i], ha='center', va='bottom')
		i+=1
	
	plt.subplots_adjust(bottom=0.25)

	plt.xlabel('Genres')
	plt.ylabel('Movies count')
	plt.title('Movies by Genres')
	plt.legend()
	plt.show()

def plot_top_x_profitable_movies(df, x=20):
	fig = plt.figure()
	ax1 = plt.subplot2grid((1,1), (0,0))
	# get only the movie_title and profit columns. And only the X first rows
	df2 = df.sort_values(by='profit', ascending=False)[:x]
	df2 = df2.sort_values(by='profit')
	# removing the \xa0 from the movie titles 
	df2['movie_title'] = df2.apply(lambda x: x['movie_title'].replace('\xa0', ''), axis=1)
	xs = df2['movie_title'].tolist()
	ys = df2['profit'].tolist()
	
	x2 = np.arange(len(xs))

	ax1.barh(x2, ys, label='Profit', color='c')
	ax1.set_yticks(x2 + 0.3)
	ax1.set_yticklabels(xs)
	#plt.yticks(x2, xs, va='center')
	
	# show values of each bar
	for i, v in enumerate(ys):
		ax1.text(v*1.03, i + .15, str(v))

	plt.subplots_adjust(left=0.30)
	plt.xlabel('Profit')
	plt.title('Top '+str(x)+' profitable movies')
	plt.legend(loc=4)
	plt.show()

def plot_imdb_vs_country(df):
	print(df)
	fig = plt.figure()
	ax1 = plt.subplot2grid((2,1), (0,0), rowspan=1, colspan=1)
	plt.ylabel('Movie Count')
	ax2 = plt.subplot2grid((2,1), (1,0), rowspan=1, colspan=1, sharex=ax1)
	plt.ylabel('IMDB Mean')
	
	x = np.arange(len(df))
	xlabels = np.array(df.reset_index()['country'])
	y1 = np.array(df['imdb_mean'])
	y2 = np.array(df['movies_count'])

	ax1.bar(x, y2, color='g')
	plt.setp(ax1.xaxis.get_ticklabels(), visible=False)
	ax2.bar(x, y1, color='b')
	plt.xticks(x, xlabels)
	ax2.set_ylim([5,8])

	for label in ax2.xaxis.get_ticklabels():
		label.set_rotation(45)

	# show values of each bar
	rects = ax1.patches
	i = 0
	for rect in rects:
		height = rect.get_height()
		# ha = horizontal alignment  |  va = vertical alignment
		ax1.text(rect.get_x() + rect.get_width()/2, height + 5, y2[i], ha='center', va='bottom')
		i+=1
	
	plt.subplots_adjust(bottom=0.15)
	plt.legend()
	plt.title('IMDB Score vs Country')
	plt.show()

def plot_imdb_vs_movie_year(df):
	print(df)
	fig = plt.figure()
	ax1 = plt.subplot2grid((1,1), (0,0))
	ax2 = plt.twinx(ax1)

	x = np.array(df.reset_index()['title_year'])
	y1 = np.array(df['imdb_mean'])
	y2 = np.array(df['movies_count'])

	ax1.bar(x, y2, color='r', alpha=0.3)
	ax1.legend()
	ax1.set_ylabel('Movies Count')
	ax2.plot(x, y1, color='c')
	ax2.set_ylabel('IMDB Mean')
	ax2.legend(loc=2)

	ax1.set_xlabel('Years')
	plt.title('IMDB Score vs Movie Year')
	plt.show()

def plot_imdb_vs_movie_facebook_likes(df):
	print(df)
	fig = plt.figure()
	ax1 = plt.subplot2grid((1,1), (0,0))

	x = np.array(df['imdb_score'])
	y = np.array(df['movie_facebook_likes'])

	ax1.scatter(x, y, color='indigo')

	plt.xlabel('IMDB Score')
	plt.ylabel('Facebook Likes')
	plt.title('IMDB Score vs Movie Facebook Likes')
	plt.legend()
	plt.show()

def plot_imdb_vs_director_facebook_likes(df):
	print(df)
	fig = plt.figure()
	ax1 = plt.subplot2grid((1,1), (0,0))
	ax2 = ax1.twinx()

	x = np.arange(len(df))
	xlabels = np.array(df.reset_index()['director_name'])
	y1 = np.array(df['imdb_score'])
	y2 = np.array(df['director_facebook_likes'])

	ax1.bar(x, y2, color='seagreen', alpha=0.3, label='Facebook Likes')
	ax1.set_ylabel('Director Facebook Likes')

	ax1.set_xticks(x)
	ax1.set_xticklabels(xlabels, rotation=45)
	ax1.grid()

	ax2.plot(x, y1, color='darkcyan', ls='--', label='IMDB Score')
	ax2.set_ylabel('IMDB Score')
	ax2.set_ylim([1, df['imdb_score'].max()*1.1])

	# add legend for both charts
	charts1, labels1 = ax1.get_legend_handles_labels()
	charts2, labels2 = ax2.get_legend_handles_labels()
	ax2.legend(charts1+charts2, labels1+labels2, loc=0)

	plt.title('Top '+str(len(df))+' most liked directors on IMDB site', fontsize=15)
	plt.subplots_adjust(bottom=0.25)
	plt.show()

def plot_imdb_vs_cast_facebook_likes(df):
	print(df)
	fig = plt.figure()
	ax1 = plt.subplot2grid((1,1),(0,0))
	ax2 = ax1.twinx()

	x = np.arange(len(df))
	xlabels = np.array(df['movie_title'])
	y1 = np.array(df['cast_total_facebook_likes'])
	y2 = np.array(df['imdb_score'])

	ax1.bar(x, y1, color='lightcoral', label='Facebook Likes', alpha=0.3)
	ax1.set_ylabel('Cast Facebook Likes')

	ax1.set_xticks(x)
	ax1.set_xticklabels(xlabels, rotation=75)
	ax1.grid()

	ax2.plot(x, y2, color='maroon', label='IMDB Score', ls='--')
	ax2.set_ylabel('IMDB Score')
	ax2.set_ylim([1, df['imdb_score'].max()*1.1])

	charts1, labels1 = ax1.get_legend_handles_labels()
	charts2, labels2 = ax2.get_legend_handles_labels()
	ax2.legend(charts1+charts2, labels1+labels2, loc=0)

	plt.title('Top '+str(len(df))+' most liked casts on IMDB site', fontsize=15)
	plt.subplots_adjust(bottom=0.30)
	plt.show()

def plot_imdb_vs_genre(sorted_genres):
	print(sorted_genres)
	fig = plt.figure()
	ax1 = plt.subplot2grid((1,1), (0,0))

	xs = []
	ys = []

	for t in sorted_genres:
		xs.append(t[0])
		ys.append(t[1])

	x = np.arange(len(xs))

	ax1.bar(x, ys, color='chocolate', label='IMDB Score', width=0.45)
	ax1.set_ylabel('IMDB Score')
	ax1.set_xticks(x)
	ax1.set_xticklabels(xs, rotation=45, ha='center')
	ax1.set_ylim([np.min(ys)-1, np.max(ys)+1])

	# show values of each bar
	rects = ax1.patches
	i = 0
	for rect in rects:
		height = rect.get_height()
		# ha = horizontal alignment  |  va = vertical alignment
		ax1.text(rect.get_x() + rect.get_width()/2, height*1.01, '%.2f' % (ys[i]), ha='center', va='bottom')
		i+=1


	plt.legend()
	plt.title('Top '+str(len(sorted_genres))+' most scored genres', fontsize=16)
	plt.subplots_adjust(bottom=0.15)
	plt.show()

def plot_genre_vs_movie_count(top_genres):
	print(top_genres)
	fig = plt.figure()
	ax1 = plt.subplot2grid((1,1), (0,0))

	xs = []
	ys = []
	for t in top_genres:
		xs.append(t[0])
		ys.append(t[1])

	x = np.arange(len(xs))
	ax1.bar(x, ys, color='lightslategrey', label='Movie Count', width=0.45)
	ax1.set_xticks(x)
	ax1.set_xticklabels(xs, rotation=45, ha='left')

	# show values of each bar
	rects = ax1.patches
	i = 0
	for rect in rects:
		height = rect.get_height()
		ax1.text(rect.get_x() + rect.get_width()/2, height*1.01, ys[i], ha='center', va='bottom')
		i+=1

	plt.title('Top '+str(len(top_genres))+' genres by movie count', fontsize=16)
	plt.legend()
	plt.subplots_adjust(bottom=0.15)
	plt.show()

def plot_director_vs_number_of_movies(df):
	print(df)
	fig = plt.figure()
	ax1 = plt.subplot2grid((1,1), (0,0))
	ax2 = ax1.twinx()

	x = np.arange(len(df))
	xlabels = np.array(df.reset_index()['director_name'])
	y1 = np.array(df['movie_count'])
	y2 = np.array(df['imdb_mean'])

	ax1.bar(x, y1, color='mediumseagreen', label='Movie Count', width=0.6, alpha=0.3)
	ax1.set_ylabel('Movie Count')
	ax1.set_xticks(x)
	ax1.set_xticklabels(xlabels, rotation=60, ha='center')
	ax1.grid()

	ax2.plot(x, y2, color='darkslategray', label='IMDB Score', ls='--')
	ax2.set_ylabel('IMDB Score')
	ax2.set_ylim([df['imdb_mean'].min()-2, df['imdb_mean'].max()*1.1])

	# show values of each bar
	rects = ax1.patches
	i = 0
	for rect in rects:
		height = rect.get_height()
		ax1.text(rect.get_x() + rect.get_width()/2, height*1.01, y1[i], ha='center', va='bottom')
		i+=1

	charts1, labels1 = ax1.get_legend_handles_labels()
	charts2, labels2 = ax2.get_legend_handles_labels()
	ax2.legend(charts1+charts2 ,labels1+labels2, loc=0)

	plt.title('Top '+str(len(df))+' Directors by movie count', fontsize=15)
	plt.subplots_adjust(bottom=0.30, right=0.90)
	plt.show()

def plot_director_vs_imdb(df):
	print(df)
	fig = plt.figure()
	ax1 = plt.subplot2grid((1,1), (0,0))

	x = np.arange(len(df))
	xlabels = np.array(df.reset_index()['director_name'])
	y = np.array(df['imdb_mean'])

	ax1.bar(x, y, label='IMDB Mean', color='darkturquoise')
	ax1.set_xticks(x)
	ax1.set_xticklabels(xlabels, rotation=60, ha='center')
	ax1.set_ylim([df['imdb_mean'].min()-2, df['imdb_mean'].max()*1.1])

	rects = ax1.patches
	i = 0
	for rect in rects:
		height = rect.get_height()
		ax1.text(rect.get_x() + rect.get_width()/2, height*1.01, '%.2f' % (y[i]), ha='center', va='bottom')
		i+=1

	plt.ylabel('IMDB Score')
	plt.xlabel('Director')
	plt.legend()
	plt.subplots_adjust(bottom=0.3)
	plt.title('Top '+str(len(df))+' most scored directors on IMDB site\n(Only directors with at least 3 movies)', fontsize=15)
	plt.show()

def plot_most_profitable_movies(df):
	print(df)
	fig = plt.figure()
	ax1 = plt.subplot2grid((1,1), (0,0))

	width = 0.4 # the width of the bars

	x = np.arange(len(df))
	xlabels = np.array(df['movie_title'])
	y1 = np.array(df['budget'])
	y2 = np.array(df['gross'])
	y3 = np.array(df['profit'])

	ax1.bar(x, y2, label='Gross', color='lightgreen', width=width)
	ax1.bar(x, y1, label='Budget', color='khaki', width=width)
	ax1.bar(x + width, y3, label='Profit', color='lightblue', width=width)

	ax1.set_xticks(x + width)
	ax1.set_xticklabels(xlabels, rotation=82, ha='center')
	ax1.set_ylim([0, round(df['profit'].max()*1.7)])

	plt.ylabel('$ (100,000,000)')
	plt.title('Top '+str(len(df))+' most profitable movies')
	plt.legend()
	plt.subplots_adjust(bottom=0.35)
	plt.show()

