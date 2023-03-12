import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
import time
import json
import csv
import pandas as pd
import glob

# Get the dates from april first 2023 to october first 2023
start_date = datetime.date(2023, 5, 1)
end_date = datetime.date(2023, 10, 1)
end_date = datetime.date(2023, 5, 3)
delta = datetime.timedelta(days=1)

dates = []
while start_date < end_date:
    dates.append(start_date.strftime('%d/%m/%Y'))
    start_date += delta


# Get the available destinations from Brussels
destinations = ["heraklion", "rhodes", "brindisi", "napels", "palermo", "faro", "alicante", "ibiza", "malaga", "palma-de-mallorca", "tenerife"]
destinations = ["heraklion"]


# Set the header for csv file
header = ["Departure", "Destination", "Date", "Departure time", "Arrival time", "Stops", "Flightnumber", "Airports", "Duration", "Price", "Seats"]

# driver.get("https://www.brusselsairlines.com/lhg/be/nl/o-d/cy-cy/brussel-malaga")

# flightsJSON = {}

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

desired_capabilities = DesiredCapabilities.CHROME.copy()
desired_capabilities['chromeOptions'] = {'args': ['--user-agent={}'.format(user_agent)]}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--user-agent")

# with open("csv/BrusselsAirlines.csv", mode="w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(header)

