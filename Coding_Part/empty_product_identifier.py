#step 5

import csv
csv_file = 'input_urls.csv'
with open(csv_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        for link in row:
            if '#' in link:
                print(link)