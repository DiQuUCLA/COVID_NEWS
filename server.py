import socket
import sys
import datetime
import math
import threading
import json
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

api_key = 'eb5d9304e7704306aac0500a3cf39ba8'
source_domains = ["bbc.com", "wsj.com", "nytimes.com"]
now_time = datetime.datetime.now().replace(microsecond=0)

news_worker = NewsTransmitter(source_domains, api_key, init_date="2020-06-01")
covid_database = Database()

def update_database(news_worker, db):
    news_list = news_worker.get_all_domain_news()
    for domain in news_list:
        for news in news_list[domain]:
            content = get_content(news.url)
            if content is None or len(content) == 0:
                content = [clean_news(news.news_content)]
            X = tfidf_vect_ngram.transform(content)
            news.score = float(clf.predict_proba(X)[0,1])
        db.insert_news_list(news_list[domain])
        print("update {} news from {} to database".format(len(news_list[domain]), domain))

def get_news(db, start_idx, count):
    news_record = db.get_all_source_news(start_idx, count)
    return news_record

#update_database(news_worker, covid_database)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostbyaddr("54.177.35.98")[0]
server_addr = (host, 8000)
print("Starting Server {} on port 8000".format(host))

sock.bind(server_addr)

sock.listen(1)

def handle_request(query, conn):
    request = process_request(query)
    new_time = datetime.datetime.now().replace(microsecond=0)
    time_difference = (new_time - now_time)
    if time_difference.total_seconds() > 1800:
        update_database(news_worker, covid_database)
    news_list = get_news(covid_database, request["page"] * request["number"], request["number"])
    if news_list == "Server Error":
        conn.sendall("Server Error".encode('utf-8'))
        conn.close()
    else:
        json_news_list = []
        for news in news_list:
            json_news = dict(zip(["source", "title", "description", "publish_time", "image_url", "url", "score"], news))
            
            json_news["publish_time"] = datetime.datetime.timestamp(json_news["publish_time"])
            del json_news["description"]
            #del json_news["score"]
            json_news_list.append(json_news)
        data_json = {"data": json_news_list}
        respond = json.dumps(data_json)
        conn.sendall(respond.encode('ascii'))
        print("\n Send Response \n{}\n".format(respond))
        conn.close()

def process_request(queries):
    queries = queries.split("\n\n")
    if len(queries) > 1:
        query_string = queries[1]
    else:
        query_string = queries[0]
    print(query_string)
    query_list = query_string.split("&")
    request = {}
    for query in query_list:
        split_query = query.split("=")
        if len(split_query) == 2:
            request[split_query[0]] = split_query[1]
    if not "page" in request:
        request["page"] = 0
    request["page"] = int(request["page"])
    if not "number" in request:
        request["number"] = 10
    request["number"] = int(request["number"])
    return request

while True:
    print("Server Listening")
    connection, client_addr = sock.accept()

    try:
    #if(True):
        print("Receive Connection from", client_addr)
        
        complete_data = "".encode("utf-8")
        while True:
            data = connection.recv(32)#.decode("utf-8")
            complete_data += data
            print("Received {}".format(data))
            if len(data) < 32:
                print("Data finished from {}".format(client_addr))
                break
        complete_data = complete_data.decode("utf-8")
        handle_request(complete_data, connection)
    except:
        e = sys.exc_info()[0]
        print("Server Error: {}".format(e))
        handle_request("", connection)

