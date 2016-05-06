#load users into list
#able to search user based on movie - use hash map
#for all movies seen

import math

def read_user_ratings(file_name):
	user_ratings = {}
	movies_ratings = {}
	not_seen_movies = [] #nested list to maintain movie ids not seen by each user
	training_file_names = [file_name]
	for file_names in training_file_names:
		training = open(file_names);
		not_seen_movies = []
		for line in training:
			values = line.split()
			if(user_ratings.has_key(values[0])):
				user_ratings[values[0]][values[1]] = values[2]
			else:
				user_ratings[values[0]] = {}
				user_ratings[values[0]][values[1]] = values[2]

			if movies_ratings.has_key(values[1]):
				movies_ratings[values[1]][values[0]] = values[2]
			else:
				movies_ratings[values[1]] = {}
				movies_ratings[values[1]][values[0]] = values[2]
		training.close()
	return user_ratings, movies_ratings

def avg_predict_rating(user_ratings, dist, movie_id, k):
	total_sum = 0
	distances = dist.keys()
	distances.sort()
	if(len(distances)>=k):
		distances = distances[-15:]
		for num in distances:
			total_sum+= int(user_ratings[str(dist[num])][str(movie_id)])
		avg = total_sum/float(k)
	else:
		for num in distances:
			total_sum+= int(user_ratings[str(dist[num])][str(movie_id)])
		avg = total_sum/float(len(dist))
	return avg



def calculate(user_ratings, movies_ratings,user_test_ratings, movies_test_ratings, naive_difference) :
	users = user_ratings.keys()
	users.sort()
	user_id_max = str(users[-1])
	movies = movies_ratings.keys()
	movies.sort()
	movie_id_max = str(movies[-1])
	for user in range(1, int(movie_id_max)+1):                                                          #for each user 'user'
		for movie_id in range(1, int(movie_id_max)+1):                                                    #for each movie in file
			if(user_ratings.has_key(str(user)) and (not user_ratings[str(user)].has_key(str(movie_id)))):   #'movie' which 'user' hasn't seen
				if(user_test_ratings.has_key(str(user)) and user_test_ratings[str(user)].has_key(str(movie_id)) and movies_ratings.has_key(str(movie_id))): 
					 																													#if movie is present in test set and someone has seen the movie
					print "user id is %d and movie is %d is MISSING"%(user, movie_id)
					potential_k_users = movies_ratings[str(movie_id)]                                           #users who have seen the 'movie'
					sum_ratings = 0
					avg_ratings = 0
					for potential_k_user in potential_k_users:                                                  #users who have seen the "to be predicted" movie
						sum_ratings = sum_ratings + float(user_ratings[str(potential_k_user)][str(movie_id)])     #calculate sum of ratings by users who have seen it
					avg_ratings = float(sum_ratings)/len(potential_k_users)
					naive_difference.append((abs(avg_ratings -float(user_test_ratings[str(user)][str(movie_id)]))))
					print "Naive Predicted value for user %d and movie %d is %f and true value is %s"%(user,movie_id, avg_ratings, user_test_ratings[str(user)][str(movie_id)])


def main():
	naive_difference = []
	files = ["u1.base", "u1.test", "u2.base", "u2.test", "u3.base", "u3.test", "u4.base", "u4.test", "u5.base", "u5.test"]  #change file names
	for i in range(0, len(files), 2):
		user_ratings, movies_ratings = read_user_ratings(files[i])
		user_test_ratings, movies_test_ratings = read_user_ratings(files[i+1])
		calculate(user_ratings, movies_ratings, user_test_ratings, movies_test_ratings, naive_difference)
		print "In file %s\n"%(files[i])
		#print users list
		#print "**Users**"
		#print user_ratings
		#print "**Movies**"
		#print movies ratings hash map
		#for key in movies_ratings:
		#	print key
		#	print movies_ratings[key]
		#print "**Test Users**"
		#print user_test_ratings
		#print "**Test Movies**"
		#print movies ratings hash map
		#for key in movies_test_ratings:
		#	print key
		#	print movies_test_ratings[key]
	naive_MAD = float(sum(naive_difference))/len(naive_difference)
	output_file =  open("naive.txt", 'w')
	output_file.write("Naive MAD %f"%(naive_MAD))
	output_file.write("\n")


main()