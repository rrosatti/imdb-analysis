import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

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

	plt.show()
