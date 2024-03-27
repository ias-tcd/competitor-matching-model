import glob
import os
import re
from time import sleep

#import filetypex
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

companies_to_urls: dict[str, list[str]] = {
    # "adidas": ["https://www.adidas.ie/men-t_shirts"],
    # "nike": ["https://eu.puma.com/de/en/men/clothing/t-shirts-and-tops"],
    "puma": ["https://eu.puma.com/ie/en/women/clothing/t-shirts-and-tops", ],
    # "reebok": ["https://www.reebok.eu/en-ie/shopping/men-clothing-t-shirts-tops-tanks"],
    # "under_armour": [],
    # "north_face": ["https://www.thenorthface.ie/shop/en-gb/tnf-ie/women-tops-t-shirts-shirts"],
    # "new_balance": [],
    # "lululemon": [],
}


# previous links 
# "https://eu.puma.com/ie/en/men/clothing/sweatshirts-and-hoodies"
# https://www.selenium.dev/documentation/
# https://requests.readt
# hedocs.io/en/latest/api/

# create the images directory in home if it doesn't exist
images_path = "./images"
if not glob.glob(images_path):
    os.mkdir(images_path)


for company, urls in companies_to_urls.items():
    company_images_dir = f"{images_path}/{company}"
    if not glob.glob(company_images_dir):
        os.mkdir(company_images_dir)

    img_num = 0

    for url in urls:
        # using selenium here to deal with sites that use js
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(url=url)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        driver.quit()

        # get all img tag on site
        for img_num, img in enumerate(soup.find_all("img")):
            src = img.get("src")

            if src and re.match("https:*", src):
                img_bytes = requests.get(url=src, timeout=2).content
                img_path = f"{company_images_dir}/{company}_img_{str(img_num).zfill(3)}.jpg"

                # write img bytes to file-like obj
                with open(img_path, "wb") as f:
                    f.write(img_bytes)
                    f.close()

                # wait in between requests
                sleep(1.5)

                # hello

                #// python library - import filetype
