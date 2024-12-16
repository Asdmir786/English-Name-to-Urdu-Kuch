import os
import csv

def search_name_in_csvs(name, base_dir='Output', output_file='output.txt'):
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
                                outfile.write(f"{row[0]}: {row[1]}\n")
                                return
        outfile.write(f"Name: {name} not found in any CSV file.\n")

def main():
    name = input("Enter your name in English: ").strip()
    search_name_in_csvs(name)

if __name__ == "__main__":
    main()
