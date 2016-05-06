import random
import math
#import matplotlib.pyplot as plt

def calculate_distance(data_points, n, k, rk):
	i = j = l = 0
	dist = 0
	dmax = -1 
	dmin = 99
	for i in range(n+1):
		j=0
		for j in range(n+1):
			if i!=j:
				dist = 0
				l = 0
				while l<=k:
					dist += (data_points[i][l] - data_points[j][l])**2
					l+=1
				dist = math.sqrt(dist)
				if(dist<dmin):
					dmin = dist
				elif(dist>dmax):
					dmax = dist
	print "dmin %f, dmax %f"%(dmin, dmax)
	dist = (math.log10((dmax-dmin)/dmin))
	return dist

def plot(rk):
	k = []
	k = list(range(1,101))
	plt.plot(k, rk)
	plt.axis([1,100,-10, 10])
	plt.show()


def generate(num, output_file):
	attributes = 100
	i=0
	rk = []
	data_points = [0]*num
	
	for k in range(attributes):
		total_dist = 0
		for repeat in range(0,10):         # for each 'k' repeat the experiment for 10 times to get stable values
			for n in range(num):
				i=0
				data_points[n] = []
				while (i <= k):
					data_points[n].append(random.uniform(0,1))
					i+=1
			total_dist += calculate_distance(data_points,n,k, rk)
		print "%d:%f"%(k,(total_dist/float(10)))
		rk.append(total_dist/float(10))
		output_file.write("%d,%f\n"%(k,rk[-1]))
		output_file.flush()
	#plot(rk)
	return 

def main():
	i=0
	num_of_data_points = [100,1000, 10000]
	file_names = ["100_debug2.txt","1000_debug2.txt", "10000_debug2.txt"]
	for num in num_of_data_points:
		output_file = open(file_names[i],'w')
		generate(num,output_file)
		i+=1
		output_file.close()

main()