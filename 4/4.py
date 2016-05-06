#for n = 100, 1000 and 10000
#  for k=1 to 100
#     data_point = [n][k]

import random
import math
#import matplotlib.pyplot as plt

def print_matrix(data_points):
	#print "printing matrix"
	for row in data_points:
		print row
		print "\n"
	#print "DONE"
	return

def calculate_distance(data_points, n, k, rk, output_file):
	#print "received args n={a} and k={b}".format(a=n,b=k)
	i = j = l = 0
	dist = 0
	dmax = -1 
	dmin = 99
	#rk = []
	for i in range(n+1):
		j=0
		for j in range(n+1):
			if i!=j:
				dist = 0
				l = 0
				while l<=k:
					dist += (data_points[i][l] - data_points[j][l])**2
					l+=1
				#print "dist between before %d and %d is  is %f"%(i, j, dist)
				dist = math.sqrt(dist)
				#if k==0:
				#	print "dist between %d and %d is  is %f"%(i, j, dist)
				if(dist<dmin):
					dmin = dist
				elif(dist>dmax):
					dmax = dist
	dist = (math.log10((dmax-dmin)/dmin))
	rk.append(dist)
	print "k = %d, max is %f, dmin is %2.5f and rk is %2.8f"%(k, dmax, dmin, rk[-1])
	output_file.write("%d,%2.8f"%(k,rk[-1]))
	output_file.write("\n")
	output_file.flush()
	#print "verify %2.8f"%(dist)
	return rk

def plot(rk):
	k = []
	k = list(range(1,101))
	plt.plot(k, rk)
	plt.axis([1,100,-10, 10])
	plt.show()


def generate(num, output_file):
	#num=1000
	attributes = 100
	i=0
	rk = []
	data_points = [0]*num
	
	for k in range(attributes):
		for n in range(num):
			i=0
			data_points[n] = []
			while (i <= k):
				#print "i %d"%(i)
				data_points[n].append(random.random())
				i+=1
		rk = calculate_distance(data_points,n,k, rk, output_file)
	#plot(rk)
	return 

def main():
	i=0
	#output_file
	num_of_data_points = [100, 1000, 10000]
	file_names = ["100_debug.txt","1000_debug.txt", "10000_debug.txt"]
	for num in num_of_data_points:
		output_file = open(file_names[i],'w')
		generate(num,output_file)
		i+=1
		output_file.close()

main()