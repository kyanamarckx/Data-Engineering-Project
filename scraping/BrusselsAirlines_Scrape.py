from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
import time
import csv
import pandas as pd

# Get the dates from april first 2023 to october first 2023
start_date = datetime.date(2023, 5, 26)
end_date = datetime.date(2023, 10, 1)
end_date = datetime.date(2023, 6, 1)
delta = datetime.timedelta(days=1)

dates = []
while start_date < end_date:
    dates.append(start_date.strftime('%d/%m/%Y'))
    start_date += delta


# Get the available destinations from Brussels
destinations = ["heraklion", "rhodes", "brindisi", "napels", "palermo", "faro", "alicante", "ibiza", "malaga", "palma-de-mallorca", "tenerife", "corfu"]
# destinations = ["alicante", "ibiza", "malaga", "palma-de-mallorca", "tenerife", "corfu"]
# destinations = ["faro"]

# Set the header for csv file
header = ["Departure", "Destination", "Date", "Departure time", "Arrival time", "Stops", "Flightnumber", "Airports", "Duration", "Price"]
filename = "csv/BrusselsAirlines.csv"

# driver.get("https://www.brusselsairlines.com/lhg/be/nl/o-d/cy-cy/brussel-malaga")

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

# Set the desired capabalities for Chrome
desired_capabilities = DesiredCapabilities.CHROME.copy()
desired_capabilities['chrome.switches'] = ['--disable-gpu']

# Set the options for Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--enable-stealth-mode")

# Set the driver
driver = webdriver.Chrome(desired_capabilities=desired_capabilities, options=chrome_options)
driver.maximize_window()

# Instantiate stealth
stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

# Write the header to csv file
# with open(filename, mode="w", newline="", encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(header)

