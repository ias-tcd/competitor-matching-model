import glob
import os
import random
import re
from base64 import b64decode
from time import sleep
from typing import Pattern

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

companies_to_urls: dict[str, list[str]] = {
    "adidas": [
        "https://www.adidas.ie/men-t_shirts",
        "https://www.adidas.ie/men-black-shoes",
        "https://www.adidas.ie/men-hoodies",
        "https://www.adidas.ie/logo_print",
        "https://www.adidas.ie/logo_print?start=48",
        "https://www.pinterest.ie/search/pins/?q=adidas&rs=typed",
        "https://www.pinterest.ie/adidas/adidas-originals/",
        "https://www.pinterest.ie/adidas/adidas-originals/",
        "https://i.pinimg.com/originals/3b/6f/2f/3b6f2f7ccfb91210e53623871ccb60cd.jpg",
        "https://www.pinterest.ie/search/pins/?q=adidas%20streetwear&rs=typed",
        "" "",
    ],
    "nike": [],
    "puma": [],
    "reebok": [],
    "under_armour": [],
    "north_face": [],
    "new_balance": [],
    "lululemon": [],
}

MAX_NUM_IMAGES_TO_COLLECT_PER_PAGE = 20
PINTEREST_URL_PATTERN: str | Pattern[str] = re.compile(r"https://www.pinterest.(com|ie)*")

# https://www.selenium.dev/documentation/
# https://requests.readthedocs.io/en/latest/api/

# create the images directory in home if it doesn't exist
images_path = "./images"
if not glob.glob(images_path):
    os.mkdir(images_path)


for company, urls in companies_to_urls.items():
    company_images_dir = f"{images_path}/{company}"

    if not glob.glob(company_images_dir):
        os.mkdir(company_images_dir)

    # start img_num
    last_saved_img_num = len(os.listdir(company_images_dir)) - 1
    # num_i = 0 if not company_images else int(sorted(company_images)[-1:][0][-3:])

    for url in urls:
        # using selenium here to deal with sites that use js
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(url=url)

        # pinterest take a while to load
        if re.match(PINTEREST_URL_PATTERN, url):
            driver.implicitly_wait(30)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        driver.quit()

        # get all img tag on site
        img_num: int

        for img_num, img in soup.find_all("img")[:MAX_NUM_IMAGES_TO_COLLECT_PER_PAGE]:
            src = img.get("src")

            if src:
                img_bytes: bytes
                img_path = f"{company_images_dir}/{company}_img_{str(img_num+last_saved_img_num).zfill(3)}"

                if re.match("https:*", src):
                    img_bytes = requests.get(url=src, timeout=2).content

                    # wait in between requests
                    sleep(random.random() * 3 + 0.3)  # nosec - random delays are a better than same delay...
                elif re.match(r"data:image/(jpeg|png);base64,/*", src):
                    base64_encoding = re.sub("data:image/(jpeg|png);base64,", "", src)
                    img_bytes = b64decode(base64_encoding)

                # write img bytes to file-like obj
                with open(img_path, "wb") as f:
                    f.write(img_bytes)
                    f.close()
