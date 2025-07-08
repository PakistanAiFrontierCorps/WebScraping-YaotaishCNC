import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Constants
INPUT_CSV = "input_urls.csv"
OUTPUT_DIR = "Output CSV"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "products.csv")
BASE_URL = "https://www.yaotaishcnc.com/"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read URLs from CSV
url_df = pd.read_csv(INPUT_CSV)
scraped_data = []

# Scrape each URL
for index, row in url_df.iterrows():
    url = row['Link']
    print(f"Scraping: {url}")

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract Product Title
        title_tag = soup.select_one(".jianjie em")
        product_title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # Extract Product Images with full URLs
        image_tags = soup.select(".item-pic img")
        image_urls = []
        for img in image_tags:
            src = img.get("src")
            if src:
                full_url = src if src.startswith("http") else BASE_URL + src.lstrip("/")
                image_urls.append(full_url)
        product_images = ", ".join(image_urls)

        # Extract Description
        desc_tag = soup.select_one(".jiann.mp")
        description = desc_tag.get_text(separator=" ", strip=True) if desc_tag else "N/A"

        # Extract SKU from description
        sku_match = re.search(r"Module number[:：]?\s*([A-Za-z0-9\-/_.]+)", description, re.IGNORECASE)
        sku = sku_match.group(1).strip() if sku_match else "N/A"

        # Add to list
        scraped_data.append({
            "SKU": sku,
            "Product Title": product_title,
            "Images": product_images,
            "Description": description,
            "Short description": description,
        })

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        scraped_data.append({
            "SKU": "ERROR",
            "Product Title": "ERROR",
            "Product Image": "ERROR",
            "Description": f"Failed to scrape: {url}",
            "Short description": f"Failed to scrape: {url}"
        })

# Save to CSV
df = pd.DataFrame(scraped_data)
df.to_csv(OUTPUT_FILE, index=False)
print(f"Scraping complete. Data saved to {OUTPUT_FILE}")
