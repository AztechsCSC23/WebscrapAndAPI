import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service

s = Service("/home/okori/Downloads/chromedriver_linux64/chromedriver")

# set up the web driver
driver = webdriver.Chrome(service=s)

# set up the product search and get the web page
product = "Samsung"
driver.get("https://jumia.ug/")
search = driver.find_element("name", "q")
search.send_keys(product)
search.send_keys(Keys.RETURN)

# Create list to store product data
products = []

# loop through the specified number of pages and extract data
max_pages = 3
page_counter = 0

while page_counter < max_pages:
    try:
        # wait for page to load
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "jm"))
        )

        # extract data for each product on the page
        articles = main.find_elements(By.TAG_NAME, "article")
        for article in articles:
            try:
                # extract product name, price, and shipped from abroad status
                product_name = article.find_element_by_class_name("name")
                product_price = article.find_element_by_class_name("prc")
                shipped_from_abroad = "No"
                if article.find_elements_by_css_selector("div.bdg._glb._xs"):
                    shipped_from_abroad = "Yes"

                # Add product data to list
                products.append([product_name.text, product_price.text, shipped_from_abroad])

                # Print the extracted data for verification
                print("Product: ", product_name.text)
                print("Price: ", product_price.text)
                print("Shipped from abroad: ", shipped_from_abroad)

            except:
                pass

        # increment the page counter
        page_counter += 1

        # check if there is a next page
        next_button = driver.find_elements(By.CSS_SELECTOR, "a.pg[aria-label='Next Page']")
        if next_button:
            next_page_url = next_button[0].get_attribute('href')
            driver.get(next_page_url)
            time.sleep(5)

        else:
            break  # no more pages, exit loop

    except:
        break  # error loading page, exit loop

# Sort the products by price in ascending order
products.sort(
    key=lambda x: float(sum([float(p.replace("UGX ", "").replace(",", "")) for p in x[1].split(" - ")]) / len(x[1].split(" - ")))
)

# Print the list of products
print(products)

# set up the CSV file for writing the results
filename = "jumia_products1_sorted_by_price_ascending.csv"
try:
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Product", "Price", "Shipped_from_abroad"])

        # write product name and price to CSV file
        for item in products:
            writer.writerow([elem.encode("utf-8") if isinstance(elem, str) else elem for elem in item])

    print("CSV file created successfully.")
except IOError:
    print("Could not create file")

    print("CSV file created successfully.")

except IOError:
    print("Could not create file")

# quit the web driver
driver.quit()
