''' This a main class of a sort.  See the second half of the document for the part that does anything.
'''
import dataset_loader as loader
import svm_classifier as svm
import sentiment_lexicon as sentlex
import numpy as np
import scipy.stats as stats

train_set = ''
lexicon_set = ''
test_set = ''
train_labels = ''
train_tweets = ''
lexicon = ''


def get_labels(tweets,dictionary):
    labels = []   
    for tweet in tweets:
        labels.append(dictionary[tweet])
    return labels

'''Calculates the accuracy of the results.
'''
def calculate_accuracy(predicted, actual):
    count = 0    
    for key in predicted.keys():
        if predicted[key] == actual[key]:
            count +=1
    return float(count)/len(predicted.keys())

''' Loads the tst and train set, trains the SVM and prepares the lexicon
'''   
def load_sets(training_file, test_file):
    global train_set, lexicon_set, test_set, train_labels, train_tweets, lexicon

    #Loading the training and lexicon sets
    train_set = loader.tweets_to_tweetlist(training_file, neutral = True)
    lexicon_set = loader.tweets_to_wordlist(training_file, neutral = False)
 
   #Loading the test set
    test_set = loader.tweets_to_tweetlist(test_file, neutral = True)
    
    #training the svm anlyzer
    train_labels = train_set.values()
    train_tweets = svm.vectorize_tweets(train_set.keys())
    svm.train(train_tweets, train_labels)

    #Building the lexicon
    lexicon = sentlex.get_ratioDict(lexicon_set['positive'], lexicon_set['negative'], 10)
    # Extracting the labels and tweets for train set and trnsforming the tweets into vectors
''' RUns a prediction. If lexicon only is true it returns only the lexicon prediction. 
'''
def predict(test_tweets, lexicon_only = False):
    global lexicon
    predicted_from_lexicon = sentlex.predict(test_tweets, lexicon)
    if lexicon_only:
        return predicted_from_lexicon
    undecided = sentlex.get_unclassified(predicted_from_lexicon)
    #undecided_labels = get_labels(undecided, test_set)

    undecided_transformed = svm.vectorize_tweets(undecided, False)
    predicted_from_svm = svm.predict(undecided_transformed)

    final = {}
    for i in range(len(undecided)):
        final[undecided[i]] = predicted_from_svm[i]
        predicted_from_lexicon.update(final)
    
    return predicted_from_lexicon

'''Runs a test on the test set. It divides the set in groups of 100 tweeets 
    and outputs a list with the accuracy on each set. 
    lexicon_only tells it if it should return olny the lexicon results
    same with SVM only
'''
def conduct_test(test_set, lexicon_only = False, svm_only = False, number_of_tweets = 3700):
    scores = []
    if  svm_only:
        for i in range(0,number_of_tweets,100):
            transformed = svm.vectorize_tweets(test_set.keys()[i:i+100], False)
            predicted = svm.score(transformed, test_set.values()[i:i+100])
            scores.append(predicted)
        transformed = svm.vectorize_tweets(test_set.keys()[number_of_tweets:len(test_set.keys())], False)
        predicted = svm.score(transformed, test_set.values()[number_of_tweets:len(test_set.keys())])
        scores.append(predicted)  
    else:
        for i in range(0,number_of_tweets,100):
             predicted = predict(test_set.keys()[i:i+100], lexicon_only) 
             expected = test_set.items()[i:i+100]
             scores.append(calculate_accuracy(predicted, dict(expected)))
        predicted = predict(test_set.keys()[number_of_tweets:len(test_set.keys())],lexicon_only)
        expected = test_set.items()[number_of_tweets:len(test_set.keys())]
        scores.append(calculate_accuracy(predicted, dict(expected)))
    return scores      
        
        
'''Returns the descriptive statistics of a list of results.
'''  
def get_stats(measures):
    descriptives = {}
    
    descriptives['mean'] = np.mean(measures)
    descriptives['median'] = np.median(measures)
    descriptives['std'] = np.std(measures)
    descriptives['min - max'] = (np.min(measures), np.max(measures))
    descriptives['number of samples'] = len(measures)
    global test_set
    descriptives['test set size'] = len(test_set.keys())
    descriptives['Shapiro normality'] = stats.shapiro(measures)
    return descriptives

###############################################################################
''' This part loads and runs the classifiers, prints statistics and conducts the t-tests
'''
#load sets
load_sets("train.train", "test.test")

#conduct experiments
print " SVM + Lexicon Analyzer: "
svm_lex = conduct_test(test_set, lexicon_only = False, svm_only = False)
print get_stats(svm_lex)
print "SVM only: "
svm_res = conduct_test(test_set, lexicon_only = False, svm_only = True)
print get_stats(svm_res)
print " Lexicon only: "
lex = conduct_test(test_set, lexicon_only = True, svm_only = False)
print get_stats(lex)

# Test equality of variances. We already know they're equal, so we're running the t-tests right away.
variance = stats.levene(svm_lex, svm_res,lex)
print variance

#t-tests
print "-------------------------"
print "T-test: SVM lexicon and svm only:"
print stats.ttest_rel(svm_lex,svm_res)
print "-------------------------"
print "T-test: SVM lexicon and lexicon"
print stats.ttest_rel(svm_lex,lex) 
print "--------------------------"
print "T-test: SVM only and lexicon:"
print stats.ttest_rel(svm_res, lex) 

print "T-test baseline(41.03: "
print "SVM lexicon: "
print stats.ttest_1samp(svm_lex, 41.03)
print "SVM: "
print stats.ttest_1samp(svm_res, 41.03) 
print "lexicon: "
print stats.ttest_1samp(lex, 41.03) 
