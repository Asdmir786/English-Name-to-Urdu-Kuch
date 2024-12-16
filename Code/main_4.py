import os
import csv

def search_name_in_csvs(name, base_dir='Output', output_file='output.txt'):
    found_in = set()  # To track which subdirectories the name is found in
    written_names = {}  # To track names and their Urdu translations

    with open(output_file, 'w', encoding='utf-8') as outfile:
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
                                written_names[row[0]] = row[1]  # Store the English and Urdu names
        
        if not found_in:
            outfile.write(f"Name: {name} not found in any CSV file.\n")
        else:
            # Determine gender based on subdirectory names
            if 'Boys' in found_in and 'Girls' in found_in:
                gender = "both genders"
                prefix = "Mr./Ms."
                suffix = "صاحب/صاحبہ"
            elif 'Boys' in found_in:
                gender = "male"
                prefix = "Mr."
                suffix = "صاحب"
            elif 'Girls' in found_in:
                gender = "female"
                prefix = "Ms."
                suffix = "صاحبہ"
            else:
                gender = "unknown"
                prefix = ""
                suffix = ""

            # Append the appropriate prefix and suffix to the name
            for eng_name, urdu_name in written_names.items():
                outfile.write(f"{prefix} {eng_name}: {urdu_name} {suffix}\n")
            outfile.write(f"Gender: {gender}\n")

def main():
    name = input("Enter your name in English: ").strip()
    search_name_in_csvs(name)

if __name__ == "__main__":
    main()
