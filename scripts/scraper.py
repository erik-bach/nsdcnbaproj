import requests
from bs4 import BeautifulSoup
import csv
import os

url = 'https://geojango.com/pages/list-of-nba-teams'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

data_list = []

table_body = soup.find('tbody')  # Find the <tbody> element containing the data rows

for row in table_body.find_all('tr', class_='shogun-table-row-container'):  # Find all rows
    data = {}

    columns = row.find_all('td', class_='shogun-table-row')  # Find all <td> elements within the row

    # Extracting data from each column
    if len(columns) >= 5:  # Make sure there are enough columns
        data['name'] = columns[0].find('span').text.strip() if columns[0].find('span') else ''
        data['arena'] = columns[1].find('span').text.strip() if columns[1].find('span') else ''
        data['location'] = columns[2].find('span').text.strip() if columns[2].find('span') else ''
        data['seating capacity'] = columns[3].find('span').text.strip() if columns[3].find('span') else ''
        data['opening year'] = columns[4].find('span').text.strip() if columns[4].find('span') else ''
        data_list.append(data)

current_directory = os.getcwd()

# Define the path to the raw data folder and the CSV file
raw_folder_path = os.path.join(current_directory, 'data', 'raw')
file_path = os.path.join(raw_folder_path, 'nba_teams.csv')

# Create the raw data folder if it doesn't exist
if not os.path.exists(raw_folder_path):
    os.makedirs(raw_folder_path)

# Write data to the CSV file
with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['name', 'arena', 'location', 'seating capacity', 'opening year']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # Write the header row
    for data in data_list:
        writer.writerow(data)  # Write each data row
