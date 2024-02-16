import glob
import os
import random
import re
from base64 import b64decode
from time import sleep
from typing import Any, Pattern

import requests
from bs4 import BeautifulSoup, ResultSet
from company_urls import companies_to_urls
from selenium import webdriver

# relevant docs
# https://www.selenium.dev/documentation/
# https://requests.readthedocs.io/en/latest/api/

MAX_NUM_IMAGES_TO_COLLECT_PER_PAGE = 45
pinterest_url_pattern: str | Pattern[str] = re.compile(r"https://www.pinterest.(com|ie)*")
base64_encoded_image_pattern: str | Pattern[str] = re.compile(r"data:image/(jpeg|png);base64,/*")
adidas_src_url_pattern = r"https://assets.adidas.com/images/w_\d+,h_\d+"
pintest_src_url_pattern = r"https://i.pinimg.com/\d+x/*"


def download_images(img_sources: ResultSet[Any], company: str, num_scraped_images_for_current_company: int) -> None:
    for img in img_sources:
        src = img.get("src")
        if not src:
            continue

        img_path = f"{company_images_dir}/{company}_img_{str(num_scraped_images_for_current_company).zfill(3)}"

        img_bytes: bytes
        if re.match(r"https:*", src):
            if re.match(adidas_src_url_pattern, src):
                new_width = random.randint(400, 1000)  # nosec
                new_height = random.randint(400, 1000)  # nosec
                src = re.sub(
                    adidas_src_url_pattern, f"https://assets.adidas.com/images/w_{new_width},h_{new_height}", src
                )
            elif re.match(pintest_src_url_pattern, src):
                src = re.sub(pintest_src_url_pattern, "https://i.pinimg.com/564x/", src)
            img_bytes = requests.get(url=src, timeout=5).content
            # wait in between requests
            sleep(random.random() * 5.3 + 0.8)  # nosec

        elif re.match(base64_encoded_image_pattern, src):
            base64_encoding = re.sub("data:image/(jpeg|png);base64,", "", src)
            img_bytes = b64decode(base64_encoding)

        print("img_src: ", src)

        # write img bytes to file-like obj
        with open(img_path, "wb") as f:
            f.write(img_bytes)
            f.close()

        num_scraped_images_for_current_company += 1


# create the images directory in home if it doesn't exist
images_path = "./images"
if not glob.glob(images_path):
    os.mkdir(images_path)


for company, urls in companies_to_urls.items():
    company_images_dir = f"{images_path}/{company}"

    if not glob.glob(company_images_dir):
        os.mkdir(company_images_dir)

    for url in urls:
        num_scraped_images_for_current_company = len(os.listdir(company_images_dir))
        print("url: ", url)
        # uses selenium here to deal with sites that use js
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(url=url)

        wait_time = 10
        # pinterest take a while to load
        if re.match(pinterest_url_pattern, url):
            wait_time += 10

        driver.implicitly_wait(wait_time)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        download_images(
            soup.find_all("img")[:MAX_NUM_IMAGES_TO_COLLECT_PER_PAGE],
            company,
            num_scraped_images_for_current_company,
        )

        driver.quit()
