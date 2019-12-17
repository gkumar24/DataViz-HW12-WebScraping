from scrape_mars import Scrape_Mars
from flask import Flask, render_template, redirect, url_for
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

def Connect_MongoDB():
    # Create connection variable
    conn = 'mongodb://localhost:27017'

    # Pass connection to the pymongo instance.
    client = pymongo.MongoClient(conn)

    return client
# ---- End of Connect_MongoDB ----#

def Close_Connection_MongoDB(client):
    client.close()
    return True
# ---- End of Close_Connection_MongoDB ----#


# Set route
@app.route('/')
def index():

    # Variable to hold status of mars_db and mars_collection
    dbExist = False
    colExist = False

    # Get client for Mongo DB
    myClient = Connect_MongoDB()

    #Check if mars_db exist, and if db exist, check for mars_collection
    dbList = myClient.list_database_names()
    if "mars_db" in dbList:
        dbExist = True
        marsDB = myClient.mars_db
        colList = marsDB.list_collection_names()
        if "mars_collection" in colList:
            colExist = True
            marsCol = marsDB.mars_collection

    if colExist == True:
        # get the Latest news from Mongo DB
        mars_news = marsCol.find_one({"group":"latest news"})
        # get JPL Featured Image
        mars_featured_image = marsCol.find_one({"group":"featured image"})
        # get Current weather
        mars_current_weather = marsCol.find_one({"group":"current weather"})
        # get facts
        mars_facts = list(marsCol.find({"group":"facts"}))
        # get facts
        mars_hemisphere_images = list(marsCol.find({"group":"hemisphere"}))
    else:
        error_message = list({"Error":"No Data found, Scrape to get data"})
        mars_news = error_message
        mars_featured_image = error_message
        mars_current_weather = error_message
        mars_facts = error_message
        mars_hemisphere_images = error_message

    # Close client
    status = Close_Connection_MongoDB(myClient)   

    # Return the template with the teams list passed in
    return render_template(\
        'index.html', \
        marsNews = mars_news, \
        marsFeaturedImage = mars_featured_image, \
        marsCurrentWeather = mars_current_weather, \
        marsFacts = mars_facts, \
        marsHemisphereImages = mars_hemisphere_images 
    )
# --- End of index route ----#

# Set route
@app.route('/scrape')
def Scrape_And_Store():
    # Scrape Mars Data
    return_value = Scrape_Mars()

    if return_value["status"] == True:
        MarsScrapeData = return_value["value"]

        # Get client for Mongo DB
        myClient = Connect_MongoDB()

        # Connect to a database. Will create one if not already available.
        marsDB = myClient.mars_db    

        # Drops collection if available to remove duplicates
        marsDB.mars_collection.drop()

        # Creates a collection in the database and inserts two documents
        marsDB.mars_collection.insert_many(MarsScrapeData)
        
        # Close client
        status = Close_Connection_MongoDB(myClient)     
        
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

# --- End of scrape route ----#


if __name__ == "__main__":
    app.run(debug=True)

