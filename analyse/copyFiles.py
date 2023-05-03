import shutil
import os

# with this function you can automatically copy the files from your source folder (you'll have to edit this one with your own directory) to the destination folder (this one always stays the same for everyone, DO NOT edit this)
# this function will only copy the 'All' csv files
# it also checks if the file already exists in the destination folder. If it does, it will skip the file
def copyFiles():
    source_folder = 'C:\\Users\\kyana\\OneDrive - Hogeschool Gent\\AirFares'
    destination_folder = 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads'

    for file in os.listdir(source_folder):
        if file.startswith('All') and file.endswith('.csv'):
            source_file = os.path.join(source_folder, file)
            destination_file = os.path.join(destination_folder, file)

            if os.path.exists(destination_file):
                print(destination_file + ' already exists, skipping...')
            else:
                shutil.copy(source_file, destination_file)
                print('Copied ' + source_file + ' to ' + destination_folder)

copyFiles()