import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# Set up the web driver
PATH = "/home/okori/Downloads/chromedriver_linux64/chromedriver"
driver = webdriver.Chrome(PATH)

# Set up the product search and get the web page
product = "Samsung"
driver.get("https://jumia.ug/")
search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))

search.send_keys(product)
search.send_keys(Keys.RETURN)

# Set up the list to store the product data
products = []

# Loop through max_pages and extract data
max_pages = 1
pg_ctr = 0

while pg_ctr < max_pages:
    try:
        # Wait for the page to load
        main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "jm")))

        # Extract data for each product on the page
        articles = main.find_elements(By.TAG_NAME, "article")

        for article in articles:
            try:
                # Extract product link
                product_link = article.find_element(By.CLASS_NAME, "core").get_attribute("href")

                # Open a new tab and switch to it
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])

                # Go to the product page
                driver.get(product_link)

                # Wait for the product page to load
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.-fs20.-pts.-pbxs")))

                try:
                    # Extract product details
                    product_name = driver.find_element(By.CSS_SELECTOR, "h1.-fs20.-pts.-pbxs").text.strip()
                    product_price = driver.find_element(By.CSS_SELECTOR, "span.-b.-ltr.-tal.-fs24").text.strip()
                    product_rating = driver.find_element(By.CSS_SELECTOR, "div.stars._s._al").text.strip()
                    key_features = driver.find_element(By.CSS_SELECTOR, "div.markup.-pam").text.strip()
                    what_in_the_box = driver.find_element(By.CSS_SELECTOR, "div.markup.-pam").text.strip()
                    specifications = driver.find_element(By.CSS_SELECTOR, "div.-pvs.-mvxs.-phm.-lsn").text.strip()

                    # Add product data to list
                    products.append([product_name, product_price, product_rating, key_features, what_in_the_box, specifications])
                except Exception as e:
                    print(f"Error extracting product details: {e}")

                # Close the product page and switch back to the main page
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print(f"Error opening product page: {e}")

        # Increment the page counter
        pg_ctr += 1

        # Check if there is a next page
        next_button = driver.find_elements(By.CSS_SELECTOR, "a.pg[aria-label='Next Page']")
        if next_button:
            next_page_url = next_button[0].get_attribute('href')
            driver.get(next_page_url)
        else:
            break

    except Exception as e:
        print(f"Error extracting products from page: {e}")
        break

# Save product data to a CSV file
filename = "jumia_products.csv"
with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Product Name", "Price", "Rating", "Key Features", "What's in the Box", "Specifications"])
    for product in products:
        writer.writerow(product)

# Quit the web driver
driver.quit()