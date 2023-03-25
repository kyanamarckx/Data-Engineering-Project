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
import csv

PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

url = "http://www.tuifly.be/flight/nl/"
url2 = "http://www.tuifly.be/flight/nl/search?flyingFrom%5B%5D=BRU&flyingTo%5B%5D={0}&depDate={1}&adults=1&children=0&childAge=&choiceSearch=true&searchType=pricegrid&nearByAirports=true&currency=EUR&isOneWay=true"

departureAirports = {'Brussel', 'Antwerpen', 'Luik', 'Brugge-Oostende'}
arrivalAirports = ['CFU', 'ALC', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'AGP', 'SPC', 'TFS', 'IBZ']

dates = pd.date_range(start='2023-04-04', end='2023-10-03', freq='7D')
datesPerDay = pd.date_range(start='2023-04-01', end='2023-10-01', freq='1D')

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--ignore-certificate-errors')
driver_service = Service(executable_path=PATH)


arrayWithAllDates = [datum.strftime('%Y-%m-%d') for datum in dates]
arrayWithAllDatesPerDay = [datum.strftime('%Y-%m-%d') for datum in datesPerDay]

headersCsv = ["datumVanVertrek", "vertrekLuchthaven", "aankomstLuchthaven", "vertrekTijd", "aankomstTijd", "prijs", "duur", "vrijeZitplaatsen", "vluchtNummer", "aantalStops"]
with open('csv/tui.csv', mode='a', newline="") as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(headersCsv)

i = 0

for arriAirport in arrivalAirports:
    for date in arrayWithAllDates:

        print('------DEBUG------')
        print(url2.format(arriAirport, date))
        print("BRU", arriAirport)
        print(date)
        print('-----------------')
        
        correctURL = url2.format(arriAirport, date)

        try:
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(25)
            driver.get(url)
            driver.find_element(By.CSS_SELECTOR, "#cmCloseBanner").click()
            element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#page div.container footer > script")))
            driver.get(correctURL)
            data = driver.execute_script("return JSON.stringify(searchResultsJson)")
            json_object = json.loads(data)

            alleVluchtenList = json_object['flightViewData'] # alle vluchten die beschikbaar zijn in een bepaalde week
            weekMetOutboundDataList = json_object['dateAvailabilityData']['outboundAvailabilityData'] # elke dag van de week met data in of dat een vlucht beschikbaar is of niet

            while i < len(weekMetOutboundDataList):
                datumInWeek = weekMetOutboundDataList[i]['displayDate']
                if weekMetOutboundDataList[i]['available'] == True:
                    j = 0
                    alleVertrekLuchthaven = [] # lege lijst waar alle luchthavens inkomen van die dag inkomen
                    aantalVluchtenVoorEenDatum = 0
                    while j < len(alleVluchtenList):
                        if datumInWeek == alleVluchtenList[j]['departureDate']: # alle vluchten van de dag met datum: datumInWeek

                            datumVanVertrek = alleVluchtenList[j]['departureDate']
                            vertrekLuchthaven = alleVluchtenList[j]['journeySummary']['departAirportName']
                            aankomstLuchthaven = alleVluchtenList[j]['journeySummary']['arrivalAirportName']
                            vertrekTijd = alleVluchtenList[j]['journeySummary']['depTime']
                            aankomstTijd = alleVluchtenList[j]['journeySummary']['arrivalTime']
                            prijs = alleVluchtenList[j]['totalPrice']
                            duur = alleVluchtenList[j]['journeySummary']['journeyDuration']
                            vrijeZitplaatsen = alleVluchtenList[j]['journeySummary']['availableSeats']
                            vluchtNummer = alleVluchtenList[j]['flightsectors'][0]['flightNumber']
                            aantalStops = len(alleVluchtenList[j]['flightsectors']) - 1

                            alleVertrekLuchthaven.append(vertrekLuchthaven)

                            with open('csv/tui.csv', mode='a', newline="") as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerow([datumVanVertrek, vertrekLuchthaven, aankomstLuchthaven, vertrekTijd, aankomstTijd, prijs, duur, vrijeZitplaatsen, vluchtNummer, aantalStops])
                        j += 1
                    # print(f'alle vertrek luchthavens met datum: ' + datumInWeek + ' list:', set(alleVertrekLuchthaven))
                    overblijfendeLuchthavens = departureAirports.symmetric_difference(set(alleVertrekLuchthaven))
                    if len(overblijfendeLuchthavens) != 0:
                        for luchthaven in overblijfendeLuchthavens:
                            datumVanVertrek = datumInWeek
                            vertrekLuchthaven = luchthaven
                            aankomstLuchthaven = json_object['arrAirportData'][0]['name']
                            vertrekTijd = "geen"
                            aankomstTijd = "geen"
                            prijs = "geen"
                            duur = "geen"
                            vrijeZitplaatsen = "geen"
                            vluchtNummer = "geen"
                            aantalStops = "geen"
                            with open('csv/tui.csv', mode='a', newline="") as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerow([datumVanVertrek, vertrekLuchthaven, aankomstLuchthaven, vertrekTijd, aankomstTijd, prijs, duur, vrijeZitplaatsen, vluchtNummer, aantalStops])
                else:

                    alleVertrekLuchthaven2 = []

                    datumVanVertrek = datumInWeek
                    vertrekLuchthaven = json_object['depAirportData'][0]['name']
                    aankomstLuchthaven = json_object['arrAirportData'][0]['name']
                    vertrekTijd = "geen"
                    aankomstTijd = "geen"
                    prijs = "geen"
                    duur = "geen"
                    vrijeZitplaatsen = "geen"
                    vluchtNummer = "geen"
                    aantalStops = "geen"

                    alleVertrekLuchthaven2.append(vertrekLuchthaven)

                    with open('csv/tui.csv', mode='a', newline="") as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow([datumVanVertrek, vertrekLuchthaven, aankomstLuchthaven, vertrekTijd, aankomstTijd, prijs, duur, vrijeZitplaatsen, vluchtNummer, aantalStops])

                    overblijfendeLuchthavens = departureAirports.symmetric_difference(set(alleVertrekLuchthaven2))
                    if len(overblijfendeLuchthavens) != 0:
                        for luchthaven in overblijfendeLuchthavens:
                            datumVanVertrek = datumInWeek
                            vertrekLuchthaven = luchthaven
                            aankomstLuchthaven = json_object['arrAirportData'][0]['name']
                            vertrekTijd = "geen"
                            aankomstTijd = "geen"
                            prijs = "geen"
                            duur = "geen"
                            vrijeZitplaatsen = "geen"
                            vluchtNummer = "geen"
                            aantalStops = "geen"
                            with open('csv/tui.csv', mode='a', newline="") as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerow([datumVanVertrek, vertrekLuchthaven, aankomstLuchthaven, vertrekTijd, aankomstTijd, prijs, duur, vrijeZitplaatsen, vluchtNummer, aantalStops])
                i += 1
            i = 0
            driver.close()
        except Exception as e:
            print(e)