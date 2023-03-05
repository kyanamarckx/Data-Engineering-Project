from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json

PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

url = "http://www.tuifly.be/flight/nl/"
url2 = "http://www.tuifly.be/flight/nl/search?flyingFrom%5B%5D={0}&flyingTo%5B%5D={1}&depDate={2}&adults=1&children=0&childAge=&choiceSearch=true&searchType=pricegrid&nearByAirports=true&currency=EUR&isOneWay=true"

departureAirports = ['ANR', 'OST', 'LGG', 'BRU']
arrivalAirports = ['CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'AGP', 'SPC', 'TFS']
arrivalAirportsTest = ['CFU', 'HER', 'RHO', 'BDS'] # voor te testen

# DATES FOR URL
# if we scrape data from tui we get the data of whole week, so if we need to start from the first of april
# we have to use april 4th instead of april 1st.
arrayWithAllDates = []
dates = pd.date_range(start='2023-04-04', end='2023-10-03', freq='7D') # gaat maar tot 29 sept dus 2023-09-30 en 2023-10-01 moeten er nog bij

alleVluchten = []

for datum in dates:
    dateStr = str(datum)
    array = dateStr.split()
    arrayWithAllDates.append(array[0])

for depAirport in departureAirports:
    for arriAirport in arrivalAirportsTest:
        for date in arrayWithAllDates:

            print('------DEBUG------')
            print(url2.format(depAirport, arriAirport, date))
            print(depAirport, arriAirport)
            print(date)
            print('-------------')

            try:
                options = webdriver.ChromeOptions()
                options.add_experimental_option("detach", True)
                options.add_argument('--ignore-certificate-errors')
                driver_service = Service(executable_path=PATH)
                driver = webdriver.Chrome(service=driver_service,options=options)
                driver.maximize_window()
                driver.implicitly_wait(25)
                driver.get(url)
                driver.find_element(By.CSS_SELECTOR, "#cmCloseBanner").click()
                element = WebDriverWait(driver, 50).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div#page div.container footer > script"))
                    ) 
                driver.get(url2.format(depAirport, arriAirport, date))
                data = driver.execute_script("return JSON.stringify(searchResultsJson)")
                json_object = json.loads(data)

                lengteFlightViewDataArray = len(json_object['flightViewData']) - 1

                while lengteFlightViewDataArray != -1:

                    lengteFlightViewDataFlightsectorsArray = len(json_object['flightViewData'][lengteFlightViewDataArray]['flightsectors']) - 1
                    aantalStopsLengte = len(json_object['flightViewData'][lengteFlightViewDataArray]['flightsectors']) - 1

                    array = json_object['flightViewData'][lengteFlightViewDataArray]['journeySummary']
                    
                    vertrekDatum = array['departDate']
                    vertrek = array['departAirportName']
                    aankomst = array['arrivalAirportName']
                    vertrekTijd = array['depTime']
                    aankomstTijd = array['arrivalTime']
                    prijs = json_object['flightViewData'][lengteFlightViewDataArray]['perPersonPrice']
                    duur = array['totalJnrDuration']
                    vrijeZitplaatsen = array['availableSeats']
                    journeyType = array['journeyType']

                    while lengteFlightViewDataFlightsectorsArray != -1:
                        vluchtnummer = json_object['flightViewData'][lengteFlightViewDataArray]['flightsectors'][lengteFlightViewDataFlightsectorsArray]['flightNumber']

                        vlucht = {
                            'vertrekDatum': vertrekDatum,
                            'vertrekPlaats': vertrek,
                            'aankomstPlaats': aankomst,
                            'vertrekTijd': vertrekTijd,
                            'aankomstTijd': aankomstTijd,
                            'prijs': prijs,
                            'duur': duur,
                            'vrijeZitplaatsen': vrijeZitplaatsen,
                            'vluchtnummer': vluchtnummer,
                            'aantalStops': aantalStopsLengte
                        }

                        lengteFlightViewDataFlightsectorsArray = lengteFlightViewDataFlightsectorsArray - 1

                    alleVluchten.append(vlucht)

                    with open("jsonData/tuiScrapeJsonData.json", "w") as file:
                        json.dump(alleVluchten, file, indent=4)

                    lengteFlightViewDataArray = lengteFlightViewDataArray - 1
                driver.close()

            except NoSuchElementException as e:
                print(e)