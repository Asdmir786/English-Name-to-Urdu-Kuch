import os
import csv

def search_name_in_csvs(name, base_dir='Output', output_file='output.txt'):
    found_in = set()  # To track which subdirectories the name is found in
    written_names = set()  # To track names already written to the output file

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
                                if row[0] not in written_names:
                                    outfile.write(f"{row[0]}: {row[1]}\n")
                                    written_names.add(row[0])
        
        if not found_in:
            outfile.write(f"Name: {name} not found in any CSV file.\n")
        else:
            # Determine gender based on subdirectory names
            if 'Boys' in found_in and 'Girls' in found_in:
                gender = "both genders"
            elif 'Boys' in found_in:
                gender = "male"
            elif 'Girls' in found_in:
                gender = "female"
            else:
                gender = "unknown"
            outfile.write(f"Gender: {gender}\n")

def main():
    name = input("Enter your name in English: ").strip()
    search_name_in_csvs(name)

if __name__ == "__main__":
    main()
