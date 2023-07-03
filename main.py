import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pymongo import MongoClient

# Set up the web driver
PATH = "/home/okori/Downloads/chromedriver_linux64/chromedriver"
driver = webdriver.Chrome(PATH)

# Set up the product search and get the web page
product = "phone"
driver.get("https://jumia.ug/")
search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))

search.send_keys(product)
search.send_keys(Keys.RETURN)

main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "jm")))

# Connect to MongoDB
uri = "mongodb+srv://okoride0:lindahst1@database1.a17zh8w.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["scraped_data"]
collection = db["products"]

# Navigate through all pages
while True:
    # Get all product links
    product_links = []
    link_elements = driver.find_elements(By.CLASS_NAME, "core")
    for link_element in link_elements:
        product_links.append(link_element.get_attribute("href"))

    # Iterate over product links
    for link in product_links:
        product_data = {}
        product_images = []

        # Go to the product page
        driver.get(link)

        # Wait for the product page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.-fs20.-pts.-pbxs")))

        # Extract product details
        product_data["source"] = "From Jumia"
        product_data["name"] = driver.find_element(By.CSS_SELECTOR, "h1.-fs20.-pts.-pts.-pbxs").text.strip()
        product_data["price"] = driver.find_element(By.CSS_SELECTOR, "span.-b.-ltr.-tal.-fs24").text.strip()
        product_data["rating"] = driver.find_element(By.CSS_SELECTOR, "div.stars._s._al").text.strip()
        product_data["key_features"] = driver.find_element(By.CSS_SELECTOR, "div.markup.-pam").text.strip()
        product_data["specifications"] = driver.find_element(By.CSS_SELECTOR, "ul.-pvs.-mvxs.-phm.-lsn").text.strip()

        # Extract product images
        image_elements = driver.find_elements(By.CSS_SELECTOR, "img.-fw.-fh")
        for image_element in image_elements:
            image_url = image_element.get_attribute("src")
            product_images.append(image_url)

        # Add product images to the data
        product_data["images"] = product_images

        # Insert the product data into MongoDB
        collection.insert_one(product_data)

        # Go back to the search page
        driver.back()

    # Go to the next page if available
    next_button = driver.find_elements(By.CSS_SELECTOR, "a.pg[aria-label='Next Page']")
    if next_button:
        next_page_url = next_button[0].get_attribute('href')
        driver.get(next_page_url)
        time.sleep(2)  # Adjust the sleep time if needed
    else:
        break

# Quit the web driver
driver.quit()
