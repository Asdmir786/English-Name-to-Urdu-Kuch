import requests
from bs4 import BeautifulSoup
import csv
import os
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the output directory
output_dir = r'C:\Users\asmir\Desktop\English-Name-to-Urdu-Kuch\Output'
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Function to scrape names for a given category (boys or girls)
def scrape_names(base_url, category, file_prefix):
    logging.info(f'Starting to scrape {category} names...')
    
    # Send a request to the base URL to get the names
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching base URL: {e}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the section containing the names
    name_rows = soup.find_all('tr')[1:]  # Assuming the names are in table rows, skip the header row
    
    # Create a list to store the names
    names = []
    
    # Loop through each row and extract the data
    for row in name_rows:
        # Find the first column (td tag) in the row
        name_cell = row.find('td')
        
        # Ensure the cell is found and contains an <a> tag
        if name_cell:
            name_link = name_cell.find('a')
            if name_link:
                # Extract name in English
                name_in_english = name_link.text.strip()
                # Append to the list
                names.append([name_in_english])
            else:
                logging.warning(f"No <a> tag found in row: {row}")
        else:
            logging.warning(f"Skipping row due to unexpected structure: {row}")
    
    # Define the output file path
    output_file = os.path.join(output_dir, f'{file_prefix}.csv')
    
    # Write the extracted names to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name in English'])  # Write the header
        writer.writerows(names)  # Write the data
    
    logging.info(f'Finished writing names for {category} to {output_file}.')

# Scrape Quranic names for boys
scrape_names('https://hamariweb.com/names/quranic-boys-names/', 'quranic boys', 'english_and_urdu_names_quranic_boys')

# Scrape Quranic names for girls
scrape_names('https://hamariweb.com/names/quranic-girls-names/', 'quranic girls', 'english_and_urdu_names_quranic_girls') 