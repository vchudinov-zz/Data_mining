# -*- coding: utf-8 -*-
import numpy
import scipy.spatial as spat
"""
This file contains a k means clustering algorithm. 
For now it works only with variables with single values
@author: vvch

"""

class k_means_clustering:
    #  Constructor
    def __init__(self):
        self.clusters = {}
        self.cluster_centers = []
        return

    #   The actual algorithm. Takes arguments k and data, where k is the number of clusters
    def k_means(self, k, data):
        
        # 1. Generate Initial clusters
        self.cluster_centers = self.select_starting_points(data, k)

        # 2. Assign centroids
        self.clusters = self.assign_to_cluster(data,k + 1) 

        previous_centers = []        
        counter = 0

        # 3. Engage Loop
        while 1:
            previous_centers = [x for x in self.cluster_centers]            
                        
            #copy centers            
            # 3.a. Recalculate centers
            self.cluster_centers = self.compute_centers()
            
            # break condition - if there has been no change in the centroids, 
            # we have reached an optimum a
            if self.cluster_centers == previous_centers:
                print 'Clustering took %d steps' % (counter)
                break;
                
            # 3.b. Reassign items
            self.clusters = self.assign_to_cluster(data,k) 
            counter += 1
        return self.clusters
    
    # Computes the new centroids by taking the mean of the values in the variable
    def compute_centers(self):
        
        new_centers = []
        for cluster in self.clusters:        
            new_centers.append(numpy.mean(self.clusters[cluster]))
        
        return new_centers    

    # Assigns values to it's corresponding cluster
    def assign_to_cluster(self, data,k):
        # initialize an empty dict for the clusters
        c = {}        
        
        # get the keys for the dict and assign them
        keys = self.cluster_centers
        for key in keys:
            c[key] = []
        
        # assign the data points to their nearest corresponding centroid
        assigned_key = keys[0]
        
        for item in data:
            for key in keys:
                 if spat.distance.euclidean(item, key) < spat.distance.euclidean(item, assigned_key):
                     assigned_key = key
            c[assigned_key].append(item)
            
        return c
        
    # Randomly select the starting centroids from the possible data values. 
    def select_starting_points(self, data, k):
        maxrange = max(data)
        starting_centers = []        
        for i in range(k):
            center = numpy.random.randint(len(data))   
            center_1  = center
            # ensure that no two centroids are the same
            while center == center_1:
                center_1  = center
                center = numpy.random.randint(maxrange)
            starting_centers.append(center)
        
        return starting_centers
        
