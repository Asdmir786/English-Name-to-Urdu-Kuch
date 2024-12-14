import requests
from bs4 import BeautifulSoup
import csv
import os

# URL of the page containing the table
url = 'https://hamariweb.com/names/muslim-boy-names-starting-with-a/'

# Send a request to the website
response = requests.get(url)

# Parse the content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all table rows
rows = soup.find_all('tr')[1:]  # Skip the header row

# Create a list to store the names and their Urdu translations
english_and_urdu_names = []

# Loop through each row and extract the data
for row in rows:
    # Find all columns (td tags) in the row
    cols = row.find_all('td')
    
    # Extract name in English and Urdu translation (from the second <a> tag inside the third column)
    name_in_english = cols[0].find('a').text.strip()  # Name in English is in the first column
    name_in_urdu = cols[2].find('a').text.strip()  # Name in Urdu is in the third column
    
    # Append to the list
    english_and_urdu_names.append((name_in_english, name_in_urdu))

# Define the output directory and file path
output_dir = r'C:\Users\asmir\Desktop\English-Name-to-Urdu-Kuch\Output'
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
output_file = os.path.join(output_dir, 'english_and_urdu_names.csv')  # Updated file name

# Write the extracted names and Urdu translations to a CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name in English', 'Name in Urdu'])  # Write the header
    writer.writerows(english_and_urdu_names)  # Write the data