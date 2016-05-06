#Algorithm for 10M data set. It takes euclidean distance between the common movies seen by the users.

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
			values = line.split('::')
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
	l = k-(2*k)
	if(len(distances)>=k):
		distances = distances[l:]
		for num in distances:
			total_sum+= float(user_ratings[str(dist[num])][str(movie_id)])
		avg = total_sum/float(k)
	else:
		for num in distances:
			total_sum+= float(user_ratings[str(dist[num])][str(movie_id)])
		avg = total_sum/float(len(dist))
	return avg


def calculate(user_ratings, movies_ratings,user_test_ratings, movies_test_ratings,euclidean_difference, manhattan_difference, lmax_difference) :
	euclidean_dist = {}
	manhattan_dist = {}
	lmax_dist = {} 
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
					for potential_k_user in potential_k_users:                                                  #users who have seen the "to be predicted" movie
						temp_euclidean = temp_lmax = temp_manhattan = flag = 0                                    #movies seen by potential k users
						for his_movie in user_ratings[str(potential_k_user)].keys():
							if(user_ratings[str(user)].has_key(str(his_movie))):                                    #if 'user' has seen 'his_movie'
								difference = abs(float(user_ratings[str(user)][str(his_movie)])-float(user_ratings[str(potential_k_user)][str(his_movie)]))
								flag = 1
								temp_euclidean += (difference**2)
								if difference > temp_lmax:
									temp_lmax = difference
								temp_manhattan += difference
						if(flag == 1):
							euclidean_dist[math.sqrt(temp_euclidean)] = str(potential_k_user)
							manhattan_dist[temp_manhattan] = str(potential_k_user)
							lmax_dist[temp_lmax] = str(potential_k_user)
					predicted_value_euclidean = avg_predict_rating(user_ratings, euclidean_dist, movie_id, 10)
					predicted_value_manhattan = avg_predict_rating(user_ratings, manhattan_dist, movie_id, 10)
					predicted_value_lmax = avg_predict_rating(user_ratings, lmax_dist, movie_id, 10)
					euclidean_difference.append(abs(float(predicted_value_euclidean)-float(user_test_ratings[str(user)][str(movie_id)])))  #store |pij-tij|
					manhattan_difference.append(abs(float(predicted_value_manhattan)-float(user_test_ratings[str(user)][str(movie_id)])))  #store |pij-tij|
					lmax_difference.append(abs(float(predicted_value_lmax)-float(user_test_ratings[str(user)][str(movie_id)])))
					print "Euclidean Predicted value for user %d and movie %d is %f and true value is %s"%(user,movie_id, predicted_value_euclidean, user_test_ratings[str(user)][str(movie_id)])
					print "Manhattan Predicted value for user %d and movie %d is %f and true value is %s"%(user,movie_id, predicted_value_manhattan, user_test_ratings[str(user)][str(movie_id)])
					print "lmax Predicted value for user %d and movie %d is %f and true value is %s"%(user,movie_id, predicted_value_lmax, user_test_ratings[str(user)][str(movie_id)])
					euclidean_dist = {}
					manhattan_dist = {}
					lmax_dist = {}



def main():
	euclidean_difference = []
	manhattan_difference = []
	lmax_difference = []
	files = ["ra.train", "ra.test", "rb.train", "rb.test"]  #change file names
	for i in range(0, len(files), 2):
		user_ratings, movies_ratings = read_user_ratings("/l/b565/ml-10M100K/"+files[i])
		user_test_ratings, movies_test_ratings = read_user_ratings("/l/b565/ml-10M100K/"+files[i+1])
		calculate(user_ratings, movies_ratings, user_test_ratings, movies_test_ratings, euclidean_difference, manhattan_difference, lmax_difference)
		print "In file %s\n"%(files[i])
	euclidean_MAD = float(sum(euclidean_difference))/len(euclidean_difference)
	manhattan_MAD = float(sum(manhattan_difference))/len(manhattan_difference)
	lmax_MAD = float(sum(lmax_difference))/len(lmax_difference)
	output_file =  open("MAD_5c.txt", 'w')
	output_file.write("For 10M without any extra dimension")
	output_file.write("Euclidean MAD %f"%(euclidean_MAD))
	output_file.write("\n")
	output_file.write("Manhattan MAD %f"%(manhattan_MAD))
	output_file.write("\n")
	output_file.write("Lmax MAD %f"%(lmax_MAD))
	output_file.write("\n")


main()