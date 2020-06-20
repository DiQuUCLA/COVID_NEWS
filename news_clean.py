from database import Database
from Grab_Data import NewsTransmitter

covid_database = Database()

def get_news(db, start_idx, count):
    news_record = db.get_all_source_news(start_idx, count)
    return news_record

news_list = get_news(covid_database, 1, 10)

json_news_list = []
for news in news_list:
    json_news = dict(zip(["source", "title", "desc", "publish_time", "img_url"], news))
    json_news_list.append(json_news)

data_json = {"data": json_news_list}

print(str(data_json).encode('utf-8').decode('utf-8'))
