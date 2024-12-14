import requests
from bs4 import BeautifulSoup

# URL of the page containing the table
url = 'https://your-website-link-here.com'

# Send a request to the website
response = requests.get(url)

# Parse the content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all table rows
rows = soup.find_all('tr')[1:]  # Skip the header row

# Create a list to store the names and their Urdu translations
names_and_urdu = []

# Loop through each row and extract the data
for row in rows:
    # Find all columns (td tags) in the row
    cols = row.find_all('td')
    
    # Extract name and Urdu translation (from the second <a> tag inside the third column)
    name = cols[0].find('a').text.strip()  # Name is in the first column
    urdu = cols[2].find('a').text.strip()  # Urdu translation is in the third column
    
    # Append to the list
    names_and_urdu.append((name, urdu))

# Print the extracted names and Urdu translations
for name, urdu in names_and_urdu:
    print(f"Name: {name}, Urdu: {urdu}")
