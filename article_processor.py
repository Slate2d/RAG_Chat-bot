import requests
import re
from bs4 import BeautifulSoup


class ArticleFetcher:
    def __init__(self, url):
        self.url = url

    def fetch(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            article_content = soup.find('div', {'class': 'article-body'})
            if article_content:
                text = article_content.text.strip()
                return self.split_article(text)
        else:
            raise Exception(f"Error fetching article: {response.status_code}")

    @staticmethod
    def split_article(text):
        chunks = re.split(r'\d+\.\s', text)
        return [chunk.strip() for chunk in chunks if chunk.strip()]
