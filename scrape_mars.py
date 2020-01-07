#imports
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import requests

def scrape_mars(): #an unconventionally LONG function

    #get nasa article title and blurb
    nasa_url = 'https://mars.nasa.gov/news/'
    response_nasa = requests.get(nasa_url)
    soup = BeautifulSoup(response_nasa.text, features='lxml')
    news_title = soup.find('div', class_='content_title').text.strip()
    news_p = soup.find('div', class_='rollover_description_inner').text.strip()

    #get featured mars image from nasa jpl
    jpl_url = 'https://www.jpl.nasa.gov'
    mars_search_url = '/spaceimages/?search=&category=Mars'
    response_jpl = requests.get(jpl_url+mars_search_url)
    soup = BeautifulSoup(response_jpl.text, features='lxml')
    img_tag = soup.find('img', class_='thumb')
    img_url = img_tag['src']
    img_url = img_url.replace('-640x350', '_hires')
    img_url = img_url.replace('wallpaper', 'largesize')
    featured_img_url = jpl_url + img_url

    #get mars weather from Twitter
    twitter_url = 'https://twitter.com/'
    mars_twitter_url = 'marswxreport?lang=en'
    response_twitter = requests.get(twitter_url + mars_twitter_url)
    soup = BeautifulSoup(response_twitter.text, features='lxml')
    weather_tweet = soup.find('p', class_='tweet-text').text.strip()\
                    .split('pic.twitter.com')[0].replace('\n', '')

    #get mars facts from space-facts.com
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    mars_table = tables[0]
    mars_table.rename(columns={0:'Measurement', 1:'Value'}, inplace=True)
    mars_table_html = mars_table.to_html(index=False, classes='table-striped')

    #get mars images from astrogeology.usgs.gov

    def get_imgs(name, url): #throws deprecation warnings...
        browser.visit(url)
        browser.click_link_by_partial_text(name) #but the documentation...
        img_title = browser.title.split(' Enhanced')[0]
        browser.click_link_by_text('Sample') #hasn't been updated so \_(-_-)_/
        img_url = browser.windows[1].url
        for window in browser.windows:
            window.close()
        return {'title':img_title,'img_url':img_url}

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q='
    search_query = 'hemisphere+enhanced&k1=target&v1=Mars'
    total_url = hemispheres_url + search_query
    hemisphere_names = [
        'Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris'
        ]
    browser = Browser('chrome', headless=True)
    hemisphere_imgs = [get_imgs(name, total_url) for name in hemisphere_names]
    browser.quit()

    return {
        'title' : news_title,
        'blurb' : news_p,
        'img_url' : featured_img_url,
        'weather' : weather_tweet,
        'table' : mars_table_html,
        'hemispheres' : hemisphere_imgs
        }