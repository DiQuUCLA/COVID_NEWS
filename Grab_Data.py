from newsapi import NewsApiClient
import datetime
import math

class NewsTransmitter:
    def __init__(self, source_domains, api_key, topic='covid'):
        self.date = datetime.datetime.now().replace(microsecond=0).isoformat()
        self.source = source_domains
        self.source_count = {}
        for source in source_domains:
            self.source_count[source] = 0
        self.newsapi = NewsApiClient(api_key='eb5d9304e7704306aac0500a3cf39ba8')
        self.topic = topic

    def get_domain_news_count(self, domain, now_time):
        news_result = self.newsapi.get_everything(q='covid',
                                                    domains=domain,
                                                    language='en',
                                                    from_param=self.date,
                                                    to=now_time,
                                                    page=1
                                                    )

        new_count = news_result['totalResults']
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
        overall_count, first_page_content = self.get_domain_news_count(domain, now_time)
        
        domain_result = []
        domain_result.extend(first_page_content)
        page_number = math.ceil(overall_count / 20) #Get the total number of pages

        if page_number >= 2:
            for page in range(2, page_number+1):
                page_result = self.get_domain_news_at_page_n(domain, now_time, page)
                domain_result.extend(page_result)
        return domain_result

    def get_all_domain_news(self):
        now_time = datetime.datetime.now().replace(microsecond=0).isoformat()
        content_dict = {}
        for domain in self.source_domains:
            content_dict[domain] = self.get_domain_news(domain, now_time)
        return content_dict

now_time = datetime.datetime.now().replace(microsecond=0).isoformat()



newsapi = NewsApiClient(api_key='eb5d9304e7704306aac0500a3cf39ba8')

news_domains = ['bbc.com', 'wsj.com', 'nytimes.com']

top_headlines = newsapi.get_everything(q='covid',
                                          domains='bbc.com',
                                          language='en', 
                                          from_param='2020-05-15', 
                                          to=now_time,
                                          page=1)

print(len(top_headlines['articles']))
print(top_headlines['totalResults'])
for article in top_headlines['articles']:
    #print(article["title"])
    for k in article:
       print('{}: {}'.format(k, article[k]))
       print()

