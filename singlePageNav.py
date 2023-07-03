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

main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "jm")))

# Navigate through all pages
while True:
    # Get all product links
    product_links = []
    link_elements = driver.find_elements(By.CLASS_NAME, "core")
    for link_element in link_elements:
        product_links.append(link_element.get_attribute("href"))

    # Open the CSV file and create the writer
    filename = "jumia_product_navigation.csv"
    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Check if the file is empty
        is_file_empty = file.tell() == 0

        # Iterate over product links
        for link in product_links:
            product_data = []
            product_images = []

            # Go to the product page
            driver.get(link)

            # Wait for the product page to load
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.-fs20.-pts.-pbxs")))

            # Extract product details
            product_name = driver.find_element(By.CSS_SELECTOR, "h1.-fs20.-pts.-pts.-pbxs").text.strip()
            product_price = driver.find_element(By.CSS_SELECTOR, "span.-b.-ltr.-tal.-fs24").text.strip()
            product_rating = driver.find_element(By.CSS_SELECTOR, "div.stars._s._al").text.strip()
            key_features = driver.find_element(By.CSS_SELECTOR, "div.markup.-pam").text.strip()
            specifications = driver.find_element(By.CSS_SELECTOR, "ul.-pvs.-mvxs.-phm.-lsn").text.strip()

            # Extract product images
            image_elements = driver.find_elements(By.CSS_SELECTOR, "img.-fw.-fh")
            for image_element in image_elements:
                image_url = image_element.get_attribute("src")
                product_images.append(image_url)

            # Add product data to the list
            product_data.extend([product_name, product_price, product_rating, key_features, specifications, product_images])

            # Write the header row if the file is empty
            if is_file_empty:
                writer.writerow(["Product Name", "Price", "Rating", "Key Features", "Specifications", "Product images"])
                is_file_empty = False

            # Write the product data to the CSV file
            writer.writerow(product_data)

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
