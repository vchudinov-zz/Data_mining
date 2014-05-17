import numpy as np
import pandas as pd
import re

''' This class contains functions related to loading and preparing 
    data for analysis. This includes both normalization and data functions
'''

#   Loads data using the pandas' csv reader. 
#   In principle Panda returns it's own DataFrame object, but I did not use it.
#   Instead I preferd a dictinoary with a key - the name of the variable and 
#   value - an array of it's corresponding values
def load_data(filename):
    data = pd.read_csv(filename, sep = ";").to_dict()
    #data = data.to_dict()
    variables = data.keys()
    for variable in variables:
        data[variable] = variable_to_array(data, variable)
    return data

# Min-Max normalization
def normalize_min_max(variable, new_min = 0, new_max = 1):
    max_val = max(variable)
    min_val = min(variable)
     
    normalized = [((value - min_val)/(max_val - min_val))*(new_max - new_min) + new_min for value in variable]

    return normalized

# Normalizes a variable using a z-score    
def normalize_varibale_z_score(variable):

    mean = np.mean(variable)    
    sigma = np.std(variable)
    
    normalized = [(value - mean)/sigma for value in variable]
    
    return normalized

#    Counts missing values    
def count_missing(variable):
    return variable.count('')
    
# Counts the number of values in a variable    
def count_vals(variable):
    counts = {}
    for val in variable:
        if val not in counts.keys():
            counts[val] = variable.count(val)
    return counts

#   Replaces missing value with the supplied replacement value
def replace_missing(variable, replacement_value):
        
    for value in variable: 
        if value == '':
            value = replacement_value
    return True 

#    Replaces outliers with a max value
def cut_outliers(variable, boundary):
    
    for value in range(len(variable)):

        if variable[value] > boundary:
            variable[value] = boundary

    return variable

# Returns a variable as an array
def variable_to_array(data, variable):
    var = []
    for key in data[variable].keys():
        var.append(data[variable][key])
    
    return var
def clean_var_with_multiple_strings(variable):
    return [get_subvalues(value) for value in variable]

#   If a value consists of multiple elements, this function divides the elements and returns them as an array
def get_subvalues(variable):
    value = variable.split(',')
    return clean_string(value)
    
#   Strips whitespaces and symbols from a single value
def tokenize_value(val):
    return val.strip("?!',/\n()<>.;:#%*-+[]^ ").lower()

#   As with the previous function, but applied to an entire variable
def clean_string(variable):
    return [tokenize_value(v) for v in variable]

#    Encodes a boolean value. In this case it returns 1 if positive,
#    -1 if negative and 0 if neither. Obviously this can be changed 
#    according to preferences
def clean_boolean(variable):
    var = []
    for value in variable:
        if re.search('yes', value.lower()) != None:
            var.append(1)
        elif re.search('no', value.lower()) != None:
            var.append(-1)
        else:
            var.append(0)
    return var

# Cleans a numeric variable and replaces missing/invalid values with the median or mean of the variable
def clean_numeric(variable):
    variable = clean_string(variable)
    var = []
   
    for value in variable:
        v = re.findall(r'\b\d+\.?\d*\b', value)
        if len(v) == 0:
            var.append(0)
        else:
            v = v[0].replace(',','.')        
            var.append(float(v))
    median = np.median(var)
    #mean = np.mean(var)
    for v in range(len(var)):
        if var[v] == 0:
            var[v]+= median
       # v+= mean
    return var
  