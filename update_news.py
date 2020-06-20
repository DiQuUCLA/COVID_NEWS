import socket
import sys
import datetime
import math
import threading
import pickle

from database import Database
from Grab_Data import NewsTransmitter 
from Collect_Content import get_content
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

def clean_news(news_text):
    for stop_tag in ["<li>", "</li>", "<ol>"]:
        text_list = news_text.split(stop_tag)
        news_text = "".join(text_list)
    return news_text

tfidf_vect_ngram = pickle.load(open("../covid_clf/Project_Update_2/Model/tfidf", 'rb'))
 
clf = pickle.load(open("../covid_clf/Project_Update_2/Model/RFClf", 'rb'))

print(clf)

api_key = 'eb5d9304e7704306aac0500a3cf39ba8'
source_domains = ["bbc.com", "wsj.com", "nytimes.com"]
now_time = datetime.datetime.now().replace(microsecond=0)

news_worker = NewsTransmitter(source_domains, api_key, init_date="2020-06-16")
covid_database = Database()

def update_database(news_worker, db):
    news_list = news_worker.get_all_domain_news()
    for domain in news_list:
        for news in news_list[domain]:
            content = get_content(news.url)
            #if content is None or len(content) == 0:
            #    content = [clean_news(news.news_content)]
            X = tfidf_vect_ngram.transform(content)
            news.score = float(clf.predict_proba(X)[0,1])
        db.insert_news_list(news_list[domain])
        print("update {} news from {} to database".format(len(news_list[domain]), domain))


def get_news(db, start_idx, count):
    news_record = db.get_all_source_news(start_idx, count)
    return news_record

update_database(news_worker, covid_database)

#news_list = get_news(covid_database, 0, 10)
#for news in news_list:
#    print(news[2])
