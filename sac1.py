from igraph import *
import csv
import numpy as np
import math
import random
import timeit

def draw():
	f = open('data/fb_caltech_small_edgelist.txt', 'r')
	string =  f.read()
	l = string.split('\n') 
	edges = []
	for elmt in l:
		if elmt != '':
			temp = elmt.split(' ')
			edge = (int(temp[0]),int(temp[1]))
			#print edge
			edges.append(edge)
	#print edges

	g = Graph(edges)

	ifile  = open('data/fb_caltech_small_attrlist.csv', "rb")
	reader = csv.reader(ifile)

	for row in reader:
		attrs = row
		break
	#print attrs
	matrix = np.loadtxt(ifile,delimiter=",",skiprows=0,dtype= int)
	ifile.close()

	#print matrix[:,0]
	#print len(matrix[:,0])
	attrnum = 0
	for attr in attrs:
		g.vs[attr] = matrix[:,attrnum]
		attrnum += 1
	#print attrnum
	#print g.vs[10]['year0']
	#print g.vs[10]['gender2']
	return g

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
	#print 'coSimA',coSimA
	return coSimA

def attr(graph,vertices,commu):
	Qattr = 0
	for vertice in vertices:
		for v in commu:
			Qattr += coSimA(graph, v, vertice)
	#print len(commu)
	return Qattr/(len(commu)*len(commu))


def newman(graph,vertices,commu):
	sum1 = 0
	sum2 = 0
	m = graph.ecount()
	Qnewman = 0
	for vertice in vertices:
		dx = vertice.degree()
		for v in commu:
			if graph.get_eid(v.index, vertice.index, directed=False, error=False)>-1:
				sum1 += 1
			sum2 += v.degree()
		Qnewman += float(1)/(2*m)*(sum1-(float(dx)/(2*m))*sum2)
	return Qnewman


def phase1(g,alpha,interation):
	commus = [[g.vs[i]] for i in range(0,g.vcount())]
	count = 0
	nodes = commus
	repeatNum = 0
	afterNodeNum = len(nodes)
	pickedNodes = []
	while (len(nodes) != 0 and repeatNum<len(nodes) and count <interation):
		temp = ([nd for nd in nodes if nd not in pickedNodes])
		node = random.choice(temp)
		highest = float("-inf")
		for index,commu in enumerate(commus, start=0):	
			Q1 = newman(g,node,commu)
			Q2 = attr(g,node,commu)/(len(commus)*len(commus))
			gain = alpha*Q1 + (1-alpha)*Q2
			if gain >= highest:
				highest = gain
				highIndex = index	
				highCommu = commu	
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
		nodes = [c for c in commus if len(c)==1]
	return commus

def phase2(g,alpha,commus):	
	count = 0
	nodes = commus
	repeatNum = 0
	afterNodeNum = len(nodes)
	pickedNodes = []
	interation = 15
	while (len(nodes) != 0 and repeatNum<len(nodes) and count <interation):
		temp = ([nd for nd in nodes if nd not in pickedNodes])
		node = random.choice(temp)
		highest = float("-inf")
		for index,commu in enumerate(commus, start=0):	
			Q1 = newman(g,node,commu)
			Q2 = attr(g,node,commu)/(len(commus)*len(commus))
			gain = alpha*Q1 + (1-alpha)*Q2
			if gain >= highest:
				highest = gain
				highIndex = index	
				highCommu = commu	
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

def summarize(commus):
	print 'here'
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
	start = timeit.default_timer()

	g = draw()
	alpha = 0.5
	interation = 15

	commus1 = phase1(g,alpha,interation)
	commus2 = phase2(g,alpha,commus1)
	# nu = len(commus2)
	# for item in commus2:
	# 	if len(item)!=1:
	# 		nu += len(item)
	# 		print 'len',len(item)
	# 		nu -= 1
	summarize(commus2)


if __name__ == "__main__":
    main()
