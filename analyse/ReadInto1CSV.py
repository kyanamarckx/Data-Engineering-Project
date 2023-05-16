import os

directory = "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads"
newName = "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\COMBINED.csv"

with open(os.path.join(directory, newName), 'w') as combined_file:
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            csv_file_path = os.path.join(directory, filename)
            with open(csv_file_path, "r") as csv_file:
                # Write the contents of the CSV file to the combined file
                combined_file.write(csv_file.read())
                combined_file.write('\n')

# open the new file and delete empty lines if there are any, drop duplicates too
with open(newName, 'r') as file:
    lines = file.readlines()
    lines = filter(lambda x: x.strip(), lines)
    lines = list(dict.fromkeys(lines))
    
with open(newName, 'w') as file:
    file.writelines(lines)