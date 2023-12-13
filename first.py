import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium.webdriver.common.by import By

# Create Edge WebDriver with the --enable-chrome-browser-cloud-management flag
options = webdriver.EdgeOptions()
options.add_argument('--enable-chrome-browser-cloud-management')
driver = webdriver.Edge(options=options)

# Initialize a list to store data
all_data = []


# Loop through pages from 1 to 10
for page_number in range(2):
    # Construct the URL for the current page
    current_url = f'https://www.bbc.com/news/technology?page={page_number}'
    driver.get(current_url)
    time.sleep(5)

    # Initialize lists to store individual column data
    titles = []
    sources = []
    abstracts = []
    article_contents = []
    urls=[]

    # Function to extract data from the current page
    def extract_data_from_page():
        anchor_elements = driver.find_elements(By.TAG_NAME, 'a')
        for anchor_element in anchor_elements:
            # Check if the element has the specified class name
            if 'ssrcss-9haqql-LinkPostLink ej9ium92' in anchor_element.get_attribute('class'):
                href_value = anchor_element.get_attribute('href')
                urls.append(href_value)
        print(urls)

        # Loop through the URLs
        for url in urls:
            if "https://www.bbc.com/news" in url:
                driver.get(url)
                time.sleep(5)
                title_element = driver.find_element(By.TAG_NAME, 'h1')
                source_element = url
                abstract_elements = driver.find_elements(By.CLASS_NAME, "ssrcss-hmf8ql-BoldText.e5tfeyi3")
                print(abstract_elements)
                if abstract_elements:
                    abstract = abstract_elements[0].text
                else:
                    abstract = "No elements found with the specified class name."

                article_elements = driver.find_elements(By.CSS_SELECTOR, '.ssrcss-1q0x1qg-Paragraph.e1jhz7w10')
                article_content = '\n'.join(paragraph.text for paragraph in article_elements[1:len(article_elements)-1])

                title = title_element.text
                source = source_element

                titles.append(title)
                sources.append(source)
                abstracts.append(abstract)
                article_contents.append(article_content)

    # Extract data from the current page
    extract_data_from_page()

    # Extend the all_data list with data from the current page
    all_data.extend(list(zip(titles, sources, abstracts, article_contents)))

# Create a DataFrame
df = pd.DataFrame(all_data, columns=['Title', 'Source', 'Abstract', 'Article Content'])

# Display the DataFrame
print(df['Abstract'])

driver.quit()
