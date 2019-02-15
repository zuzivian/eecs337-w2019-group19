from helpers import *

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_sentiment_of_tweets(tweet_list):
    sid = SentimentIntensityAnalyzer()
    sentiments = {}
    stopwords = get_stopwords() + ['red', 'carpet']
    for tweet in tweet_list:
        ss = sid.polarity_scores(tweet)
        names = extract_names(tweet)
        for name in names:
            name = name.lower()
            name = RemovePunctuation(name)
            if not IsLegalName(name):
                continue
            word = name.split(" ")
            if word[0] in stopwords or word[1] in stopwords:
                    continue
            if name not in sentiments.keys():
                sentiments[name] = (ss['compound'], 1)
            else:
                sentiments[name] = (sentiments[name][0]+ss['compound'], sentiments[name][1]+1)
    return sentiments
