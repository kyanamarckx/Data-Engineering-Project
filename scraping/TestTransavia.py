import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
import json
import csv


start_date = datetime.date(2023, 4, 1)
# end_date = datetime.date(2023, 10, 1)
end_date = datetime.date(2023, 4, 2)
delta = datetime.timedelta(days=1)

dates = []

while start_date < end_date:
    dates.append(start_date.strftime("%#d %B %Y").lower())
    start_date += delta

print(dates)

destinations = ['CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'AGP', 'SPC', 'TFS']
destinations = ['Corfu, Griekenland', 'Kreta (Heraklion), Griekenland', 'Rhodos, Griekenland', 'Brindisi, Italië', 'Napels, Italië', 'Sicilië (Palermo), Italië',
                'Faro, Portugal', 'Alicante, Spanje', 'Ibiza, Spanje', 'Malaga, Spanje', 'Tenerife (Zuid), Spanje']
destinations = ['Corfu, Griekenland', 'Kreta (Heraklion), Griekenland']
destinations = ['Kreta (Heraklion), Griekenland']

def switchDestination(destination):
   match destination:
      case 'Corfu, Griekenland':
          return 'Corfu'
      case 'Kreta (Heraklion), Griekenland':
          return 'Kreta'
      case 'Rhodos, Griekenland':
          return 'Rhodos'
      case 'Brindisi, Italië':
          return 'Brindisi'
      case 'Napels, Italië':
          return 'Napels'
      case 'Sicilië (Palermo), Italië':
          return 'Palermo'
      case 'Faro, Portugal':
          return 'Faro'
      case 'Alicante, Spanje':
          return 'Alicante'
      case 'Ibiza, Spanje':
          return 'Ibiza'
      case 'Malaga, Spanje':
          return 'Malaga'
      case 'Tenerife (Zuid), Spanje':
          return 'Tenerife'
       

# destinations = ['CFU']

with open("csv/Transavia.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Date", "Departure", "Destination", "Departure time", "Arrival time", "Duration", "Price"])


for date in dates:
    for destination in destinations:
        # Instantiate the Chrome driver
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # chrome_options.add_argument("--incognito")
        chrome_options.add_extension("./extension/buster.crx")
        chrome_options.add_extension("./extension/nopecha.crx")
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()

        destinationString = switchDestination(destination)

        time.sleep(6)

        URL = "https://www.transavia.com/nl-BE/boek-een-vlucht/vluchten/zoeken/"
        # URL = "https://www.transavia.com/nl-BE/boek-een-vlucht/uitgebreid-zoeken/zoeken/"

        driver.get(URL)

        time.sleep(7)

        driver.implicitly_wait(5)

        try:
          cookies = driver.find_element(By.CLASS_NAME, "cb__button--accept-all").click()
        except:
          pass

        time.sleep(5)
        driver.implicitly_wait(5)

        wait = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.CLASS_NAME, "panel_section--secondary")))

        # departureAirport = driver.execute_script("document.getElementById('countryStationSelection_Origin-input').value='Brussel, België'")
        # departureAirport = driver.find_element(By.ID, "countryStationSelection_Origin-input").send_keys("Brussel, België")
        time.sleep(5)

        departureAirport = driver.execute_script("document.getElementById('routeSelection_DepartureStation-input').value='Brussel, België'")

        arrivalAirport = driver.execute_script("document.getElementById('routeSelection_ArrivalStation-input').value='" + destination + "'")

        oneway = driver.execute_script("document.getElementById('dateSelection_IsReturnFlight').removeAttribute('checked');")

        # inbounddate = driver.find_element(By.ID, "dateSelection_OutboundDate-datepicker").clear()
        # inbounddateClear = driver.execute_script("document.getElementById('dateSelection_OutboundDate-datepicker').value='" + date + "';")
        datepickerbtn = driver.find_element(By.CLASS_NAME, "datepicker-trigger").click()
        datepicker = driver.find_element(By.ID, "ui-datepicker-div")
        
        month = datepicker.find_element(By.CLASS_NAME, "ui-datepicker-month").text
        year = datepicker.find_element(By.CLASS_NAME, "ui-datepicker-year").text

        while month != date.split(" ")[1]:
            next = datepicker.find_element(By.CLASS_NAME, "ui-datepicker-next").click()

        days = datepicker.find_elements(By.CLASS_NAME, "ui-state-default")
        for day in days:
            if day.text == date.split(" ")[0]:
                day.click()
                break

        time.sleep(10)

        # # arrivalAirport = driver.execute_script("document.getElementById('countryStationSelection_Destination-input').value='" + destination + "'")
        # arrivalAirport = driver.find_element(By.ID, "countryStationSelection_Destination-input").send_keys(destination)
        # time.sleep(5)

        # titles = driver.find_elements(By.CLASS_NAME, "h5")
        # departureTitle = titles[2]
        # departureTitle.find_element(By.XPATH, "..")
        # departureTitle.click()
        # time.sleep(5)

        # specificDate = driver.execute_script("document.getElementById('data-type-data').checked='checked';")
        # specificDate1 = driver.execute_script("document.getElementById('data-type-data').click();")
        # time.sleep(5)

        # selectList = driver.find_element(By.ID, "data-flight-type")
        # allOptions = selectList.find_elements(By.TAG_NAME, "option")
        # for option in allOptions:
        #     if option.get_attribute("value") == "Single":
        #         option.click()
        #         break
            
        # time.sleep(5)
            
        # departureDate = driver.execute_script("document.getElementById('timeFrameSelection_SingleFlight_OutboundDate-datepicker').value='" + date + "';")
        # time.sleep(5)

        # search = driver.find_element(By.CLASS_NAME, "button-primary").click()
        # time.sleep(5)

        # try:
        #   wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "notification-message")))
        #   notification = driver.find_element(By.CLASS_NAME, "notification-message")

        #   if notification.text == "We hebben helaas geen vluchten gevonden. Probeer het nog eens":
        #     with open("csv/Transavia.csv", "a", newline="") as csvfile:
        #       writer = csv.writer(csvfile)
        #       writer.writerow([date, "Brussel", destinationString, "None", "None", "None", "None"])
        #     driver.quit()
        #     continue
        # except:
        #   pass

        # time.sleep(5)

        # try:
        #   showResults = driver.find_element(By.CLASS_NAME, "button-open").click()
        #   time.sleep(5)

        #   details = driver.find_element(By.CLASS_NAME, "toggle-button-level-2").click()
        #   time.sleep(2)

        #   times = driver.find_element(By.CLASS_NAME, "HV-gu--bp20--x2-2").text
        #   departureTime = times.split(" - ")[0]
        #   arrivalTime = times.split(" - ")[1]
        #   t1 = datetime.datetime.strptime(departureTime, "%H:%M")
        #   t2 = datetime.datetime.strptime(arrivalTime, "%H:%M")
        #   duration = t2 - t1
        #   duration = duration.seconds / 60
        #   time.sleep(5)

        #   priceDiv = driver.find_element(By.CLASS_NAME, "HV-gu--bp22--x1-2")
        #   price = priceDiv.find_element(By.CLASS_NAME, "integer").text
        #   price = float(price)
        #   price = price.replace(",", ".")

        #   with open("csv/Transavia.csv", "a", newline="") as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow([date, "Brussel", destinationString, departureTime, arrivalTime, duration, price])

        # except:
        #   with open("csv/Transavia.csv", "a", newline="") as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow([date, "Brussel", destinationString, "None", "None", "None", "None"])
        #   driver.quit()
        #   continue

        # time.sleep(25)

        # driver.quit()
      


