from helpers import *
from TweetDatabase import TweetDatabase
from nltk import bigrams, trigrams
from math import pow


gg2013_categories = [
        u"Best Motion Picture - Drama",
        u"Best Motion Picture - Musical or Comedy",
        u"Best Performance by an Actress in a Motion Picture - Drama",
        u"Best Performance by an Actor in a Motion Picture - Drama",
        u"Best Performance by an Actress in a Motion Picture - Musical or Comedy",
        u"Best Performance by an Actor in a Motion Picture - Musical or Comedy",
        u"Best Performance by an Actress in a Supporting Role in any Motion Picture",
        u"Best Performance by an Actor in a Supporting Role in any Motion Picture",
        u"Best Director - Motion Picture",
        u"Best Screenplay - Motion Picture",
        u"Best Motion Picture - Animated",
        u"Best Motion Picture - Foreign Language",
        u"Best Original Score - Motion Picture",
        u"Best Original Song - Motion Picture",
        u"Best Television Series - Drama",
        u"Best Television Series - Musical or Comedy",
        u"Best Television Limited Series or Motion Picture Made for Television",
        u"Best Performance by an Actress in a Limited Series or a Motion Picture Made for Television",
        u"Best Performance by an Actor in a Limited Series or a Motion Picture Made for Television",
        u"Best Performance by an Actress In A Television Series - Drama",
        u"Best Performance by an Actor In A Television Series - Drama",
        u"Best Performance by an Actress in a Television Series - Musical or Comedy",
        u"Best Performance by an Actor in a Television Series - Musical or Comedy",
        u"Best Performance by an Actress in a Supporting Role in a Series, Limited Series or Motion Picture Made for Television",
        u"Best Performance by an Actor in a Supporting Role in a Series, Limited Series or Motion Picture Made for Television",
        u"Cecil B. deMille Award",
    ]

gg2015_categories = {
        "Best Motion Picture – Drama",
        "Best Motion Picture – Musical or Comedy",
        "Best Motion Picture – Foreign Language",
        "Best Motion Picture – Animated",
        "Best Director – Motion Picture"
        "Best Actor – Motion Picture Drama",
        "Best Actor – Motion Picture Musical or Comedy",
        "Best Actress – Motion Picture Drama",
        "Best Actress – Motion Picture Musical or Comedy",
        "Best Supporting Actor – Motion Picture",
        "Best Supporting Actress – Motion Picture",
        "Best Screenplay – Motion Picture",
        "Best Original Score – Motion Picture",
        "Best Original Song – Motion Picture",
        "Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures",
        "Best Television Series – Drama",
        "Best Television Series – Musical or Comedy",
        "Best Miniseries or Television Film",
        "Best Actor – Television Series Drama",
        "Best Actor – Television Series Musical or Comedy",
        "Best Actor – Miniseries or Television Film",
        "Best Actress – Television Series Drama",
        "Best Actress – Television Series Musical or Comedy",
        "Best Actress – Miniseries or Television Film",
        "Best Supporting Actor – Series, Miniseries or Television Film",
        "Best Supporting Actress – Series, Miniseries or Television Film",
        "Best Documentary Film",
        "Best English-Language Foreign Film",
        "New Star of the Year – Actor",
        "New Star of the Year – Actress",
        "Henrietta Award (World Film Favorite – Female)",
        "Henrietta Award (World Film Favorite – Male)",
        "Best Film Promoting International Understanding",
        "Golden Globe Award for Best Cinematography",
        }


def award_classifier(tweet_tokens, award_categories, token_dict, bigram_dict, trigram_dict):
    tweet_bigrams = list(bigrams(tweet_tokens))
    tweet_trigrams = list(trigrams(tweet_tokens))
    best_score = 0
    best_category = ""
    for award in award_categories:
        token_matches = num_matches(token_dict[award], tweet_tokens)
        bigram_matches = num_matches(bigram_dict[award], tweet_bigrams)
        trigram_matches = num_matches(trigram_dict[award], tweet_trigrams)
        score = 2 * token_matches + 2 * bigram_matches + 2 * trigram_matches
        if score > best_score and score > 12:
            best_score = score
            best_category = award
    return best_category

def num_matches(list1, list2):
    matches = 0
    for item in list1:
        matches += list2.count(item)
    return matches


'''
A script that classifies tweets into different award types
'''

db = TweetDatabase('./data/gg2013.json', 100000)
print("Extracting tweets...")
tweets = db.get_tweets()

print("Parsing awards...")
tweet_dict_by_award = {}
award_token_dict = {}
award_bigram_dict = {}
award_trigram_dict = {}
for award in gg2013_categories:
    tweet_dict_by_award[award] = []
    award_token = award.lower().split()
    award_token = strip_punctuation(award_token)
    award_bigram_dict[award] = list(bigrams(award_token))
    award_trigram_dict[award] = list(trigrams(award_token))
    award_token = remove_stopwords(award_token)
    award_token_dict[award] = award_token


print("Classifying tweets...")
for tweet in tweets:
    tokens = twitter_tokenize(tweet)
    tokens = strip_punctuation(tokens)
    # tokens = remove_stopwords(tokens)
    category = award_classifier(tokens, gg2013_categories, award_token_dict, award_bigram_dict, award_trigram_dict)
    if category:
        tweet_dict_by_award[category].append(tweet)

print("Printing results to file...")
date = datetime.datetime.now()
file = open(dir_path + '/output/' + str(date) + ".txt", "w")

d_view = [ (v,k) for k,v in tweet_dict_by_award.iteritems() ]
for twts, award in d_view:
    file.write("\n\n\n%s:\n" % award.encode('ascii', 'ignore'))
    for t in twts:
        file.write("%s\n" % t.encode('ascii', 'ignore'))
file.close()
