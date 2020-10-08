from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import time
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': r'C:\Users\ppaim\Downloads\chromedriver_win32\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_content = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_content": news_content,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
       "last_modified": dt.datetime.now()
    }
    browser.quit()
    return data


def mars_news(browser):
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    news_soup = soup(html, 'html.parser')
    new_story = news_soup.select_one('ul.item_list li.slide')
    news_title = new_story.find("div", class_="content_title").get_text()
    news_content = new_story.find("div", class_="article_teaser_body").get_text()
    return news_title, news_content


def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image = browser.find_by_id('full_image')
    full_image.click()
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()
    img_html = browser.html
    img_soup = soup(img_html, 'html.parser')
    image_path = img_soup.select_one('figure.lede a img').get('src')
    featured_image_url = f'https://www.jpl.nasa.gov{image_path}'
    return featured_image_url


def mars_facts():
    fact_url = "https://space-facts.com/mars/"
    table = pd.read_html(fact_url)
    fact_df = table[0]
    fact_df.columns = ["Description", "Value"]
    facts_html = fact_df.to_html()
    return facts_html

def hemispheres(browser):
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    hemisphere_image_urls = []
    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        hemisphere['title'] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    return hemisphere_image_urls


if __name__ == "__main__":
    print(scrape_all())

