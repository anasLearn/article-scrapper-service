import requests
from bs4 import BeautifulSoup
import re

from article_exception import ArticleException
from replace import remove_text_in_angle_brackets

header_css_class = "yle__article__header"
content_css_class = "yle__article__content"
published_css_class = "yle__article__date--published"
updated_css_class = "yle__article__date--modified"


def get_article_soup(article_url: str) -> BeautifulSoup:
    # Fetch the content from the URL
    response = requests.get(article_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'lxml')

        return soup

    else:
        raise ArticleException(f"Failed to retrieve the page. Status code: {response.status_code}. URL = {article_url}")


def scrap_article_header(article_soup: BeautifulSoup) -> dict:
    article_title = ""
    article_introduction = ""
    image_url = ""

    article_header = article_soup.find(class_=header_css_class)
    if not article_header:
        raise ArticleException("Article Header Not Found")

    # Extract header title
    header_title = article_header.find('h1')
    if header_title:
        article_title = remove_text_in_angle_brackets(str(header_title))

    # Extract introduction paragraph
    header_intro = article_header.find("p")
    if header_intro:
        article_introduction = remove_text_in_angle_brackets(str(header_intro))

    # Extract the image URL
    image_tag = article_header.find('img')
    if image_tag and 'src' in image_tag.attrs:
        image_url = image_tag['src']

    return {
        "article_title": article_title,
        "article_introduction": article_introduction,
        "article_image_url": image_url
    }


def scrap_article_content(article_soup: BeautifulSoup) -> str:
    # Find all elements with class {article_css_class}
    elements = article_soup.find_all(class_=content_css_class)

    # We expect only one element:
    try:
        article_content_html = str(elements[0])
    except IndexError:
        raise ArticleException("Article Content Not Found")

    separated_paragraphs = re.sub("</p>", "</p>\n\n", article_content_html)
    article_content_text = remove_text_in_angle_brackets(separated_paragraphs)

    return article_content_text


def scrap_article_datetime(article_soup: BeautifulSoup) -> str:
    # Find the published date element
    published_tag = article_soup.find(class_=published_css_class)

    # Find the modified date element
    modified_tag = article_soup.find(class_=updated_css_class)

    # Determine which datetime to use
    if modified_tag and 'datetime' in modified_tag.attrs:
        date_str = modified_tag['datetime']
    elif published_tag and 'datetime' in published_tag.attrs:
        date_str = published_tag['datetime']
    else:
        raise ArticleException("Article date not found")

    # Return the datetime string and datetime object as a tuple
    return date_str


def scrap_article(article_url: str) -> dict:
    try:
        article_soup = get_article_soup(article_url)
        result_dict = scrap_article_header(article_soup)
        result_dict["article_content"] = scrap_article_content(article_soup)
        result_dict["article_datetime"] = scrap_article_datetime(article_soup)
        return result_dict

    except ArticleException as e:
        # TODO: Log e and URL and remove the print
        print(e)

        return {}


if __name__ == "__main__":
    from pprint import pprint
    arti_url = "https://yle.fi/a/74-20090269"
    pprint(scrap_article(arti_url))
