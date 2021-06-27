"""
Title: What Made it National: A simple web scraper
Final Goal: website that displays national news articles that contain keywords about local areas
Current Description: scraps nbc us news and stores basic article data in json object array
Creator: Sophia M. Barnett
Revision History:
    06/25/2021: Creation 
    06/26/2021: Stores basic data in json object from nbc us news articles
"""

from bs4 import BeautifulSoup
import requests
import json

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
    #articles.append(article.prettify())
    articleObject = {
        "category": article.find("span", attrs={"data-test": "unibrow-text"}).text,
        "posted": article.find("div", attrs={"class": "wide-tease-item__timestamp dib db-m ml3 ml0-m"}).text,
        "title": article.find("h2", attrs={"class": "wide-tease-item__headline"}).text,
        "subscript": article.find("div", attrs={"class": "wide-tease-item__description"}).text
    }
    articles.append(articleObject)

# store data as a json file
with open("articleData.json", "w") as outfile:
    json.dump(articles, outfile, indent=4)
