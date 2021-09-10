#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# The `src` will be different every time the page is updated. We'll use the image tag and class (`<img />`and `fancybox-img`) to build the URL to the full-size image.

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Scrape info from "Mars Facts"
# Instead of scraping each row, or the data in each <td />, we're going to scrape the entire table with Pandas' `.read_html()` function.

df = pd.read_html('https://galaxyfacts-mars.com')[0]

# assign columns to the new DataFrame 'df'
df.columns=['description', 'Mars', 'Earth']

# By using the .set_index() function, we're turning the Description column 
# into the DataFrame's index. inplace=True means that the updated index 
# will remain in place, without having to reassign the df to a new variable.
df.set_index('description', inplace=True)
df

# The function `read_html()` specifically searches for and returns a list of tables found in the HTML. By specifying an index of `[0]`, we're telling Pandas to pull only the first table it encounters

df.to_html()


## D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for x in range(4):
     
    # Find the image link with "h3" tag and click to open the relevant image page
    full_image_element = browser.find_by_tag("h3")[x]
    full_image_element.click()
    
    # Parse the resulting html with soup
    html = browser.html
    image_soup = soup(html, 'html.parser')
    
    # Find the relative image url and get the 'href'
    image_url = image_soup.find('a', target='_blank', text='Sample').get('href')

    # Find image title(s)
    img_title = image_soup.find('h2', class_='title').text
              
    # Create a 'hemispheres' dictionary with 'image_url' and 'img_title' key:value pairs   
    hemispheres= {'img_url' : image_url, 'title' : img_title}
    
    # store the dictionary in a list and append values in each iteration
    hemisphere_image_urls.append(hemispheres)
    
    # Go back to the browser
    browser.back()
    
hemisphere_image_urls




