import requests
from bs4 import BeautifulSoup
import re
from replace import remove_text_in_angle_brackets

content_css_class = "yle__article__content"


def get_article_soup(article_url: str) -> BeautifulSoup:
    # Fetch the content from the URL
    response = requests.get(article_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'lxml')

        return soup

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


def scrap_article_content(article_soup: BeautifulSoup):
    # Find all elements with class {article_css_class}
    elements = article_soup.find_all(class_=content_css_class)

    # We expect only one element:
    try:
        article_content_html = str(elements[0])
    except IndexError:
        raise Exception("Article Content Not Found")

    separated_paragraphs = re.sub("</p>", "</p>\n\n", article_content_html)
    article_content_text = remove_text_in_angle_brackets(separated_paragraphs)

    return article_content_text


if __name__ == "__main__":
    arti_url = "https://yle.fi/a/74-20090483"
    arti_soup = get_article_soup(arti_url)
    print(scrap_article_content(arti_soup))
