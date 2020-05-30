import socket
import sys
import datetime
import math

from database import Database
from Grab_Data import NewsTransmitter 

api_key = 'eb5d9304e7704306aac0500a3cf39ba8'
source_domains = ["bbc.com", "wsj.com", "nytimes.com"]
now_time = datetime.datetime.now().replace(microsecond=0)

news_worker = NewsTransmitter(source_domains, api_key, init_date="2020-05-20")
covid_database = Database()

def update_database(news_worker, db):
    news_list = news_worker.get_all_domain_news()
    for domain in news_list:
        db.insert_news_list(news_list[domain])
        #print("update {} news from {} to database".format(len(news_list), domain))

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

def handle_request(query):
    request = process_request(query)
    new_time = datetime.datetime.now().replace(microsecond=0)
    time_difference = (new_time - now_time)
    if time_difference.total_seconds() > 300:
        update_database(news_worker, covid_database)
    news_list = get_news(covid_database, request["page"] * request["number"], request["number"])
    json_news_list = []
    for news in news_list:
        json_news = dict(zip(["source", "title", "description", "publish_time", "image_url"], news))
        json_news_list.append(str(json_news))
    return "\n".join(json_news_list)

def process_request(queries):
    query_list = queries.split("&")
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
        print("Receive Connection from", client_addr)
        
        complete_data = ""
        while True:
            data = connection.recv(16).decode("utf-8")
            complete_data += data
            print("Received {}".format(data))
            if len(data) < 16:
                print("Data finished from {}".format(client_addr))
                break
        respond = handle_request(complete_data)
        connection.sendall(respond.encode('utf-8'))
    finally:
        connection.close()
