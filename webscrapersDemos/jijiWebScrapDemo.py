import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pymongo import MongoClient

#Declare the source from which the data was gathered
source = "From Jiji"

# Set up the web driver
PATH = "/home/okori/Downloads/chromedriver_linux64/chromedriver"
driver = webdriver.Chrome(PATH)

# Maximize the browser window
driver.maximize_window()

# Open the website
driver.get("https://jiji.ug/")

# Wait for the element to be clickable and click it
index = 2
category_elements = WebDriverWait(driver, 10).until(
    EC.visibility_of_all_elements_located(
        (By.XPATH, '//div[@data-index="' + str(index) + '"]/a[contains(@class, "b-categories-item") and contains(@class, "qa-category-parent-item")]')
    )
)
if category_elements:
    category_elements[0].click()

# Wait for the page to load (you may need to modify the wait time based on the website's performance
time.sleep(5)

# Scroll to load more results
prev_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Wait for the new results to load

    # Check if the page height has changed
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == prev_height:
        break  # If the page height hasn't changed, all items have been loaded
    else:
        prev_height = new_height

# Gather item links
item_links = []
item_elements = WebDriverWait(driver, 10).until(
    EC.visibility_of_all_elements_located(
        (By.XPATH, '//div[contains(@class, "js-advert-list-item")]/a[contains(@class, "b-list-advert-base--gallery")]')
    )
)
for item_element in item_elements:
    item_links.append(item_element.get_attribute("href"))


#Declare the uri to connect to the client
uri = "mongodb+srv://okoride0:lindahst1@database1.a17zh8w.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(uri)
db = client["sample_scraped_data"]
collection = "sample_Jiji_products"

# Create a new collection
collection_name = "jijiProducts"  # Replace "your_collection_name" with the desired name for your collection
collection = db[collection_name]

# Iterate through item links and extract information
for item_link in item_links:
    # Open the item link
    driver.get(item_link)

    # Wait for the page to load (you may need to modify the wait time based on the website's performance)
    time.sleep(5)

    # Gather item information
    item_name_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//div[contains(@class, "b-advert-title-inner")]')
        )
    )

    item_price_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "qa-advert-price-view-title")
        )
    )

    description_elements = WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located((By.XPATH, '//div[contains(@class, "b-advert-attributes-wrapper")]'))
    )

    # Extract image URL
    image_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//picture/img[@itemprop="image"]'))
    )

    item_name = item_name_element.text.strip()
    item_price = item_price_element.text.strip()
    image_url = image_element.get_attribute("src")
    negotiable = ""

    # Extract only the price value and remove the negotiability status
    if "Negotiable" in item_price:
        item_price = item_price.replace(", Negotiable", "")
        negotiable = "Yes"
    elif "Non-negotiable" in item_price.lower():
        item_price = item_price.replace(" Non-negotiable", "")
        negotiable = "No"

    # Collect attribute key-value pairs from the description elements
    description = ""
    attribute_set = set()  # Set to track unique attribute keys
    for element in description_elements:
        attribute_elements = element.find_elements(By.CLASS_NAME, "b-advert-attribute")
        for attribute_element in attribute_elements:
            key_element = attribute_element.find_element(By.CLASS_NAME, "b-advert-attribute__key")
            value_element = attribute_element.find_element(By.CLASS_NAME, "b-advert-attribute__value")

            key = key_element.text.strip()
            value = value_element.text.strip()

            if key not in attribute_set:  # Check if key has already been added
                description += f"{key} - {value}\n"
                attribute_set.add(key)
        description += "\n"  # Add a new line after each description block

    # Remove the duplicate description
    description = description.strip()

    # Store the data in MongoDB
    data = {
        "Item Name": item_name,
        "Price": item_price,
        "Negotiable": negotiable,
        "Description": description,
        "Image": image_url,
        "Source": source
    }
    collection.insert_one(data)

# Quit the webdriver
driver.quit()

# Close the MongoDB connection
client.close()
