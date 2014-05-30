import re
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


''' Loads tweets to a simple dictionary based on a label.If neutral is true it will also include
    a neutral wordlist. 
    Else it will be only a list of positive and negative tweets. 
'''
def tweets_to_tweetlist(filename,tweetindex =3,labelindex=2, neutral = False):
    # The keys are specific for the SemEval dataset keys
    data_dictionary = {}
    trainSet = open(filename).readlines()
   
    if neutral:
       for line in trainSet:
            data = line.split('\t')
            tweet = parse_tweet(data[tweetindex])
            data_dictionary[tweet] = get_normal_label(data[labelindex])
    else:
        for line in trainSet:
            data = line.split('\t')
            if data[labelindex] != 'neutral':
                tweet = parse_tweet(data[tweetindex])
                data_dictionary[tweet] = get_normal_label(data[labelindex])
                 
    return data_dictionary

''' Loads a file directly to a dictionary with wordlists. If neutral is true it will make a neutral wordlist. 
    Else it will be only a list of positive and negative tweets. 
'''
def tweets_to_wordlist(filename, tweetindex=3, labelindex=2, neutral = False):
     
     trainSet= open(filename).readlines()
     data_dictionary = {'positive':[], 'negative':[]}
     
     if neutral:
        data_dictionary['neutral'] = []
        for line in trainSet:
            data = line.split('\t')
            tweet = parse_tweet(data[tweetindex], False)
            data_dictionary[data[labelindex]].extend(tweet)
     else:
        for line in trainSet:
            data = line.split('\t')
            if data[labelindex] != 'neutral':
                tweet = parse_tweet(data[tweetindex], False)
                data_dictionary[data[labelindex]].extend(tweet)
     
     return data_dictionary

''' Outputs a file cleaned of stopwords and punctuation
'''
def write_to_file(data_dictionary, filename):
    f = open(filename, "w")
    tweets = data_dictionary.values()
    for tweet, label in tweets:
        f.write(label)        
        f.write("\t")
        f.write(tweet)
        f.write("\n")
    f.close()

    return "Done writing"
    
''' Normalizes the label to a numerical form
'''    
def get_normal_label(label):
    if label == 'positive':
        return 1
    elif label == 'negative':
        return 0
    else:
        return 2  
'''Cleans stopwords,based on the NLTK stopword corpus
'''
def clean_stopwords(tweet):
    cleaned_tweet = []    
    stops = stopwords.words('english')
    
    for word in tweet:
        word = word.lower()
        if word not in stops: 
            cleaned_tweet.append(word)
    return cleaned_tweet
''' Replaces smileyis in a tweet
'''
def replace_smiley(tweet_string):
    happy_smileys = """:-) :) :o) :] :3 :c) :> =] 8) =) :} :^) 
             :D 8-D 8D x-D xD X-D XD =-D =D =-3 =3 B^D""".split()
    sad_smileys = ''':-( :( :o( :[ :3 :c( :< =[ 8( =( :{ :^('''.split()
    
    for smiley in sad_smileys:
        if smiley in tweet_string:
            tweet_string += ' NEGSMILEY'
    
    for smiley in happy_smileys:
        if smiley in tweet_string:
            tweet_string += ' POSSMILEY'
    return tweet_string
    
''' Parses a tweet. Used in preprocessing. If true returns the tweet as one string.
    Otherwise it returns it as a list of words. The regexp part is used to append the negative words 
    with _neg - see report for details
'''
def parse_tweet(tweet_string, one_string = True):
    tokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+')
    
    tweet_string = replace_smiley(tweet_string)
    if one_string:
        tweet = tokenizer.tokenize(tweet_string)
    
        cleaned_tweet = ""
        for word in clean_stopwords(tweet):
            cleaned_tweet = cleaned_tweet + " "  + word
            cleaned_tweet = re.sub(r'\b(?:not|never|no|hardly|barely|can\'t|cant|cannot|won\'t|wont|shouldn\'t|shouldnt|isn\'t|isnt|aren\'t|arent)\b[\w\s]+',
                          lambda match: re.sub(r'(\s+)(\w+)', r'\1NEG_\2', 
                          match.group(0)), cleaned_tweet, flags=re.IGNORECASE)    
        return cleaned_tweet
     
    else:
        tweet_string = re.sub(r'\b(?:not|never|no|hardly|barely|can\'t|cant|cannot|won\'t|wont|shouldn\'t|shouldnt|isn\'t|isnt|aren\'t|arent)\b[\w\s]+',
                          lambda match: re.sub(r'(\s+)(\w+)', r'\1NEG_\2', 
                          match.group(0)), tweet_string, flags=re.IGNORECASE)
        return tokenizer.tokenize(tweet_string)

