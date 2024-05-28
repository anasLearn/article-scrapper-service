import requests
from bs4 import BeautifulSoup

from article_exception import RSSException

# variables needed for scraping
main_news_url = "https://feeds.yle.fi/uutiset/v1/majorHeadlines/YLE_UUTISET.rss"


def get_rss_soup(feed_url: str):
    # Step 1: Fetch the RSS feed
    response = requests.get(feed_url)

    if response.status_code == 200:
        # Step 2: Parse the RSS feed with BeautifulSoup
        soup = BeautifulSoup(response.content, 'xml')
        return soup

    raise RSSException(f"RSS Feed can't be read. Status code: {response.status_code}")


def scrap_articles_from_feed_soup(feed_soup: BeautifulSoup):
    # Extract text inside all <guid> tags
    guid_tags = feed_soup.find_all('guid')
    guid_texts = [tag.get_text() for tag in guid_tags]

    return list(set(guid_texts))  # remove duplicates


def scrap_all_feed_articles(feed_url: str):
    try:
        feed_soup = get_rss_soup(feed_url)
        articles_urls_list = scrap_articles_from_feed_soup(feed_soup)
        return articles_urls_list

    except RSSException as e:
        # TODO: Log e and feed URL and remove the print
        print(e)

        return []


if __name__ == "__main__":
    rss_url = "https://feeds.yle.fi/uutiset/v1/majorHeadlines/YLE_UUTISET.rss"
    from pprint import pprint
    result = scrap_all_feed_articles(rss_url)
    pprint(result)