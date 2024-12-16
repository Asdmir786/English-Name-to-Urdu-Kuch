import os
import csv

def search_name_in_csvs(first_name, base_dir='Output_Scraper'):
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
                        if len(row) >= 2 and row[0].strip().lower() == first_name.lower():
                            found_in.add(os.path.basename(subdir))  # Add the subdirectory name
                            urdu_name = row[1]
                            break
            if urdu_name:
                break

    # Determine gender based on subdirectory names
    if 'Boys' in found_in and 'Girls' in found_in:
        gender = "صاحب/صاحبہ"
    elif 'Boys' in found_in:
        gender = "صاحب"
    elif 'Girls' in found_in:
        gender = "صاحبہ"
    else:
        gender = ""

    return urdu_name, gender

def process_input_file(input_file, output_file, base_dir='Output_Scraper'):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['SR', 'NTN', 'NAME', 'NAME IN URDU', 'GENDER']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            name = row['NAME'].strip()
            first_name = name.split()[0]  # Use only the first name for checking
            urdu_name, gender = search_name_in_csvs(first_name, base_dir)
            row['NAME IN URDU'] = urdu_name if urdu_name else name
            row['GENDER'] = gender
            writer.writerow({field: row[field] for field in fieldnames})

def main():
    input_file = r'C:\Users\asmir\Desktop\English-Name-to-Urdu-Kuch\input_0-20000.csv'
    output_file = r'Output_Code\output.csv'
    process_input_file(input_file, output_file)

if __name__ == "__main__":
    main()