# Loop through the dates and destinations
for date in dates:
    for destination in destinations:
        if destination == "corfu":
            with open(filename, mode="a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([departure, destination, date, "None", "None", "None", "None", "None", "None", "None"])
                continue

        URL = "https://www.brusselsairlines.com/lhg/be/nl/o-d/cy-cy/brussel-" + destination

        driver.get(URL)

        time.sleep(2)

        # Search for cookies and accept them
        try:
            cookies = driver.find_element(By.ID, "cm-acceptAll").click()
        except:
            pass

        time.sleep(2)

        # Search for doorgaan and click it to open whole menu
        try:
            doorgaan = driver.find_element(By.CLASS_NAME, "active-hidden").click()
        except:
            pass
        try:
            doorgaan = driver.find_element(By.ID, "consentOverlay").click()
        except:
            pass

        time.sleep(2)

        # Select single flight
        oneway = driver.execute_script("document.getElementById('flightsOneWay').value='true';")
        oneway1 = driver.execute_script("document.getElementById('flightsOneWay').checked='true';")

        # Select the departure date
        departure = driver.execute_script("document.getElementById('departureDate').value='" + date + "';")
        
        time.sleep(2)

        # Click search
        try:
            search = driver.find_element(By.ID, "searchFlights").click()
        except:
            pass
        try:
            search = driver.find_element(By.CLASS_NAME, "search-button-wrapper")
            searchbtn = search.find_element(By.TAG_NAME, "button").click()
        except:
            pass

        # Wait for the page to load
        driver.implicitly_wait(30)

        departure = "brussel"

        try:
            # Check if there are flights available
            noFlightsAvailable = driver.find_elements(By.TAG_NAME, "refx-no-flights-found-pres")
            if noFlightsAvailable:
                with open(filename, mode="a", newline="", encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([departure, destination, date, "None", "None", "None", "None", "None", "None", "None"])
                continue
        except:
            pass

        # Scroll down to load all flights
        for i in range(7):
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)

        WebDriverWait(driver, 600).until(EC.presence_of_all_elements_located((By.TAG_NAME, "refx-upsell-premium-row-pres")))

        # Get the rows of all the flights
        rows = driver.find_elements(By.TAG_NAME, "refx-upsell-premium-row-pres")
        counter = 0
        for row in rows:
            counter += 1

            # Get all the airports
            airports = row.find_elements(By.CLASS_NAME, "operating-airline-name")

            # Get the number of stops
            try:
                stops = row.find_element(By.CLASS_NAME, "bound-nb-stop")
                stop = stops.find_element(By.TAG_NAME, "span").text
                stop = int(stop)
            except:
                stop = 0

            # Set the airports in an array
            airportsArray = []
            for airport in airports[0:stop+1]:
                airportsArray.append(airport.text)

            #  Check if Brussels Airlines is in the array
            if not airportsArray.__contains__("Brussels Airlines"):
                continue

            #  Get economy cabin
            flightCardButtonSection = row.find_element(By.CLASS_NAME, "flight-card-button-section")
            economyClassCabin = flightCardButtonSection.find_element(By.TAG_NAME, "div")

            # Check if the flight is available in economy class
            try:
                notAvailable = economyClassCabin.find_element(By.CLASS_NAME, "not-available-card")
                if notAvailable:
                    continue
            except:
                pass

            departuretime = row.find_element(By.CLASS_NAME, "bound-departure-datetime").text
            arrivaltime = row.find_element(By.CLASS_NAME, "bound-arrival-datetime").text

            details = row.find_element(By.TAG_NAME, "refx-flight-details")
            duration = details.find_element(By.CLASS_NAME, "duration-value").text

            try:
                economy = row.find_element(By.CLASS_NAME, "eco")
                price = economy.find_element(By.CLASS_NAME, "price-amount").text
                if price.__contains__("."):
                    price = price.replace(".", "")
                price = float(price.format().replace(",", "."))
            except:
                pass

            try:
                price = row.find_element(By.CLASS_NAME, "price-amount").text
                if price.__contains__("."):
                    price = price.replace(".", "")
                price = float(price.format().replace(",", "."))
            except:
                continue

            try:
                moreInfo = row.find_element(By.CLASS_NAME, "itin-details-link").click()
            except:
                pass
            try:
                moreInfo = row.find_element(By.CLASS_NAME, "flight-recap").click()
            except:
                pass

            container = driver.find_element(By.TAG_NAME, "mat-dialog-container")
            scroll = container.find_element(By.CLASS_NAME, "refx-dialog-content")

            for i in range(4):
                scroll.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)

            WebDriverWait(driver, 600).until(EC.presence_of_all_elements_located((By.TAG_NAME, "refx-segment-details-pres")))

            flightnumbers = container.find_elements(By.CLASS_NAME, "seg-marketing-flight-number")
            
            # Get flight number
            flightnumberArray = []
            for flightnumber in flightnumbers:
                flightnumberValue = flightnumber.find_element(By.TAG_NAME, "b").text
                flightnumberArray.append(flightnumberValue)

            closeMoreInfo = container.find_element(By.CLASS_NAME, "close-btn-bottom").click()

            # Get duration in minutes as Integer
            duration_string = duration.split("h ")
            duration_hours = int(duration_string[0])
            duration_minutes = int(duration_string[1].replace("m", ""))
            duration = duration_hours * 60 + duration_minutes

            # Write the flight to csv when the flight is done by Brussels Airlines itself
            if len(airportsArray) > 0:
                with open(filename, mode="a", newline="", encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([departure, destination, date, departuretime, arrivaltime, stop, flightnumberArray, airportsArray, duration, price])
            
        found = False
        with open(filename, mode="r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] == destination and row[2] == date:
                    found = True
                    break

        if not found:
            with open(filename, mode="a", newline="", encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([departure, destination, date, "None", "None", "None", "None", "None", "None", "None"])

driver.quit()

# Remove duplicates
df = pd.read_csv(filename)
df.drop_duplicates(subset=None, inplace=True)
df.to_csv(filename, index=False)
