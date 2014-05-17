import collections
import copy
import itertools
'''
Contains the apriori algorithm for finding patterns
TODO: implementing the support funcion for patterns with more than two elements

'''

def apriori(data, threshold ):
    # some random control stuff
    if threshold > len(data):
        return "You can't have a support larger than the database"
    elif threshold < 0:
        return "Negative numbers are not acceted"
    elif len(data) == 0:
        return "The database is empty"
    
    # generating the k = 1 set.         
    frequent_item_sets = generate_itemset_zero(data, threshold)
    
    while 1:    
        
        if len(frequent_item_sets) <= 0:
            frequent_item_sets = temp
            break                
        
        # at each step store a copy of the frequent itemsets of k-1. This 
        # is used so that the algorithm returns the last number of 
        # viable patterns and not an empty list
        
        #copy the current array
        temp = copy.copy(frequent_item_sets)        
        
        # generate next level of patterns
        frequent_item_sets = generate_frequent_itemsets(frequent_item_sets)
        
        #prune the patterns
        frequent_item_sets = prune(frequent_item_sets,data,threshold)

    return frequent_item_sets
 
#returns the confidence for a given pattern
def confidence(pattern, data):
    rules = powerset(pattern)
    valid_rules = []
    for i in rules:
       for j in rules:
           if i != j:
               valid_rules.append(rule_confidence(i,j,data))
    
    return valid_rules

# Returns the confidence of a rule.
def rule_confidence(A,B, data):
    rule_support = support((A+B), data)
    support_A = support(A, data)
    return float(rule_support)/float(support_A)
    
    

    
# Counts the support of a given pattern. 
def support( itemSet, dataset ):
        support = 0
        
        for item in dataset:
            flag = True
            for element in itemSet:
                if element not in item:
                    flag = False
            if flag:
                support +=1 
        return float(support)/len(dataset)

   
#Goes trough a k-1 itemset and generates candidates for k-length pattern
def generate_frequent_itemsets(lower_level_sets):
    
    candidates = []
    
    for index in range(len(lower_level_sets) -1):
        for second_index in range(index+1,len(lower_level_sets)):
            candidates.append(join_sets(lower_level_sets[index], lower_level_sets[second_index]))
    
    return candidates

#Removes the candidates that do not have enough support in the database.
def prune(candidates, data, treshold):
    
    pruned_cands = []
    
    for cand_set in candidates:
        
        if float(support(cand_set, data))/len(data) > treshold and not cand_set in pruned_cands and len(cand_set)>0:
            pruned_cands.append(cand_set)
    
    return pruned_cands

#joins two sets. The comparison between the k-th elements is != so that the function could handle strings
def join_sets( first_set, second_set ):
    
    result = []    
    
    if isinstance(first_set,list):    
        result.extend(first_set)
        if first_set[:-1] == second_set[:-1] and first_set[-1] != second_set[-1]:
            result.append(second_set[-1])
        else: return []
    else: 
        if first_set < second_set:
            result = [first_set,second_set]
    return result
  
#Flattens the database, counts the different items and generates the initial itemset  
def generate_itemset_zero(data, threshold):
    
    zero = []    
    candidates = count_db(data)
    for key in candidates.keys():
        if float(candidates[key])/float(len(data)) > threshold:
            zero.append(key)
    
    return zero

# counts the frequencies of the values in the database
def count_db(data):
    items = [value for element in data for value in element]
    return collections.Counter(items)
    
# Generates the possible rules combinations. Taken from the python documentation
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    powerset = []
    for i in itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(1,len(s))):
        powerset.append(list(i))
    return powerset
