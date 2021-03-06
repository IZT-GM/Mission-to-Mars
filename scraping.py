# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def scrape_all():
    import datetime as dt
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    #Define variables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }



def mars_news(browser):

    #Set up executable
    # executable_path = {'executable_path': 'C:/Users/gamad/OneDrive\Documentos/_BootCamp/Module 10/Mission-to-Mars'}
    browser = Browser('chrome', executable_path='chromedriver', headless=False)

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html=browser.html
    news_soup=BeautifulSoup(html, 'html.parser')
    
    try:
        slide_elem=news_soup.select_one('ul.item_list li.slide')
        # slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title=slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_paragraph=slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p


# ### Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem=browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    #Parse the resulting html with soup
    html=browser.html
    img_soup=BeautifulSoup(html,'html.parser')

    try:
        # Find the relative image url
        img_url_rel=img_soup.select_one('figure.lede a img').get('src')

        # Use the base URL to create an absolute URL
        img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    except AttributeError:
        return None

    return img_url

def mars_facts():
    # Use 'read_html' to scrape the facts table into a dataframe
    try:
        df=pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['desctiption','value']
    df.set_index('desctiption', inplace=True)

    # Assign columns and set index of dataframe
    return df.to_html()

#Close browser and return data
browser.quit()
return data

if __name__ == "__main__":
# If running as script, print scraped data
print(scrape_all())