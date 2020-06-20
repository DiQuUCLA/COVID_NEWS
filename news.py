class News:
    def __init__(self, 
            news_source, 
            news_title, 
            news_content, 
            publish_time=None, 
            image_source=None,
            url=None,
            score=None):
        self.news_source = news_source
        self.news_title = news_title
        self.news_content = news_content
        self.publish_time = publish_time
        self.image_source = image_source
        self.url = url
        self.score = score
