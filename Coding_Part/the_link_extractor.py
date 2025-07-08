#step 1
import requests
from bs4 import BeautifulSoup
import csv

start_page = 2
end_page = 100

output_file = 'fanuc_link.csv'

all_links = []

for i in range(start_page, end_page + 1):
    url = f'https://www.yaotaishcnc.com/ab/index_{i}.html'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', class_='prtu')

        for link in links:
            href = link.get('href')
            if href:
                all_links.append([href])

        print(f"Page {i} scraped successfully.")
    except Exception as e:
        print(f"Failed to scrape page {i}: {e}")


with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Link'])
    writer.writerows(all_links)

print(f"Saved {len(all_links)} links to {output_file}.")