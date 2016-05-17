import math, json

# use when the data is dense, ie, it has non-zero values (faster, but slightly less accurate)
def manhattan_distance(lst1, lst2):
        dist = [abs(lst1[x] - lst2[x]) for x in lst1 if x in lst2 if (lst1[x] !=0 and lst2[x] != 0)]
        return sum(dist)

# use when the data is dense, ie, it has non-zero values (slower, but more accurate)
def euclidean_distance(dic1, dic2):
        dist = [(dic1[x] - dic2[x])**2 for x in dic1 if x in dic2 if (dic1[x] !=0 and dic2[x] != 0)]
        return sum(dist)**0.5

# use when different users may be using different scales of measurement
def pearson_correlation(x, y):
	x_bar = sum(x.values())/len(x)
	y_bar = sum(y.values())/len(y)
	numerator = 0
	sum_root_x = 0
	sum_root_y = 0
	counter = 0

	for key in x:
		if key in y:
			counter += 1
			numerator += (x[key] - x_bar) * (y[key] - y_bar)
			sum_root_x += ((x[key] - x_bar)**2)
			sum_root_y += ((y[key] - y_bar)**2)

	if counter == 0:
		return 0
	else:
		return numerator/((sum_root_x**0.5) * (sum_root_y**0.5))

# use when the data is sparse, ie, when there are zero/blank values
def cosine_similarity(dic1, dic2):
	magnitude_dic1 = 0
	magnitude_dic2 = 0
	sqr_sum1 = 0
	sqr_sum2 = 0
	dot_product = 0
	cosine_val = 0
	
	for i in dic1.values():
		sqr_sum1 += i**2
	
	for i in dic2.values():
		sqr_sum2 += i**2
	
	for i, j in zip(dic1.values(), dic2.values()):
		dot_product += i * j
	
	magnitude_dic1 = sqr_sum1**0.5
	magnitude_dic2 = sqr_sum2**0.5
	
	return dot_product/(magnitude_dic1 * magnitude_dic2)


def k_nearest_neighbour(email, other_emails, k, algorithm):
	if algorithm == 1:
		closeList = [(manhattan_distance(other_emails[email], other_emails[i]), i) for i in other_emails]
		return sorted(closeList, key = lambda lst: lst[0])[1:k+1]
		
	elif algorithm == 2:
		closeList = [(euclidean_distance(other_emails[email], other_emails[i]), i) for i in other_emails]
		return sorted(closeList, key = lambda lst: lst[0])[1:k+1]
	
	elif algorithm == 3:
		closeList = [(pearson_correlation(other_emails[email], other_emails[i]), i) for i in other_emails]
		return sorted(closeList, key = lambda lst: lst[0])[len(closeList)-(k+1):-1][::-1]
	
	elif algorithm == 4:
		closeList = [(cosine_similarity(other_emails[email], other_emails[i]), i) for i in other_emails]
		return sorted(closeList, key = lambda lst: lst[0])[len(closeList)-(k+1):-1][::-1]

# takes a list of recommended_list - ('user', score, 'event', rating) and returns predicted value
def event_judge(recommended_list):
	sum_algo_return = 0
	user_percent = []
	predicted_rating = 0
	
	for i in range(len(recommended_list)):
		sum_algo_return += recommended_list[i][1]
	
	for i in range(len(recommended_list)):
		user_percent.append((recommended_list[i][0], recommended_list[i][1] / sum_algo_return))
	
	for i in range(len(recommended_list)):
		predicted_rating += recommended_list[i][3] * user_percent[i][1]
	
	return predicted_rating

# uses event_judge to test if list of events are over the required limit
def test(lst_of_event):
	new_recommendation = {}
	for i in range(len(lst_of_event)):
		if (event_judge(lst_of_event[i])) > 3:
			new_recommendation['event'+str(i+1)] = lst_of_event[i][2]
	return json.dumps(new_recommendation)

# sort the list of tuples in ascending order by event
def sort_events(lst_of_event):
	return test(sorted(lst_of_event, key = lambda vent: vent[2], reverse=True))
	

# find the closest neighbour
def closestNeighbour(email, other_emails, algorithm):
	if algorithm == 1:
		closeList = [(manhattan_distance(other_emails[email], other_emails[i]), i) for i in other_emails]
		return sorted(closeList, key = lambda lst: lst[0])[1:]
		
	elif algorithm == 2:
		closeList = [(euclidean_distance(other_emails[email], other_emails[i]), i) for i in other_emails]
		return sorted(closeList, key = lambda lst: lst[0])[1:]
	
	elif algorithm == 3:
		closeList = [(pearson_correlation(other_emails[email], other_emails[i]), i) for i in other_emails]
		return sorted(closeList, key = lambda lst: lst[0])[1:-1][::-1]
	
	elif algorithm == 4:
		closeList = [(cosine_similarity(other_emails[email], other_emails[i]), i) for i in other_emails]
		return sorted(closeList, key = lambda lst: lst[0])[1:-1][::-1]

# recommend based on closest neighbour
def ratings_recommender(email, other_emails, algorithm):
	closest = closestNeighbour(email, other_emails, algorithm)[0][1]
	lst = [(key, val) for key, val in other_emails[closest].items() if key not in other_emails[email]]
	return sorted(lst, key = lambda based_on_val: based_on_val[1], reverse = True)