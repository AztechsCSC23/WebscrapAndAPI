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
product = "Samsung"
driver.get("https://jumia.ug/")
search = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "q"))
)

search.send_keys(product)
search.send_keys(Keys.RETURN)

# Set up the MongoDB connection
uri = "mongodb+srv://okoride0:lindahst1@database1.a17zh8w.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["your_database"]
collection = db["products"]

# Loop through 3 pages
max_pages = 3
pg_ctr = 0

# Loop through all pages and extract data
while pg_ctr < max_pages:
    try:
        # Wait for the page to load
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "jm"))
        )

        # Extract data for each product on the page
        articles = main.find_elements(By.TAG_NAME, "article")
        for article in articles:
            try:
                # Extract product name and price
                product_name = article.find_element(By.CLASS_NAME, "name").text
                product_price = article.find_element(By.CLASS_NAME, "prc").text
                shipped_from_abroad = article.find_elements(By.CSS_SELECTOR, "div.bdg._glb._xs")
                if shipped_from_abroad:
                    shipped_from_abroad = "Yes"
                else:
                    shipped_from_abroad = "No"

                # Insert product data into the MongoDB collection
                collection.insert_one({"product_name": product_name, "product_price": product_price, "shipped_from_abroad": shipped_from_abroad})

            except:
                pass

        # Increment the page counter
        pg_ctr += 1

        # Check if there is a next page
        next_button = driver.find_elements(By.CSS_SELECTOR, "a.pg[aria-label='Next Page']")
        if next_button:
            next_page_url = next_button[0].get_attribute('href')
            driver.get(next_page_url)
            time.sleep(5)

        else:
            break  # No more pages, exit loop

    except:
        break  # Error loading page, exit loop

# Quit the web driver
driver.quit()

# Print success message
print("Scraped data inserted into MongoDB successfully.")

# Close the MongoDB connection
client.close()
