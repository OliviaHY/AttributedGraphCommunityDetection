from igraph import *
import csv
import numpy as np
import math
import random
import timeit

# draw a graph using data/*
def draw():
	f = open('data/fb_caltech_small_edgelist.txt', 'r')
	string =  f.read()
	l = string.split('\n') 
	edges = []
	# read all the edges
	for elmt in l:
		if elmt != '':
			temp = elmt.split(' ')
			edge = (int(temp[0]),int(temp[1]))
			edges.append(edge)


	g = Graph(edges)

	ifile  = open('data/fb_caltech_small_attrlist.csv', "rb")
	reader = csv.reader(ifile)

	#save all attributes name to attrs
	for row in reader:
		attrs = row
		break
	#load the matrix contain all the nodes and their attributes
	matrix = np.loadtxt(ifile,delimiter=",",skiprows=0,dtype= int)
	ifile.close()
	
	#save all the attributes to its attribute name in the grahp
	attrnum = 0
	for attr in attrs:
		g.vs[attr] = matrix[:,attrnum]
		attrnum += 1
	return g

# calculate cosine similarity between two node
def coSimA(graph,vx,vy):
	v1 = vx.attributes().values()
	v2 = vy.attributes().values()
	sumxx, sumxy, sumyy = 0, 0, 0
	for i in range(0,len(v1)):
		x = v1[i]; y = v2[i]
		sumxx += x*x
		sumyy += y*y
		sumxy += x*y
	coSimA = float(sumxy)/math.sqrt(sumxx*sumyy)
	return coSimA

#calculate modularity attribute Qattr of two community
def attr(graph,vertices,commu):
	Qattr = 0
	for vertice in vertices:
		for v in commu:
			Qattr += coSimA(graph, v, vertice)
	return Qattr/(len(commu)*len(commu))

#calculate modularity structure Qnewman of two community
def newman(graph,vertices,commu):
	sum1 = 0
	sum2 = 0
	# m = the number of edges in the graph
	m = graph.ecount()
	Qnewman = 0
	for vertice in vertices:
		dx = vertice.degree()
		for v in commu:
			#sum up Gij (1 when this edge exists)
			if graph.get_eid(v.index, vertice.index, directed=False, error=False)>-1:
				sum1 += 1
			# expected number of connections
			sum2 += v.degree()
		Qnewman += float(1)/(2*m)*(sum1-(float(dx)/(2*m))*sum2)
	return Qnewman


def phase1(g,alpha,iteration):
	commus = [[g.vs[i]] for i in range(0,g.vcount())]
	count = 0
	nodes = commus
	repeatNum = 0
	afterNodeNum = len(nodes)
	pickedNodes = []
	# stop iterating when 
	#1, all the nodes have been included in a community with more than 1 node
	#2, could not move any node to any community
	#3, reach the iteration limit
	while (len(nodes) != 0 and repeatNum<len(nodes) and count <iteration):
		# randomly chose a node without repeat
		temp = ([nd for nd in nodes if nd not in pickedNodes])
		node = random.choice(temp)
		highest = float("-inf")
		for index,commu in enumerate(commus, start=0):	
			Q1 = newman(g,node,commu)
			Q2 = attr(g,node,commu)/(len(commus)*len(commus))
			# caculate the composite modularity gain
			gain = alpha*Q1 + (1-alpha)*Q2
			# record the community with highest gain
			if gain >= highest:
				highest = gain
				highIndex = index	
				highCommu = commu	
		# move the node with highest positive gain to target community
		if highest > 0:
			tempnode = node
			commus.remove(node)
			commus[highIndex-1] = commus[highIndex-1] + tempnode
			repeatNum = 0
			pickedNodes = []
			count+=1
			pickedNodes.append(node)
		else:	
			if count!= 0:
				repeatNum += 1
			pickedNodes.append(node)
		nodes = [c for c in commus if len(c)==1]
	return commus

# similar to phase1 except that input community is the result from phase 1
# and can pick not just node, community too in random choose 
def phase2(g,alpha,commus,iteration):	
	count = 0
	nodes = commus
	repeatNum = 0
	afterNodeNum = len(nodes)
	pickedNodes = []
	# stop iterating when 
	#1, all the nodes have been included in a community with more than 1 node
	#2, could not move any node to any community
	#3, reach the iteration limit
	while (len(nodes) != 0 and repeatNum<len(nodes) and count <iteration):
		# randomly chose a node without repeat
		temp = ([nd for nd in nodes if nd not in pickedNodes])
		node = random.choice(temp)
		highest = float("-inf")
		for index,commu in enumerate(commus, start=0):	
			Q1 = newman(g,node,commu)
			Q2 = attr(g,node,commu)/(len(commus)*len(commus))
			# caculate the composite modularity gain
			gain = alpha*Q1 + (1-alpha)*Q2
			if gain >= highest:
				highest = gain
				highIndex = index	
				highCommu = commu
		# move the node with highest positive gain to target community	
		if highest > 0:
			tempnode = node
			commus.remove(node)
			commus[highIndex-1] = commus[highIndex-1] + tempnode
			repeatNum = 0
			pickedNodes = []
			count+=1
			pickedNodes.append(node)
		else:
			pickedNodes.append(node)
			if count!= 0:
				repeatNum += 1
	return commus

# write all the communities to communities.txt
def summarize(commus):
	try:
		file = open('communities.txt','a')
		content = ''
		for commu in commus:
			temp = '\n'
			for node in commu:
				temp = temp+str(node.index)+','
			content += temp
		file.write(content[1:])
		file.close()
	except:
		print "Unexpected error:", sys.exc_info()[0]
		sys.exit(0)

def main():
	#g is the graph
	g = draw()
	# set alpha
	alpha = 0.5
	# set iteration number
	iteration = 15
	# run the graph through phase1 and 2
	commus1 = phase1(g,alpha,iteration)
	commus2 = phase2(g,alpha,commus1,iteration)
	# output communities.txt
	summarize(commus2)


if __name__ == "__main__":
    main()
