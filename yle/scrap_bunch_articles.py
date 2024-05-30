import os
import re
import json
import requests
from bs4 import BeautifulSoup

from article_exception import RSSException


def get_rss_soup(feed_url: str):
    # Step 1: Fetch the RSS feed
    response = requests.get(feed_url)

    if response.status_code == 200:
        # Step 2: Parse the RSS feed with BeautifulSoup
        soup = BeautifulSoup(response.content, 'xml')
        return soup

    raise RSSException(f"RSS Feed can't be read. Status code: {response.status_code}")


def scrap_articles_from_feed_soup(feed_soup: BeautifulSoup):
    def clean_image_url(img_url):
        cleaned_url = re.sub(r'/w_\d+,h_\d+,q_\d+/', '/', img_url)
        return cleaned_url

    # Extract text inside all <guid> tags
    guid_tags = feed_soup.find_all('guid')
    guid_texts = [tag.get_text() for tag in guid_tags]

    # Find all 'enclosure' tags
    enclosure_tags = feed_soup.find_all('enclosure')

    # Extract the 'url' attribute from each 'enclosure' tag
    img_urls = [tag['url'] for tag in enclosure_tags if tag.has_attr('url')]

    cleaned_img_urls = [clean_image_url(img_url) for img_url in img_urls]

    return [{"url": article_url, "img_url": img_url} for article_url, img_url in zip(guid_texts, cleaned_img_urls)]


def scrap_feed_articles(feed_url: str):
    try:
        feed_soup = get_rss_soup(feed_url)
        articles_urls_and_img_list = scrap_articles_from_feed_soup(feed_soup)
        return articles_urls_and_img_list

    except RSSException as e:
        # TODO: Log e and feed URL and remove the print
        print(e)

        return []


def scrap_all_feeds():
    # Read JSON file into a dictionary
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'article_sources.json')
    with open(json_path, "r") as file:
        feeds = json.load(file)

    all_articles_urls = {}

    for feed_key in feeds:
        feed_url = feeds[feed_key]
        all_articles_urls[feed_key] = scrap_feed_articles(feed_url)

    return all_articles_urls


if __name__ == "__main__":
    from pprint import pprint
    result = scrap_all_feeds()
    pprint(result)
