import math
'''
Contains the k-nearest enighbours classifier. At some point also the ID3. 
Troughout the file variables are as follows:

k - the number of neighbours
item/item_1/item_2 - values in the variables that we use for comparison. 
item and item_1 are the values we want to classify

Database is an array containing a vector of variables that is
 used for classifying the item on the basis of similarity
@author: vvch
'''

#   This is the version of the algorithm that works with categorical variables
#   Returns a dictionary, where the key is the rank of the neughbur.
#    The value is a tuple as  (index of the neighbour in the database. class of the neighbour, distance to the item)
def k_nearest_neighbours_categorical(k, item, database):
    neighbours = get_distances(item, database)
    results = {}
    for i in range(1,k+1):
        results[i] = ("index: " + str(neighbours[i][0])
        ,"class: " + str(database[neighbours[i][0]][-1])
        , "distance: " + str(neighbours[i][1]))
    return results

# This function average the score of the nearest neighbour in order to clasify the output more easily
def av_distance(k, item, database):
    # getting the k-nearest neighbours
    k_neighbours = get_distances(item, database)[:k]
    # and their indices    
    indices = []
    for i in k_neighbours:
        indices.append(i[0])
        
    # and returning the average of the class values
    classify = [database[i][-1] for i in indices]
    return float(sum(classify))/len(k_neighbours)

# returns the distance between two categorical variables
def categorical_distance(item_1, item_2):
    sigma = 0
    for i in range(len(item_1)-1):
        if item_1[i] == item_2[i]:
            sigma += 1
    return sigma/float(len(item_1)-1)

# Not currently in use but returns eucledian distances
def eucledian_distance(item_1, item_2):
        sigma = 0
        for i in range(len(item_1)):
            sigma += (item_1[i] - item_2[i])**2
        return math.sqrt(sigma/len(item_1))
# TODO: Manhattan distance        
def manhattan_distance(item_1, item_2):
    pass

# returns the sorted array of distances between the item and each element in the database
# returns a list of tuples in the form of (index of the item in the db, distance)       
def get_distances(item, database):
    dists = []   
    for index in range(len(database)):
        dists.append((index, categorical_distance(item, database[index])))
 
    return sorted(dists, key=lambda distance: distance[1], reverse = True)

    
            
        


