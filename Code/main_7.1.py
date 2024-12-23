import os
import csv
from tqdm import tqdm  # Import tqdm for the progress bar
import time  # Import time to measure processing duration

# List of keywords to skip
keywords_to_skip = [
    "(PRIVATE)", "LIMITED", "(PVT.)", "(PAKISTAN)", "MILLS", "ENTERPRISES",
    "SERVICES", "COMPANY", "(SMC-PRIVATE)", "MOTORS", "TECHNOLOGY", "RESEARCH",
    "ENERGY", "MARKETING", "PLANT", "PROCESSING"
]

def search_name_in_csvs(name, base_dir='Output_Scraper'):
    found_in = set()  # To track which subdirectories the name is found in
    urdu_name = None

    # Iterate over all subdirectories and files in the base directory
    for subdir, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    # Skip the header
                    next(reader, None)
                    for row in reader:
                        if len(row) >= 2 and row[0].strip().lower() == name.lower():
                            found_in.add(os.path.basename(subdir))  # Add the subdirectory name
                            urdu_name = row[1]
                            break
            if urdu_name:
                break

    # Determine gender based on subdirectory names
    if 'Boys' in found_in and 'Girls' in found_in:
        gender = "صاحب/صاحبہ"
        gender_english = "male/female"
    elif 'Boys' in found_in:
        gender = "صاحب"
        gender_english = "male"
    elif 'Girls' in found_in:
        gender = "صاحبہ"
        gender_english = "female"
    else:
        gender = "N/A"
        gender_english = "N/A"

    return urdu_name, gender, gender_english

def process_input_file(input_file, output_file, base_dir='Output_Scraper'):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['SR', 'NTN', 'NAME', 'NAME IN URDU', 'Sahib/Sahiba', 'Gender']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Use tqdm to create a progress bar
        for row in tqdm(reader, desc="Processing rows", unit="row"):
            name = row['NAME'].strip()
            # Check if the name contains any of the keywords to skip
            if any(keyword in name for keyword in keywords_to_skip):
                row['NAME IN URDU'] = "N/A"
                row['Sahib/Sahiba'] = "N/A"
                row['Gender'] = "N/A"
            else:
                name_parts = name.split()
                urdu_names = []
                sahib_sahiba = "N/A"
                gender_english = "N/A"
                for part in name_parts:
                    urdu_name, part_sahib_sahiba, part_gender_english = search_name_in_csvs(part, base_dir)
                    if urdu_name:
                        urdu_names.append(urdu_name)
                        if sahib_sahiba == "N/A":  # Set sahib/sahiba based on the first name part found
                            sahib_sahiba = part_sahib_sahiba
                        if gender_english == "N/A":  # Set gender based on the first name part found
                            gender_english = part_gender_english
                row['NAME IN URDU'] = " ".join(urdu_names) if urdu_names else name
                row['Sahib/Sahiba'] = sahib_sahiba
                row['Gender'] = gender_english

            writer.writerow({field: row[field] for field in fieldnames})

def main():
    input_file = r'C:\Users\asmir\Desktop\English-Name-to-Urdu-Kuch\input_0-20000.csv'
    output_file = r'Output_Code\output.csv'
    
    start_time = time.time()  # Record the start time
    process_input_file(input_file, output_file)
    end_time = time.time()  # Record the end time
    
    total_time = end_time - start_time
    print(f"Total processing time: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()
