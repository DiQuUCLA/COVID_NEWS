from newspaper import Article
import pandas as pd
from nltk.tokenize import RegexpTokenizer

def get_content(url_input):
    paper = Article(url_input)
    newsPaper = {}

    paper.download()
    paper.parse()
    newsPaper['title'] = paper.title
    newsPaper['text'] = paper.text
    newsPaper['link'] = paper.url
    newsPaper['author'] = ["someone"]
    print("articles downloaded from newspaper url: ", paper.url)
    if not "text" in newsPaper:
        return None
    X_input = pd.DataFrame(newsPaper)
    df_clean = X_input
    

    tokenizer = RegexpTokenizer(r'\w+')
    df_clean['clean'] = df_clean['text'].astype('str') 
    df_clean.dtypes

    df_clean["tokens"] = df_clean["clean"].apply(tokenizer.tokenize)
    # delete Stop Words
    X_predict = df_clean['clean']
    return X_predict
