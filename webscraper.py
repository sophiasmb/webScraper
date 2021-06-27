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

from bs4 import BeautifulSoup
import requests
import json
import re

def main():
    # Make a get request to get information from website
    url = "https://www.nbcnews.com/us-news"
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")

    # Put raw info in file to further examination
    art = content.find("div", attrs={"class": "feeds__items-wrapper ph5 ph0-m"}).prettify()
    with open('output.txt', 'w') as f:
        f.write(str(art))

    # Create an array of objects for each headline article on the 'us news' page
    articles = []
    for article in content.find("div", attrs={"class": "feeds__items-wrapper ph5 ph0-m"}):
        link =  article.find('a', attrs={'href': re.compile('https:..www.nbcnews.com.*.{9,}')})
        articleObject = {
            "category": article.find("span", attrs={"data-test": "unibrow-text"}).text,
            "posted": article.find("div", attrs={"class": "wide-tease-item__timestamp dib db-m ml3 ml0-m"}).text,
            "title": article.find("h2", attrs={"class": "wide-tease-item__headline"}).text,
            "subscript": article.find("div", attrs={"class": "wide-tease-item__description"}).text,
            "link": link.get('href')
        }
        articles.append(articleObject)

        matches = ["Texas", "Tx", "Dallas", "Houston", "Austin", "Midland", "Odessa", "Lubbock"]
        if any(x in (articleObject["title"] or articleObject["subscript"]) for x in matches):
            print(articleObject["title"])

    # store data as a json file
    with open("articleData.json", "w") as outfile:
        json.dump(articles, outfile, indent=4)

if __name__ == '__main__':
    main()