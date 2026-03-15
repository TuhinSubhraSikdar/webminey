import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
from urllib.parse import urlparse


STOPWORDS = {
    'the', 'is', 'and', 'of', 'to', 'in', 'for', 'on', 'with', 'as',
    'at', 'by', 'an', 'be', 'this', 'that', 'from', 'it', 'or', 'are',
    'was', 'were', 'has', 'have', 'had', 'not', 'but', 'can', 'will',
    'you', 'your', 'we', 'our', 'about', 'into', 'after', 'before',
    'their', 'there', 'they', 'them', 'then', 'than', 'which', 'also'
}


def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower()


def extract_visible_text(soup):
    for tag in soup([
        'script', 'style', 'noscript',
        'header', 'footer', 'nav',
        'aside', 'svg', 'form'
    ]):
        tag.extract()

    return soup.get_text(separator=' ')


def extract_headings(soup):
    headings = []

    for tag in soup.find_all(['h1', 'h2', 'h3']):
        text = tag.get_text(strip=True)
        if text:
            headings.append(text)

    return headings


def extract_meta_description(soup):
    meta = soup.find('meta', attrs={'name': 'description'})
    if meta and meta.get('content'):
        return meta.get('content')
    return ''


def generate_bigrams(words):
    return [
        f"{words[i]} {words[i+1]}"
        for i in range(len(words)-1)
    ]


def extract_bag_of_words(url):
    try:
        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive'
                  }
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        response.raise_for_status()

        if response.status_code != 200:
            return {
                'error': f'Failed to fetch URL ({response.status_code})'
            }

        soup = BeautifulSoup(response.text, 'lxml')

        title = soup.title.string.strip() if soup.title else ''

        headings = extract_headings(soup)

        meta_description = extract_meta_description(soup)

        visible_text = extract_visible_text(soup)

        combined_text = f"{title} {' '.join(headings)} {meta_description} {visible_text}"

        cleaned = clean_text(combined_text)

        words = cleaned.split()

        filtered_words = [
            word for word in words
            if len(word) > 2 and word not in STOPWORDS
        ]

        total_words = len(filtered_words)

        word_counts = Counter(filtered_words)

        top_words = []

        for word, count in word_counts.most_common(50):
            density = round((count / total_words) * 100, 2)

            top_words.append({
                'word': word,
                'count': count,
                'density': density
            })

        # Bigram extraction
        bigrams = generate_bigrams(filtered_words)

        bigram_counts = Counter(bigrams).most_common(15)

        parsed_url = urlparse(url)

        return {
            'title': title,
            'domain': parsed_url.netloc,
            'meta_description': meta_description,
            'headings': headings,
            'words': top_words,
            'bigrams': bigram_counts,
            'total_words': total_words,
            'unique_words': len(set(filtered_words))
        }

    except Exception as e:
        return {
            'error': str(e)
        }