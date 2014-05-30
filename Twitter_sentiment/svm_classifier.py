''' This file implements the functions needed for the SVM classifier. 
Most of them are fairly straightforward.
'''
from sklearn.feature_extraction.text import CountVectorizer as cv
from sklearn import svm

''' GLobals. For some reason this is the only way to get the classifiers to work. 
'''
#    Vectorizes the words into a format suitable for proxessing
#    the ngram range shows the minimum and maximum number of ngrams it takes into account. 
vectorizer = cv(ngram_range=(1,2),token_pattern=r'\b\w+\b', min_df = 1)
svm = svm.LinearSVC()


def train(train_data, labels):
    global svm    
    svm.fit(train_data, labels)
    return
    
''' Returns the accuracy on a given dataset'''
def score(test_data, test_labels):
    global svm
    return svm.score(test_data, test_labels)
''' Predicts the class of the tweets passed as input.'''
def predict(test_data):
    return svm.predict(test_data)
    
''' Turns a set of tweets into it's corresponding vector. For more about vectorization see:
   http://en.wikipedia.org/wiki/Bag-of-words_model
'''
def vectorize_tweets(training_set,train = True):
    global vectorizer
    if train:    
        vectorizer.fit(training_set)
    processed_set = vectorizer.transform(training_set)
    
    return processed_set
