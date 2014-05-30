import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

''' Returns only words that have a frequency higher than the given treshold
'''
def get_significant_words(frequency_dict, threshold):
    cleaned = {}    
    for key in frequency_dict.keys():
        if frequency_dict[key] > threshold:
            cleaned[key] = frequency_dict[key]
    return cleaned
    
''' Finds the n most significant bigrams in the wordlists. Default value is 20.
    Currently not used
    Taken from http://streamhacker.com/2010/05/24/text-classification-sentiment-analysis-stopwords-collocations/
'''   
def get_siginficant_bigrams(tweet_list, score_fn=BigramAssocMeasures.chi_sq, n=20):
    #import itertools   
    from nltk.tokenize import word_tokenize
    bigstring = concatenate_tweets(tweet_list)
    bigram_finder = BigramCollocationFinder.from_words(word_tokenize(bigstring))
    bigrams = bigram_finder.nbest(score_fn, n)
    
    return bigrams
    
''' Turns bigrams into a single string. 
'''
def parse_bigrams(bigrams):
    parsed_bigrams = []
    for bigram in bigrams:
        parsed_bigrams.append(bigram[0] + " " + bigram[1])
    return parsed_bigrams
    
''' Concatenates the tweets so that the bigram classifier can handle them.
'''
def concatenate_tweets(tweet_list):
    bigstring = ""    
    for tweet in tweet_list:
        bigstring = bigstring + "\n"  + tweet
    return bigstring
    
''' Normalizes the score of the frequency of each word using min_max normalization. 
    N refers to the cutoff point - if a word has frequency lower than that it is ommited  
'''
def normalize_wordlist(wordlist, new_min = 0, new_max = 1, n = 25):
    normalized = {}    
    frequency = get_significant_words(nltk.FreqDist(wordlist), n)
    
    min_val_key = min(frequency, key = frequency.get)
    min_val = frequency[min_val_key]
    max_val_key = max(frequency, key = frequency.get)    
    old_range =  frequency[max_val_key] - min_val
    
    for word in frequency.keys():
        vi = frequency[word]
        normalized[word] = (float(vi - min_val)/(old_range))*(new_max - new_min) + new_min

    return normalized
    
''' Returns the final lexicon.
'''
def get_ratioDict(positive_words,negative_words, n):
    #final ratio dictionary
    ratioDict = {}
    #normalizing the words
    normalized_positive_words = normalize_wordlist(positive_words)
    normalized_negative_words = normalize_wordlist(negative_words)
    # computing final weight and adding to dictionary
    for word in normalized_positive_words.keys():
       if word in normalized_negative_words.keys():
             ratioDict[word] = normalized_positive_words[word] - normalized_negative_words[word]
       else:
            ratioDict[word] =  normalized_positive_words[word]
    
    ratio_keys = ratioDict.keys()
    #finally adding all the words that are missing from the above operation
    for word in  normalized_negative_words.keys():
        if word not in ratio_keys:
            ratioDict[word] = -1*normalized_negative_words[word]
    
    return ratioDict
    
''' Makes a prediction based on the sentiment lexicon. Df is the prediction rate. 
Change that to change which tweets get labelled as neutral
'''  
def predict(tweets,  lexicon, df = 0.5):
    predicted_tweets = {}
    for tweet in tweets:
        
        score = count_score(tweet.split(), lexicon)
        if  score > df:
            predicted_tweets[tweet] = 1
        elif score < -df:
            predicted_tweets[tweet] = 0
        else:
            predicted_tweets[tweet] = 2
    return predicted_tweets
'''Counts the score for each tweet, based on the word weight in the lexicon
'''
def count_score(tweet, lexicon):
    
    score = 0
    for word in tweet:
        if word in lexicon.keys():
            score += lexicon[word]
    return score
'''Returns tweets that have been deemed neutral. These are then passed to the SVM
'''    
def get_unclassified(labelled_tweets):
    
    unclassified_tweets = []
    for key in labelled_tweets.keys():
        if labelled_tweets[key] == 2:
            unclassified_tweets.append(key)
    return unclassified_tweets