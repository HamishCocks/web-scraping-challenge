from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



def scrape_data():
    ##set up splinter 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ##news page (headlines and picture)
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    content_title = soup.find("li", class_="slide")
    news_title = content_title.find("div", class_="content_title").get_text()
    news_para = soup.find("div", class_="article_teaser_body").get_text()


    ##JPL page for URL
    jpl_img_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_img_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    my_url = jpl_img_url.rsplit("i", 1)[0]

    featured_image = soup.find("div", class_="header")
    featured_image2 = str(featured_image.find_all('img')[1]["src"])
    featured_image_url = my_url  + featured_image2


    #mars facts - table
    marsf_url = 'https://space-facts.com/mars/'
    browser.visit(marsf_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    marsf_table = pd.read_html(marsf_url)[0]
    marsf_table_html = marsf_table.to_html()


    #hemisphere pictures
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')

    cerberus_title = soup.find("h2", class_ = "title").get_text()
    cerberus_url = soup.find_all("a")[4]["href"]

    browser.visit(hemi_url)
    browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')

    schia_title = soup.find("h2", class_ = "title").get_text()
    schia_url = soup.find_all("a")[4]["href"]

    browser.visit(hemi_url)
    browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')

    syrtis_title = soup.find("h2", class_ = "title").get_text()
    syrtis_url = soup.find_all("a")[4]["href"]

    browser.visit(hemi_url)
    browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')

    valles_title = soup.find("h2", class_ = "title").get_text()
    valles_url = soup.find_all("a")[4]["href"]

    hemisphere_image_urls = [
        {"title": valles_title, "img_url": valles_url},
        {"title": cerberus_title, "img_url": cerberus_url},
        {"title": schia_title, "img_url": schia_url},
        {"title": syrtis_title, "img_url": syrtis_url},
    ]

    ##dictionary for the Pymongo
    mars_data = {
        "news_title":news_title,
        "news_paragraph":news_para,
        "featured_url":featured_image_url,
        "mars_table":marsf_table_html,
        "hemisphere_urls":hemisphere_image_urls
    }

    return mars_data

    browser.quit()
