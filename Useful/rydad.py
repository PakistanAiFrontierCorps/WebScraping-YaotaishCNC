import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Paths
input_csv = "input_urls.csv"
output_dir = "Output CSV"
output_file = os.path.join(output_dir, "products.csv")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read URLs from CSV
url_df = pd.read_csv(input_csv)

# Container for all scraped data
scraped_data = []

# Loop over each URL
for index, row in url_df.iterrows():
    url = row['link']
    print(f"Scraping: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract Product Title
        title_tag = soup.select_one(".jianjie em")
        product_title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # Extract Product Images
        image_tags = soup.select(".item-pic img")
        image_urls = [img['src'] for img in image_tags if img.get("src")]
        product_images = ", ".join(image_urls)

        # Extract Description
        desc_tag = soup.select_one(".jiann.mp")
        description = desc_tag.get_text(strip=True) if desc_tag else "N/A"

        # Add to data list
        scraped_data.append({
            "Product Title": product_title,
            "Product Image": product_images,
            "Description": description
        })

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        scraped_data.append({
            "Product Title": "ERROR",
            "Product Image": "ERROR",
            "Description": f"Failed to scrape: {url}"
        })

# Save all data to CSV
df = pd.DataFrame(scraped_data)
df.to_csv(output_file, index=False)
print(f"Scraping complete. Data saved to {output_file}")
