import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to scrape data from Amazon.in search results and print products
def scrape_amazon_category(category):
    options = webdriver.EdgeOptions()
    options.use_chromium = True
    options.add_argument('--headless')  # To run the browser in headless mode
    driver = webdriver.Edge(options=options)

    search_url = f"https://www.amazon.in/s?k={category.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(2)  # Wait for the page to load

    # Get the total number of pages
    try:
        last_page_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//li[@class="a-disabled" and contains(@class,"a-last")]/a'))
        )
        last_page = int(last_page_element.text)
    except (NoSuchElementException, TimeoutException):
        last_page = 1

    print("Total Pages:", last_page)

    # Loop through each page to scrape data
    for page_number in range(1, last_page + 1):
        if page_number > 1:
            page_url = f"{search_url}&page={page_number}"
            driver.get(page_url)
            time.sleep(2)  # Wait for the page to load

        # Extract data from the page
        products = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
        print("Number of Products on Page", page_number, ":", len(products))
        for product in products:
            try:
                title = product.find_element(By.XPATH, './/h2/a/span').text
                
                price = product.find_element(By.XPATH,".//span[@class='a-price-whole']").text
                rating = product.find_element(By.XPATH, './/span[@class="a-icon-alt"]').get_attribute('innerHTML').strip().split(' ')[0]

                # Print product details
                print("Title:", title)
                print("Price:", price)
                print("Rating:", rating)
                print("="*50)
            except NoSuchElementException:
                print("Failed to extract product details")
                continue

    driver.quit()

# Example usage
category = input("Enter the product category: ").strip()
scrape_amazon_category(category)                                                          