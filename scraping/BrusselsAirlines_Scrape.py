from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import json

# Instantiate the Chrome driver
driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://www.brusselsairlines.com/lhg/be/nl/o-d/cy-cy/brussel-malaga")

cookies = driver.find_element(By.ID, "cm-acceptAll").click()

doorgaan = driver.find_element(By.CLASS_NAME, "active-hidden").click()

oneway = driver.execute_script("document.getElementById('flightsOneWay').value='true';")
oneway1 = driver.execute_script("document.getElementById('flightsOneWay').checked='true';")

departure = driver.execute_script("document.getElementById('departureDate').value='01/04/2023';")

search = driver.find_element(By.ID, "searchFlights").click()

# WebDriverWait(driver, 25)
driver.implicitly_wait(45)

# WebDriverWait(driver, 70)
# time.sleep(70)

# TODO: de datum moet er nog bij

times = driver.find_elements(By.CLASS_NAME, "time")
stops = driver.find_elements(By.CLASS_NAME, "nbStops")
airports = driver.find_elements(By.CLASS_NAME, "airlineName")
durations = driver.find_elements(By.CLASS_NAME, "duration")
prices = driver.find_elements(By.CLASS_NAME, "cabinE")
prices.remove(prices[0])

flights = []

for i in range(len(times)):
    flight = []

    # Get time
    time_text = times[i].text
    flight.append(time_text)

    # Get stops
    stop_text = stops[i].text
    if stop_text.startswith("1"):
        stop_count = 1
        airport_text = airports[0].text + " - " + airports[1].text
        del airports[0:2]
    elif stop_text.startswith("2"):
        stop_count = 2
        airport_text = airports[0].text + " - " + airports[1].text + " - " + airports[2].text
        del airports[0:3]
    else:
        stop_count = 0
        airport_text = airports[0].text
        del airports[0]
    flight.append(stop_count)
    flight.append(airport_text)

    # Get duration
    duration_text = durations[i].text
    flight.append(duration_text)

    # Get price
    price_text = prices[i].text.split("\n")[0]
    flight.append(price_text)

    flight = {"Time": time_text, "Stops": stop_count, "Airports": airport_text, "Duration": duration_text, "Price": price_text}

    flights.append(flight)

print(flights)

# save the body to a json file
with open("BrusselsAirlines.json", "w") as file:
    json.dump(flights, file, indent=4)