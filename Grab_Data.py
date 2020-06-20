from newsapi import NewsApiClient
from news import News
from database import Database
import datetime
import math

class NewsTransmitter:
    def __init__(self, source_domains, api_key, topic='covid', init_date=None):
        self.date = init_date
        if not init_date:
            self.date = datetime.datetime.now().replace(microsecond=0).isoformat()
        self.source = source_domains
        self.source_count = {}
        for source in source_domains:
            self.source_count[source] = 0
        self.newsapi = NewsApiClient(api_key=api_key)
        self.topic = topic

    def get_domain_news_count(self, domain, now_time):
        news_result = self.newsapi.get_everything(q='covid',
                                                    domains=domain,
                                                    language='en',
                                                    from_param=self.date,
                                                    to=now_time,
                                                    page=1
                                                    )

        news_count = news_result['totalResults']
        first_page_news = news_result['articles']
        return news_count, first_page_news

    def get_domain_news_at_page_n(self, domain, now_time, page_number):
        news_result = self.newsapi.get_everything(q='covid',
                                                    domains=domain,
                                                    language='en',
                                                    from_param=self.date,
                                                    to=now_time,
                                                    page=page_number
                                                    )
        page_content = news_result['articles']
        return page_content

    def get_domain_news(self, domain, now_time):
        '''
            domain: str, the domain of source (e.g. 'bbc.com')
            now_time: Datetime, the current datetime in iso form

            return:
                domain_news_result: list<News> The news from the last query until now
        '''
        overall_count, first_page_content = self.get_domain_news_count(domain, now_time)
        
        domain_result = []
        domain_result.extend(first_page_content)
        page_number = math.ceil(overall_count / 20) #Get the total number of pages

        if page_number >= 2:
            for page in range(2, min(page_number+1, 5)):
                page_result = self.get_domain_news_at_page_n(domain, now_time, page)
                domain_result.extend(page_result)
        domain_news_result = []
        for r in domain_result:
            news_r = News(domain, r["title"], r["description"], r["publishedAt"], r["urlToImage"], r["url"])
            domain_news_result.append(news_r)

        return domain_news_result

    def get_all_domain_news(self):
        """
            return:
                dict <domain: list<News>>
        """
        now_time = datetime.datetime.now().replace(microsecond=0).isoformat()
        content_dict = {}
        for domain in self.source:
            content_dict[domain] = self.get_domain_news(domain, now_time)
        self.date = datetime.datetime.now().replace(microsecond=0).isoformat()
        return content_dict

if __name__ =='__main__':
    now_time = datetime.datetime.now().replace(microsecond=0).isoformat()


    #newsapi = NewsApiClient(api_key='eb5d9304e7704306aac0500a3cf39ba8')


    news_domains = ['bbc.com', 'wsj.com', 'nytimes.com']


    api_key='eb5d9304e7704306aac0500a3cf39ba8'
    transmitter= NewsTransmitter(news_domains, api_key, init_date="2020-06-16")
    top_headlines = transmitter.get_domain_news(transmitter.source[0], now_time)

    print(len(top_headlines))
    #print(top_headlines['totalResults'])

    for article in top_headlines[:3]:
        print(article["title"])
