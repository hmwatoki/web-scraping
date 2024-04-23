from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup

# Replace the path with the actual path to the WebDriver executable
options = webdriver.EdgeOptions()
options.add_argument("--user-data-dir=C:\\Users\\HP Harry\\AppData\\Local\\Microsoft\\Edge\\User Data")
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

url = "https://learningtechnologies.app.swapcard.com/event/learning-and-hr-technologies-uk-2024/my-visit/networking"
driver.get(url)

html_content = driver.page_source

soup = BeautifulSoup(html_content, "html.parser")

name_element = soup.select_one("h2.sc-f3b80a80-1.hbvnEe")
title_element = soup.select_one("h4.sc-f3b80a80-2.gqcPin")
company_element = soup.select_one("h3.sc-f3b80a80-3.epmPKC")

name = name_element.get_text(strip=True) if name_element else "Not found"
title = title_element.get_text(strip=True) if title_element else "Not found"
company = company_element.get_text(strip=True) if company_element else "Not found"

print(f"Name: {name}")
print(f"Title: {title}")
print(f"Company: {company}")

driver.quit()
