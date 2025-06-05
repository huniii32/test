"""Simple Naver News crawler and cleaner.

This script demonstrates how to fetch and clean a single article from Naver News.
Please verify that you are allowed to crawl Naver according to their terms of
service before using this script in production.
"""

import re
from typing import List

import pandas as pd
import requests
from bs4 import BeautifulSoup


def fetch_article(url: str) -> dict:
    """Fetch article data from a Naver News URL.

    Returns a dictionary containing the article title, publication date and
    content text. Raises an exception if the request fails.
    """
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.select_one("h2#title_area")
    date_tag = soup.select_one(".media_end_head_info_datestamp_time")
    content_tag = soup.select_one("#dic_area")

    return {
        "title": title_tag.get_text(strip=True) if title_tag else None,
        "date": date_tag.get_text(strip=True) if date_tag else None,
        "content": content_tag.get_text(separator=" ", strip=True) if content_tag else None,
    }


def clean_text(text: str) -> str:
    """Remove newlines and excessive whitespace from text."""
    if not text:
        return ""
    cleaned = re.sub(r"[\n\r\t]", " ", text)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def crawl_articles(urls: List[str]) -> List[dict]:
    """Fetch and clean multiple Naver News articles."""
    articles = []
    for url in urls:
        article = fetch_article(url)
        article["content"] = clean_text(article.get("content", ""))
        articles.append(article)
    return articles


def save_to_csv(articles: List[dict], path: str) -> None:
    """Save article data to a CSV file."""
    df = pd.DataFrame(articles)
    df.to_csv(path, index=False)


def main():
    # Example URLs (replace with real ones)
    urls = [
        "https://n.news.naver.com/article/001/0000000000",
        "https://n.news.naver.com/article/001/0000000001",
    ]
    articles = crawl_articles(urls)
    save_to_csv(articles, "articles.csv")
    print("Saved articles to articles.csv")


if __name__ == "__main__":
    main()
