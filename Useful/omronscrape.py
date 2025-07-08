import requests
from bs4 import BeautifulSoup
import csv

def scrape_links_and_save(url, output_file='omron.csv'):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    product_divs = soup.find_all('div', class_='prlie')
    
    links = []
    for div in product_divs:
        a_tag = div.find('a', class_='prtu')
        if a_tag and a_tag.get('href'):
            links.append(a_tag['href'])
    
    # Write to CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Link'])  # header
        for link in links:
            writer.writerow([link])
    
    print(f"Saved {len(links)} links to {output_file}")

# Example usage:
url = "https://www.yaotaishcnc.com/omron/index_2.html"  # Replace with your target URL
scrape_links_and_save(url)
