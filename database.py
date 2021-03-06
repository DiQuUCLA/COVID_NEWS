import psycopg2
import datetime
from news import News

class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(user = "ubuntu",
                                    password = "ubuntu",
                                    host = "127.0.0.1",
                                    port = "5432", 
                                    database = "ubuntu")
            self.cursor = self.connection.cursor()

            print( self.connection.get_dsn_parameters(), "\n")
            self.cursor.execute("SELECT version();")
            record = self.cursor.fetchone()
            print("You are connected to - ", record, "\n")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def insert_news_list(self, news_list):
        for news in news_list:
            self.insert_news(news)

    def insert_news(self, news):
        insert_query = """ INSERT INTO covid (news_source,
                                                    news_title,
                                                    news_content, 
                                                    publish_time,
                                                    image_source,
                                                    url,
                                                    score)
                                                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        record_to_insert = (news.news_source, \
                            news.news_title, \
                            news.news_content, \
                            news.publish_time, \
                            news.image_source, \
                            news.url, \
                            news.score)
        #try:
        if True:
            if news.news_source and news.news_title and news.news_content:
                self.cursor.execute(insert_query, record_to_insert)
                self.connection.commit()
                count = self.cursor.rowcount
        #except psycopg2.DatabaseError as error:
        #    self.connection.rollback()
        
            #print("Insert failed: {}".format(record_to_insert))
        #print(count, "Record inserted successfully into covid table")
    
    def get_news(self, sources, start_idx, count):
        select_Query = "select distinct * from covid where news_source is %s"
        try:
            self.cursor.execute(select_Query, (sources,))
            news_records = cursor.fetchall()
            return news_records
        except psycopg2.DatabaseError as error:
            self.connection.rollback()
            return "Server Error"

    def get_all_source_news(self, start_idx, count):
        select_Query = "SELECT distinct * from covid ORDER BY publish_time DESC LIMIT %s OFFSET %s"
        self.cursor.execute(select_Query, (count, start_idx))
        news_records = self.cursor.fetchall()
        return news_records
    
if __name__ == "__main__":
    database = Database()
    new_article = News("First", "second", "Third", datetime.datetime.now())
    database.insert_news(new_article)
