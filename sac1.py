from igraph import *
import csv
import numpy as np

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
print attrs
matrix = np.loadtxt(ifile,delimiter=",",skiprows=0,dtype= int)
ifile.close()

print matrix[:,0]
print len(matrix[:,0])
attrnum = 0
for attr in attrs:
	g.vs[attr] = matrix[:,attrnum]
	attrnum += 1
print attrnum
print g.vs[10]['year0']
print g.vs[10]['gender2']