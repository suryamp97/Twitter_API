'''
@author: Souvik Das
Institute: University at Buffalo
'''

import json
import datetime
import pandas as pd
from twitter import Twitter
from tweet_preprocessor import TWPreprocessor
from indexer import Indexer

reply_collection_knob = True


def read_config():
    with open("config.json") as json_file:
        data = json.load(json_file)

    return data


def write_config(data):
    with open("config.json", 'w') as json_file:
        json.dump(data, json_file)


def save_file(data, filename):
    df = pd.DataFrame(data)
    df.to_pickle("data/" + filename)


def read_file(type, id):
    return pd.read_pickle(f"data/{type}_{id}.pkl")


def main():
    config = read_config()
    indexer = Indexer()
    twitter = Twitter()

    pois = config["pois"]
    keywords = config["keywords"]
    
    reply_count = 0
    poi_tweets = 0
    vaccine_tweets = 0
#     for i in range(len(pois)):
#         if pois[i]["finished"] == 0:
#             print(f"---------- collecting tweets for poi: {pois[i]['screen_name']}")
#             screen_name = pois[i]['screen_name']
#             raw_tweets = twitter.get_tweets_by_poi_screen_name(screen_name)  # pass args as needed

#             processed_tweets = []
#             for tw in raw_tweets:
#                 processed_tweets.append(TWPreprocessor.preprocess(tw,"poi"))

#             print(len(processed_tweets),pois[i]["screen_name"])
#             poi_tweets=poi_tweets+len(processed_tweets)
            
#             indexer.create_documents(processed_tweets)

#             pois[i]["finished"] = 1
#             pois[i]["collected"] = len(processed_tweets)

#             write_config({
#                 "pois": pois, "keywords": keywords
#             })

#             #save_file(processed_tweets, f"poi_{pois[i]['id']}.pkl")
#             print("------------ process complete -----------------------------------")
#     print("poi_tweets_7500 : ",poi_tweets)
#     for i in range(25,len(keywords)):
#         if keywords[i]["finished"] == 0:
#             print(f"---------- collecting tweets for keyword: {keywords[i]['name']}")
#             keyword = keywords[i]['name']
#             raw_tweets = twitter.get_tweets_by_lang_and_keyword(keyword)  # pass args as needed

#             processed_tweets = []
#             for tw in raw_tweets:
#                 processed_tweets.append(TWPreprocessor.preprocess(tw,"kw"))
#             print(len(processed_tweets),keywords[i]["name"])
#             vaccine_tweets=vaccine_tweets+len(processed_tweets)
            
#             indexer.create_documents(processed_tweets)

#             keywords[i]["finished"] = 1
#             keywords[i]["collected"] = len(processed_tweets)

#             write_config({
#                 "pois": pois, "keywords": keywords
#             })

#             #save_file(processed_tweets, f"keywords_{keywords[i]['id']}.pkl")

#             print("------------ process complete -----------------------------------")
#     print("vaccine_tweets_32500 : ",vaccine_tweets)
    if reply_collection_knob:
        for i in range(15):

            screen_name = pois[i]['screen_name']
            raw_tweets = twitter.get_replies(screen_name,keywords)  # pass args as needed

            processed_tweets = []
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw,"reply"))
                
            print("reply tweets count: ")
            print(len(processed_tweets),pois[i]["screen_name"])
            reply_count=reply_count+len(processed_tweets)
            indexer.create_documents(processed_tweets)

            print("------------ process complete -----------------------------------")

    print("total replies: ", reply_count);
if __name__ == "__main__":
    main()
