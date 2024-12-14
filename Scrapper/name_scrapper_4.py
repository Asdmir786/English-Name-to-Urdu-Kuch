import requests
from bs4 import BeautifulSoup
import csv
import os
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Base URL of the page containing the alphabet links
base_url = 'https://hamariweb.com/names/muslim/'

# Send a request to the base URL to get the alphabet links
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Define the output directory
output_dir = r'C:\Users\asmir\Desktop\English-Name-to-Urdu-Kuch\Output'
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Function to scrape names for a given category (boys or girls)
def scrape_names(category, link_selector, file_prefix):
    logging.info(f'Starting to scrape {category} names...')
    
    # Find the section containing the alphabet links for the given category
    alphabet_links = soup.select(link_selector)
    
    # Loop through each alphabet link
    for link in tqdm(alphabet_links, desc=f'Scraping {category} names'):
        alphabet = link.text.strip()
        url = 'https://hamariweb.com' + link['href']
        
        logging.info(f'Scraping names starting with {alphabet} for {category}...')
        
        # Create a list to store the names and their Urdu translations for the current alphabet
        english_and_urdu_names = []
        
        # Start with the first page for the current alphabet
        page_number = 1
        
        while True:
            # Construct the full URL for the current page
            page_url = f'{url}page-{page_number}/'
            
            logging.debug(f'Requesting URL: {page_url}')
            
            # Send a request to the website
            response = requests.get(page_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all table rows
            rows = soup.find_all('tr')[1:]  # Skip the header row
            
            # If no rows are found, break the loop
            if not rows:
                logging.info(f'No more rows found for {alphabet} on page {page_number}.')
                break
            
            # Loop through each row and extract the data
            for row in rows:
                # Find all columns (td tags) in the row
                cols = row.find_all('td')
                
                # Extract name in English and Urdu translation (from the second <a> tag inside the third column)
                name_in_english = cols[0].find('a').text.strip()  # Name in English is in the first column
                name_in_urdu = cols[2].find('a').text.strip()  # Name in Urdu is in the third column
                
                # Append to the list
                english_and_urdu_names.append((name_in_english, name_in_urdu))
            
            # Check if there is a "Next" page link
            next_page = soup.find('a', text='Next')
            if not next_page:
                logging.info(f'No next page found for {alphabet} on page {page_number}.')
                break
            
            # Increment the page number
            page_number += 1
        
        # Define the output file path for the current alphabet
        output_file = os.path.join(output_dir, f'{file_prefix}_{alphabet}.csv')
        
        # Write the extracted names and Urdu translations to a CSV file
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name in English', 'Name in Urdu'])  # Write the header
            writer.writerows(english_and_urdu_names)  # Write the data
        
        logging.info(f'Finished writing names starting with {alphabet} for {category} to {output_file}.')

# Scrape names for boys
scrape_names('boy', 'ul.alphabad_row li.boy_li a', 'english_and_urdu_names_muslim_boys')

# Scrape names for girls
scrape_names('girl', 'ul.alphabad_row li.girl_li a', 'english_and_urdu_names_muslim_girls')
