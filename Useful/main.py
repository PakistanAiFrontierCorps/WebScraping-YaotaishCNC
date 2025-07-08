import os
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Replace this with your target URL
url = "https://www.yaotaishcnc.com/mitsubishi/mitsubishi-fcu6-dut32.html"

# Send GET request
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Extract product title from <em> inside .jianjie
title_tag = soup.select_one(".jianjie em")
product_title = title_tag.get_text(strip=True) if title_tag else "N/A"

# Extract image URLs from .item-pic
image_tags = soup.select(".item-pic img")
image_urls = [img['src'] for img in image_tags if img.get("src")]
product_images = ", ".join(image_urls)

# Extract description from .jiann.mp
desc_tag = soup.select_one(".jiann.mp")
description = desc_tag.get_text(strip=True) if desc_tag else "N/A"

# Prepare data
data = [{
    "Product Title": product_title,
    "Product Image": product_images,
    "Description": description
}]

# Ensure output directory exists
output_dir = "Output CSV"
os.makedirs(output_dir, exist_ok=True)

# Save to CSV
output_file = os.path.join(output_dir, "products.csv")
df = pd.DataFrame(data)
df.to_csv(output_file, index=False)

print(f"Data saved to {output_file}")
