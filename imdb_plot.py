import matplotlib.pyplot as plt
from matplotlib import style

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
