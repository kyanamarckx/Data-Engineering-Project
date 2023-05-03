import csv
import os

# this function will create a header in the csv files if it doesn't exist yet
# you do not have to edit this function or paths
def makeHeader():
    destination_folder = 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads'
    header = 'flight_id,flightnumber,departure_date,arrival_date,departure_time,arrival_time,duration,number_of_stops,airline_iata_code,departure_airport_iata_code,arrival_airport_iata_code,scrape_date,available_seats,price'
    returnedHeader = ['flight_id', 'flightnumber', 'departure_date', 'arrival_date', 'departure_time', 'arrival_time', 'duration', 'number_of_stops', 'airline_iata_code', 'departure_airport_iata_code', 'arrival_airport_iata_code', 'scrape_date', 'available_seats', 'price']

    for file in os.listdir(destination_folder):
        if file.startswith('All') and file.endswith('.csv'):
            destination_file = os.path.join(destination_folder, file)

            with open(destination_file, 'r') as csv_file:
                reader = csv.reader(csv_file)
                rows = list(reader)

                if len(rows) > 0 and rows[0] == returnedHeader:
                    print('Header already exists in ' + file + ', skipping...')
                else:
                    with open(destination_file, 'w', newline='') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(header.split(','))
                        print('Header created in ' + file)
                        writer.writerows(rows)

makeHeader()