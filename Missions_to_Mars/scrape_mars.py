from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo

url = "https://mars.nasa.gov/news/"

response = requests.get(url)

soup=bs(response.text, 'html.parser')

#Collect the latest News Title and Paragraph Text
news_title = soup.find('div', class_ = 'content_title').text
print(news_title)

news_p = soup.find('div', class_ = 'rollover_description_inner').text
print(news_p)

#Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#Use splinter to navigate the site and find the image url for the current Featured Mars Image
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

featured_image_url=browser.find_by_css('a.fancybox-thumbs')
# print(featured_image_url)
featured_image_url['href']

featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/image/featured/mars2.jpg'

url = 'https://space-facts.com/mars/'

tables=pd.read_html(url)
tables

mars_facts=tables[0]
mars_facts=mars_facts.rename(columns={0:"Profile",1:"Value"},errors="raise")
mars_facts.set_index("Profile",inplace=True)
mars_facts

facts_table=mars_facts.to_html()
print(facts_table)

facts_table=facts_table.replace('\n','')
print(facts_table)

url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

hemisphere_image_urls=[]
# Get a list of all the hemispheres
links=browser.find_by_css('a.product-item h3')
for link in range(len(links)):
    hemisphere = {}
    #Find the element to loop on
    browser.find_by_css("a.product-item h3")[link].click()
    element= browser.links.find_by_text("Sample").first
    hemisphere['img_url'] = element['href']
    hemisphere['title'] = browser.find_by_css('h2.title').text
    
    hemisphere_image_urls.append(hemisphere)
    browser.back()

hemisphere_image_urls

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db
collection = db.items

mars_dict={
    "news_title":news_title,
    "news_p":news_p,
    "featured_image_url":featured_image_url,
    "mars_facts":facts_table,
    "hemisphere_images":hemisphere_image_urls
}

collection.insert_one(mars_dict)

mars_stuff = db.items.find()

for stuff in mars_stuff:
    print(stuff)