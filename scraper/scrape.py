import glob
import os

companies_to_urls = {
    "adidas": ["https://www.adidas.ie/men-t_shirts"],
    "nike": [],
    "puma": [],
    "reebok": [],
    "under_armour": [],
    "north_face": [],
    "new_balance": [],
    "lululemon": [],
}

# create the images directory in home if it doesn't exist
images_path = f"{os.path.expanduser('~')}/images"
if not glob.glob(images_path):
    os.mkdir(images_path)
