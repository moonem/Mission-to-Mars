# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = hemisphere_url_title()

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_img_title": hemisphere_url_title()
        }

    # Stop webdriver and return data
    browser.quit()
    return data


## News Title and Paragraph:
def mars_news(browser):
# When we add the word "browser" to our function, we're telling Python that we'll be using the browser variable we defined outside the function. All of our scraping code utilizes an automated browser, and without this section, our function wouldn't work.
    
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


## Featured Image:
def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url


## Mars Facts:
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


## Hemisphere Image URLs and Titles:
def hemisphere_url_title():
    
    # Mars Hemisphere URL:
    url = 'https://marshemispheres.com/'
    
    # Define an empty list to contain dictionary with image_urls and titles
    hemisphere_image_urls = []

# for loop to retrieve the image urls and titles for each hemisphere.
    for x in range(4):
     
    # Find the image link with "h3" tag and click to open the relevant image page
        full_image_element = browser.find_by_tag("h3")[x]
        full_image_element.click()
    
    # Parse the resulting html with soup
        html = browser.html
        image_soup = soup(html, 'html.parser')
    
    # Find the relative image url and get the 'href'
        image_url = image_soup.find('a', target='_blank', text='Sample').get('href')
        img_url = f'{url}{image_url}'
    
    # Find image title(s)
        img_title = image_soup.find('h2', class_='title').text
              
    # Create a 'hemispheres' dictionary with 'image_url' and 'img_title' key:value pairs   
        hemispheres= {'img_url' : img_url, 'title' : img_title}
    
    # store the dictionary in a list and append values in each iteration
        hemisphere_image_urls.append(hemispheres)
    
    # Go back to the browser
        browser.back()

        return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())