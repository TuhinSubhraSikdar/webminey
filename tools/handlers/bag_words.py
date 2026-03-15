import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

STOPWORDS = {
    'the', 'is', 'and', 'of', 'to', 'in', 'for', 'on', 'with', 'as',
    'at', 'by', 'an', 'be', 'this', 'that', 'from', 'it', 'or', 'are',
    'was', 'were', 'has', 'have', 'had', 'not', 'but', 'can', 'will',
    'you', 'your', 'we', 'our'
}


def extract_bag_of_words(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for tag in soup(['script', 'style', 'noscript']):
            tag.extract()

        text = soup.get_text(separator=' ')

        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())

        filtered_words = [
            word for word in words
            if word not in STOPWORDS
        ]

        word_counts = Counter(filtered_words)

        top_words = word_counts.most_common(50)

        return {
            'words': top_words,
            'total_words': len(set(filtered_words))
        }

    except Exception as e:
        return {
            'words': [],
            'total_words': 0,
            'error': str(e)
        }