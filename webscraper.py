"""
Title: What Made it National: A simple web scraper
Final Goal: website that displays national news articles that contain keywords about local areas
Current Description: scraps nbc us news and stores basic article data in json object array
Creator: Sophia M. Barnett
Revision History:
    06/25/2021: Creation 
    06/26/2021: Stores basic data in json object from nbc us news articles
"""
# Things to accomplish
# 1. Add page scrolling so more articles can be searched (include selenium?)
# 2. Go into each article and search the whole page for key words
# 3. Set up website to show the title and subscript of the articles
# 4. Search multiple different national news websites

from requests.api import request
from bs4 import BeautifulSoup
import requests
import json
import re

matches = ["Texas", "Tx", "Dallas", "Houston", "Austin", "Midland", "Odessa", "Lubbock"]

# function to scan the full article for the words searching for
def scan_article(url):
    res = requests.get(url, timeout=5)
    content = BeautifulSoup(res.content, "html.parser")

    try:
        for paragraph in content.find("div", attrs={"class": "article-body__content"}):
            if any(x in paragraph.text for x in matches):
                return True
            # end if
        # end for
    except:
        return False

    return False
# end scan_article

def main():
    # Make a get request to get information from website
    url = "https://www.nbcnews.com/us-news"
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")

    # Put raw info in file to further examination
    art = content.find("div", attrs={"class": "feeds__items-wrapper ph5 ph0-m"}).prettify()
    #art = content.find("div", attrs={"class": "multi-up__articles bg-knockout-primary"}).prettify()
    with open('output.txt', 'w') as f:
        f.write(str(art))

    articles = []

    # Get top three stories (They do not include subscript)
    for topStory in content.find("div", attrs={"class": "multi-up__articles bg-knockout-primary"}):
        topStoryObj = {
            "category": topStory.find("span", attrs={"data-test": "unibrow-text"}).text,
            "posted": "",
            "title": topStory.find("span", attrs={"class": "tease-card__headline"}).text,
            "subscript": "",
            "link": ""
        }
        articles.append(topStoryObj)

        if any(x in (topStoryObj["title"] or topStoryObj["subscript"]) for x in matches):
            print(topStoryObj["title"])

    # Create an array of objects for each headline article on the 'us news' page
    for article in content.find("div", attrs={"class": "feeds__items-wrapper ph5 ph0-m"}):
        links = []
        for link in article.find_all('a', attrs={'href': re.compile("^https://")}):
            links.append(link)
        articleObject = {
            "category": article.find("span", attrs={"data-test": "unibrow-text"}).text,
            "posted": article.find("div", attrs={"class": "wide-tease-item__timestamp dib db-m ml3 ml0-m"}).text,
            "title": article.find("h2", attrs={"class": "wide-tease-item__headline"}).text,
            "subscript": article.find("div", attrs={"class": "wide-tease-item__description"}).text,
            "link": links[2].get('href')
        }
        articles.append(articleObject)

        if any(x in (articleObject["title"] or articleObject["subscript"]) for x in matches):
            print(articleObject["title"])
        elif scan_article(articleObject['link']):
            print(articleObject["title"])

    #if scan_article(articles[5]['link']):
    #    print(articles[5]["title"])

    # store data as a json file
    with open("articleData.json", "w") as outfile:
        json.dump(articles, outfile, indent=4)

if __name__ == '__main__':
    main()