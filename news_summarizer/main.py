import os
import logging
from dotenv import load_dotenv
from typing import List, Dict
import requests
import anthropic

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class NewsSummarizer:
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = 'https://newsapi.org/v2/'
        if not self.api_key:
            raise ValueError("NEWS_API_KEY missing from .env")

    def fetch_news(self, query: str) -> List[Dict]:
        """Fetch news articles from NewsAPI"""
        try:
            url = f"{self.base_url}everything?q={query}&apiKey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get('articles', [])
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return []

    def summarize_articles(self, articles: List[Dict]) -> str:
        """Summarize articles using Claude"""
        articles_text = '\n\n'.join([
            f"Article: {article['content']}\nSource URL: {article['url']}"
            for article in articles
        ])
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"Summarize these news articles and include the source URLs in your summary:\n{articles_text}"
            }]
        )
        return response.content[0].text

    def run(self):
        """Main execution flow"""
        topic = input("Enter news topic to summarize: ")
        articles = self.fetch_news(topic)
        
        if not articles:
            print("No articles found for this topic.")
            return
        
        summary = self.summarize_articles(articles)
        print(f"\nSummary for '{topic}':\n")
        print(summary)

if __name__ == "__main__":
    summarizer = NewsSummarizer()
    summarizer.run()
