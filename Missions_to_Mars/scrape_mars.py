# Dependencies
import os
from bs4 import BeautifulSoup as bs, re
from splinter import Browser
from datetime import datetime

# -----------------------------------------------------------------------------------------#
# Function to return Beautifulsoup
# -----------------------------------------------------------------------------------------#

# Function to create beautiful soup object, for the given url and browser
def Create_BeautifulSoup(url,browser):
    browser.visit(url)
    
    # Get html content of the visited page
    html_content = browser.html

    # Create a Beautiful Soup object, for the browser html
    soup = bs(html_content, 'html.parser')
    
    return soup  
# -- End of Create_BeautifulSoup -- #

def Scrape_Mars():

    try:        
    # Chrome Driver
        executable_path = {'executable_path': '/Chromedrv/chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
    except:
        # On error, return Status as False, with empty value
        return_value = {"status":False,"Error":{}}

    # Variable to hold Scrape time, for data timestamp
    current_datetime = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")

    try:
        # List to store Scrape data
        MarsScrape = []    

        # -----------------------------------------------------------------------------------------#
        # Scrape NASA Mars News
        # -----------------------------------------------------------------------------------------#

        #URL for NASA News Website
        url = 'https://mars.nasa.gov/news'

        # Create a Beautiful Soup object, for the browser html
        soup = Create_BeautifulSoup(url,browser)

        #Search for the 1st article/news
        NewsSlide = soup.find('section',class_='grid_gallery').find('div',class_='list_text')

        #Scrate the title and article teaser
        news_title = NewsSlide.find('div',class_='content_title').text
        news_teaser = NewsSlide.find('div',class_='article_teaser_body').text

        # Create a empty dictionary to store scrape data
        MarsDetail = {}
        
        # update the dictionary with the Scraped data, and give it a tag / group
        MarsDetail["title"] = news_title
        MarsDetail["teaser"] = news_teaser
        MarsDetail["group"] = "latest news"
        MarsDetail["time_stamp"] = current_datetime

        # Append the dictionary to the MarsScrape list 
        MarsScrape.append(dict(MarsDetail))

        # -----------------------------------------------------------------------------------------#
        # JPL Mars Space Images - Featured Image
        # -----------------------------------------------------------------------------------------#

        #URL for JPL 
        jpl_url = 'https://www.jpl.nasa.gov'

        # URL to search for featured Mars image
        url = jpl_url + '/spaceimages/index.php?category=Mars'

        # Create a Beautiful Soup object, for the browser html
        soup = Create_BeautifulSoup(url,browser)

        #Search for the 1st article/news
        ImageSlide = soup.find('ul',class_='articles').find('a',class_='fancybox')

        #Scrate the title and article teaser
        featured_image_url = jpl_url + ImageSlide['data-fancybox-href']
        featured_image_title = ImageSlide['data-title']
        featured_image_teaser = ImageSlide['data-description']

        # reset the dictionar to empty
        MarsDetail = {}

        # update the dictionary with the Scraped data, and give it a tag / group
        MarsDetail["title"] = featured_image_title
        MarsDetail["img_url"] = featured_image_url
        MarsDetail["teaser"] = featured_image_teaser
        MarsDetail["group"] = "featured image"
        MarsDetail["time_stamp"] = current_datetime

        # Append the dictionary to the MarsScrape list 
        MarsScrape.append(dict(MarsDetail))


        # -----------------------------------------------------------------------------------------#
        # Mars Weather
        # -----------------------------------------------------------------------------------------#

        # URL of Mars weather twitter account
        url = 'https://twitter.com/marswxreport?lang=en'

        # Create a Beautiful Soup object, for the browser html
        soup = Create_BeautifulSoup(url,browser)

        #Search for the latest tweet
        tweetContainer = soup.find('div',class_='js-tweet-text-container').find('p')
        tweetImageText = tweetContainer.find('a').text
        mars_weather = tweetContainer.text
        mars_weather = mars_weather.replace(tweetImageText, "")

        # reset the dictionar to empty
        MarsDetail = {}

        # update the dictionary with the Scraped data, and give it a tag / group
        MarsDetail["weather"] = mars_weather
        MarsDetail["group"] = "current weather"
        MarsDetail["time_stamp"] = current_datetime

        # Append the dictionary to the MarsScrape list 
        MarsScrape.append(dict(MarsDetail))

        # -----------------------------------------------------------------------------------------#
        # Mars Facts
        # -----------------------------------------------------------------------------------------#

        # URL of Mars facts
        url = 'https://space-facts.com/mars/'

        # Create a Beautiful Soup object, for the browser html
        soup = Create_BeautifulSoup(url,browser)

        MarsDetail = {}

        #Parse through the fact table
        mars_fact_table = soup.find(id="tablepress-p-mars-no-2").find_all("tr")
        for mars_fact in mars_fact_table:
            fact_cell = mars_fact.find_all("td")    
            MarsDetail["title"] = fact_cell[0].text.replace(":","")
            MarsDetail["detail"] = fact_cell[1].text
            MarsDetail["group"] = "facts"
            MarsDetail["time_stamp"] = current_datetime

            # Append the dictionary to the MarsScrape list 
            MarsScrape.append(dict(MarsDetail))


        # -----------------------------------------------------------------------------------------#
        # Mars Hemispheres
        # -----------------------------------------------------------------------------------------#

        # URL of Mars facts
        base_url = "https://astrogeology.usgs.gov"
        url = base_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

        # Create a Beautiful Soup object, for the browser html
        soup = Create_BeautifulSoup(url,browser)

        # get all sections containing the result
        hemisphereSlides = soup.find("div",class_="results").find_all("div",class_="description")

        # Create variables to store Image Link detail. 
        imageDict = {}

        # Loop through each of the result, and get the full resolution image link
        for slide in hemisphereSlides:    
            hemisphereName = slide.find('a',class_='product-item').text.replace("Enhanced","").strip()
            hemisphereUrl = base_url + slide.a["href"]      

            # browse each url, to get the enhanced image link           
            # Create a Beautiful Soup object, for the browser html
            soup2 = Create_BeautifulSoup(hemisphereUrl,browser)
            
            #Search the line item, in the download dection
            ImageURL = soup2.find("div",class_="downloads").find("a",text="Sample")
            
            #Create dictionary, of detail captured
            imageDict["title"] = hemisphereName
            imageDict["img_url"] = ImageURL.get("href")
            imageDict["group"] = "hemisphere"
            imageDict["time_stamp"] = current_datetime
            
            # Append the dictionary to the final list
            MarsScrape.append(dict(imageDict))

        # quit browser
        browser.quit()

        # return value along with scrape status
        return_value = {"status":True,"value":MarsScrape}
    except:
        # On error, return Status as False, with empty value
        return_value = {"status":False}
        browser.quit()

    # return the Scrape result
    return return_value

# -- End of function doScrapeMars -- #
