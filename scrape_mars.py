import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # create mars dictionary for mongo
    mars_data = {}

    # visit website 1
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    content_title = soup.find('div', class_='content_title').find('a')

    news_title = content_title.text.strip()

    article_teaser_body = soup.find('div', class_='article_teaser_body')

    news_p = article_teaser_body.text.strip()

    # add to mars_data
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    # visit website 2
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    baseurl = 'https://www.jpl.nasa.gov'

    html2 = browser.html
    soup2 = bs(html2, 'html.parser')

    button = soup2.find('a', class_='button fancybox')

    image_url = soup2.find('a', {'id': 'full_image', 'data-fancybox-href': True}).get('data-fancybox-href')

    featured_image_url = baseurl + image_url
    # add to mars_data
    mars_data["featured_image_url"] = featured_image_url
    
    # visit website 3
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)

    html3 = browser.html
    soup3 = bs(html3, 'html.parser')

    tweet = soup3.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    mars_weather = tweet.text.strip()
    # add to mars_data
    mars_data["mars_weather"] = mars_weather

    # website 4
    url4 = 'https://space-facts.com/mars/'

    tables = pd.read_html(url4)

    df = tables[0]

    table = df.to_html()

    # add to mars_data
    mars_data["table"] = table

    # visit website 5
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)

    html5 = browser.html
    soup5 = bs(html5, 'html.parser')

    one = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'
    two = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'
    three = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'
    four = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'

    links = [one, two, three, four]

    a = soup5.find_all('h3')

    descriptions = [h3.text.strip() for h3 in a]

    hemisphere_image_urls = [{'title': description, 'img_url': link} for description, link in zip(descriptions,links)]

    # add to mars_data
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    # return mars_data dict
    print(mars_data["featured_image_url"])

    return mars_data

if __name__ == "__main__":
    scrape()