# Loop through the dates and destinations
for date in dates:
    for destination in destinations:
        # Instantiate the Chrome driver
        driver = webdriver.Chrome(options=chrome_options, desired_capabilities=desired_capabilities)
        driver.maximize_window()

        URL = "https://www.brusselsairlines.com/lhg/be/nl/o-d/cy-cy/brussel-" + destination

        driver.get(URL)

        # driver.implicitly_wait(10)

        cookies = driver.find_element(By.ID, "cm-acceptAll").click()

        time.sleep(2)

        doorgaan = driver.find_element(By.CLASS_NAME, "active-hidden").click()

        time.sleep(2)

        oneway = driver.execute_script("document.getElementById('flightsOneWay').value='true';")
        oneway1 = driver.execute_script("document.getElementById('flightsOneWay').checked='true';")

        time.sleep(2)

        departure = driver.execute_script("document.getElementById('departureDate').value='" + date + "';")

        time.sleep(2)

        search = driver.find_element(By.ID, "searchFlights").click()

        time.sleep(2)

        driver.find_element(By.ID, "searchFlights").click()

        driver.implicitly_wait(30)

        # flights = {}

        # Check if there are flights available
        noFlightsAvailable = driver.find_elements(By.ID, "warning-message-content-0")
        if noFlightsAvailable:
            # key = str(date)
            # value = "No flights available for " + destination + " on " + date
            # flight = {}
            # flights.update(key, flight)

            # filename = "json/BrusselsAirlines-" + destination + ".json"

            # with open(filename, "a") as file:
            #     if os.path.getsize(filename) > 0:
            #         file.seek(0, os.SEEK_END)
            #         file.seek(file.tell() - 1, os.SEEK_SET)
            #         file.write(",")
            #     json.dump(flights, file, indent=3)

            with open("csv/BrusselsAirlines.csv", mode="a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                # writer.writerow([departure, destination, date, departureTime, arrivalTime, stop_count, flightnumber_text, airportsArray, duration_text, price, seat])
                writer.writerow([departure, destination, date, None, None, None, None, None, None, None, None])
                
            driver.quit()
            continue

        # Check if there is a button to view more flights, if yes: click on it
        try:
            moreFlights = driver.find_element(By.CLASS_NAME, "more-flights-link-container")
            moreFlights.click()
        except:
            pass

        pres_avails = driver.find_elements(By.TAG_NAME, "pres-avail")
        counter = 0
        for pres_avail in pres_avails:
            # TODO: Get the unique flightkey
            departure = "brussel"
            times = pres_avail.find_element(By.CLASS_NAME, "time")
            stops = pres_avail.find_element(By.CLASS_NAME, "nbStops")
            airports = pres_avail.find_elements(By.CLASS_NAME, "airlineName")
            durations = pres_avail.find_element(By.CLASS_NAME, "duration")
            cabins = pres_avail.find_element(By.CLASS_NAME, "cabins")
            flightnumbers = pres_avail.find_elements(By.CLASS_NAME, "flightNumber")
            pres_avail_class_info = cabins.find_element(By.TAG_NAME, "pres-avail-class-info")

            try:
                # economies = pres_avail_class_info.find_element(By.CLASS_NAME, "cabinE")
                # prices = economies.__getattribute__("label")
                # economies.remove(economies[0])
                # economy = economies[counter]
                prices = pres_avail_class_info.find_element(By.CLASS_NAME, "cabinPrice")
                # prices = economies.find_element(By.TAG_NAME, "label")
                prices = prices.text.split(" ")
                price = float(prices[1].format().replace(",", "."))
            except:
                price = "No price available"
                # continue

            try:
                seats = pres_avail_class_info.find_element(By.CLASS_NAME, "seats")
                seat = seats.text
            except:
                seat = "No information available"

            # Get time
            time_text = times.text
            departureTime = time_text.split(" - ")[0]
            arrivalTime = time_text.split(" - ")[1]

            # Get stops
            stop_text = stops.text
            airportsArray = []
            if stop_text.startswith("1"):
                stop_count = 1
                # airport_text = airports[0].text + " - " + airports[1].text
                airportsArray.append(airports[0].text)
                airportsArray.append(airports[1].text)
                # del airports[0:2]
            elif stop_text.startswith("2"):
                stop_count = 2
                # airport_text = airports[0].text + " - " + airports[1].text + " - " + airports[2].text
                airportsArray.append(airports[0].text)
                airportsArray.append(airports[1].text)
                airportsArray.append(airports[2].text)
                # del airports[0:3]
            elif stop_text.startswith("3"):
                stop_count = 3
                airportsArray.append(airports[0].text)
                airportsArray.append(airports[1].text)
                airportsArray.append(airports[2].text)
                airportsArray.append(airports[3].text)
            else:
                stop_count = 0
                # airport_text = airports[0].text
                airportsArray.append(airports[0].text)
                # del airports[0]

            # Get duration
            duration_text = durations.text
            duration_string = duration_text.split("h ")
            duration_hours = int(duration_string[0])
            duration_minutes = int(duration_string[1].replace("min", ""))
            duration = duration_hours * 60 + duration_minutes

            # Get flight number
            flightnumberArray = []
            for flightnumber in flightnumbers:
                flightnumber_text = flightnumber.text
                flightnumberArray.append(flightnumber_text)

            # Create the flight object when the flight is done by Brussels Airlines itself
            if airportsArray.__contains__("Brussels Airlines") and len(airportsArray) > 0 and price != "No price available" :
                # flight = {"Departure": departure, "Destination": destination, "Date": date, "Departure time": departureTime, "Arrival time": arrivalTime, "Stops": stop_count, "FlightNumber": flightnumberArray, "Airports": airportsArray, "Duration": duration, "Price": price, "Seats": seat}

                # key = str(str(counter) + ")" + " " + date)

                # flights.__setitem__(counter, flight)

                filename = "csv/BrusselsAirlines-" + destination + ".csv"
                filename = "csv/BrusselsAirlines.csv"

                with open(filename, mode="a", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([departure, destination, date, departureTime, arrivalTime, stop_count, flightnumberArray, airportsArray, duration, price, seat])

                counter += 1

        # filename = "json/BrusselsAirlines-" + destination + ".json"
        # key = destination + " " + date
        # flightsJSON.__setitem__(date, flights)

        # with open(filename, "a") as file:
        #     if os.path.getsize(filename) > 0:
        #         file.seek(0, os.SEEK_END)
        #         file.seek(file.tell() - 1, os.SEEK_SET)
        #         file.write(",")
        #     json.dump(flightsJSON, file, indent=3)

        driver.quit()

# flightsOVERALL = {}
# flightsOVERALL.update(flightsJSON)

# with open("json/BrusselsAirlines.json", "w") as jsonfile:
#     # if os.path.getsize(filename) > 0:
#     #     file.seek(0, os.SEEK_END)
#     #     file.seek(file.tell() - 1, os.SEEK_SET)
#     #     file.write(",")
#     json.dump(flightsJSON, jsonfile, indent=3)


# csv_files = glob.glob('*.{}'.format('csv'))
# df_csv_append = pd.DataFrame()

# for file in csv_files:
#     df = pd.read_csv(file)
#     df_csv_append = df_csv_append.append(df, ignore_index=True)

# df_csv_append.drop_duplicates(subset=None, inplace=True)
# df_csv_append.to_csv('csv/BrusselsAirlines.csv', index=False)



df = pd.read_csv("csv/BrusselsAirlines.csv")
df.drop_duplicates(subset=None, inplace=True)
df.to_csv("csv/BrusselsAirlines.csv", index=False)



