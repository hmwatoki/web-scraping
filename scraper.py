from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import csv
import random

# Get the path to your Chrome user data directory
chrome_user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data")

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={chrome_user_data_dir}")
options.add_argument("--disable-cache")  # Disable browser caching

# Create a new instance of the Chrome driver with your user data directory
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Read the links from the CSV file
with open('input.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    links = []
    for row in reader:
        links.extend(row)

# Create a CSV file and a writer object
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'Title', 'Company']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    scrape_count = 0
    for link in links:
        url = link
        driver.get(url)

        # Introduce a 50-second sleep after navigating to a new link
        time.sleep(25)

        max_retries = 3  # Maximum number of retries
        retry_count = 0
        scraped_successfully = False

        while retry_count < max_retries and not scraped_successfully:
            try:
                # Wait for the page to load
                wait = WebDriverWait(driver, 300)  # Maximum wait time of 300 seconds (5 minutes)
                name_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2.sc-f3b80a80-1.hbvnEe")))
                title_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h4.sc-f3b80a80-2.gqcPin")))
                company_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3.sc-f3b80a80-3.epmPKC")))

                name = name_element.text.strip() if name_element else "Not found"
                title = title_element.text.strip() if title_element else "Not found"
                company = company_element.text.strip() if company_element else "Not found"

                if name == "Not found" or title == "Not found" or company == "Not found":
                    print(f"Retry {retry_count + 1}: Scraping returned empty values. Retrying...")
                    retry_count += 1
                    driver.refresh()  # Refresh the page before retrying
                    time.sleep(35)
                else:
                    print(f"Name: {name}")
                    print(f"Title: {title}")
                    print(f"Company: {company}")
                    scraped_successfully = True  # Set the flag to indicate successful scraping
                    break
            except StaleElementReferenceException:
                print(f"Stale element reference error occurred. Retrying...")
                retry_count += 1
                driver.refresh()  # Refresh the page before retrying
                time.sleep(35)
            except Exception as e:
                print(f"Error occurred: {e}")
                retry_count += 1
                driver.refresh()  # Refresh the page before retrying
                time.sleep(35)

        if scraped_successfully:
            # Write the scraped data to the CSV file
            writer.writerow({'Name': name, 'Title': title, 'Company': company})

        scrape_count += 1

        # Mimic human browsing by resting for 2-3 minutes randomly after every 10 scrapes
        if scrape_count % 10 == 0:
            rest_time = random.randint(120, 180)  # 2-3 minutes
            print(f"Resting for {rest_time} seconds...")
            time.sleep(rest_time)

        # Move to the next link only if the current link was scraped successfully or retries were exhausted
        if not scraped_successfully and retry_count == max_retries:
            print("Maximum retries reached. Unable to scrape data for this link.")

# Keep the browser open until you're ready to close it
input("Press Enter to close the browser...")
driver.quit()