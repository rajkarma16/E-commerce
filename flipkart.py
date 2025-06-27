import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

searchterm = input("Enter your search term: ")

# Setup Chrome in headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=options)
driver.get("https://www.flipkart.com/")
time.sleep(3)

# Close login popup if present
try:
    driver.find_element(By.XPATH, '//span[@class="_30XB9F"]').click()
except NoSuchElementException:
    pass

# Search for product
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(searchterm)
driver.find_element(By.XPATH, '//button[@class="_2iLD__"]').click()
time.sleep(3)

# Prepare CSV file
csv_file = open("flipkart_data.csv", mode="w", newline="", encoding="utf-8")
writer = csv.writer(csv_file)
writer.writerow(["Brand", "Title", "Price", "Ratings", "Image_URL", "Product_URL"])

page_count = 0

while page_count < 5:  # Scrape first 5 pages to avoid long runs
    time.sleep(3)
    
    products = driver.find_elements(By.XPATH, '//a[contains(@class,"rPDeLR") or contains(@class,"VJA3rP") or contains(@class,"CGtC98")]')

    product_links = [p.get_attribute("href") for p in products if p.get_attribute("href")]

    for link in product_links:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        time.sleep(2)

        try:
            brand = driver.find_element(By.CLASS_NAME, "mEh187").text
        except NoSuchElementException:
            brand = ""

        try:
            title = driver.find_element(By.CLASS_NAME, "VU-ZEz").text
        except NoSuchElementException:
            title = ""

        try:
            price = driver.find_element(By.CLASS_NAME, "Nx9bqj").text
        except NoSuchElementException:
            price = ""

        try:
            ratings = driver.find_element(By.CLASS_NAME, "Y1HWO0").text
        except NoSuchElementException:
            ratings = ""

        try:
            image = driver.find_element(By.XPATH, '//img[contains(@class,"_53J4C-") or contains(@class,"DByuf4")]').get_attribute("src")
        except NoSuchElementException:
            image = ""

        writer.writerow([brand, title, price, ratings, image, link])

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    # Move to next page
    try:
        next_button = driver.find_element(By.XPATH, '//a[@class="_1LKTO3"][2]')
        next_button.click()
    except NoSuchElementException:
        break

    page_count += 1

csv_file.close()
driver.quit()

print("Scraping completed. Data saved to flipkart_data.csv.")
