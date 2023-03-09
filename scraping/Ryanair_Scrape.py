import requests
from bs4 import BeautifulSoup
import json
import datetime
import csv

start_date = datetime.date(2023, 4, 1)
end_date = datetime.date(2023, 10, 1)
delta = datetime.timedelta(days=1)

all_destinations = ['CFU', 'HER', 'RHO', 'BDS', 'NAP',
                    'PMO', 'FAO', 'ALC', 'IBZ', 'AGP', 'SPC', 'TFS']
all_airports = ['BRU', 'CRL']
all_dates = []

bestandsnaam = "ryanair.csv"
veldnamen = ["Luchthaven", "Bestemming", "Vertrektijdstip", "Aankomsttijdstip","prijs","duur","aantalStops","vrijePlaatsen", "VluchtNr","Flightkey"]

current_date = start_date

while current_date < end_date:
    all_dates.append(current_date.strftime("%Y-%m-%d"))
    current_date += delta

for dateOut in all_dates:
    for destination in all_destinations:
        for airport in all_airports:
            url = f"https://www.ryanair.com/api/booking/v4/nl-nl/availability?ADT=1&DateOut={dateOut}&dateIn=&Destination={destination}&Disc=0&INF=0&Origin={airport}&TEEN=0&promoCode=&IncludeConnectingFlights=false&RoundTrip=true&ToUs=AGREED"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "lxml")
            result = soup.find("p").text
            json_object = json.loads(result)
            if 'trips' in json_object and isinstance(json_object['trips'], list):
                for trip in json_object['trips']:
                    if 'dates' in trip and isinstance(trip['dates'], list):
                        for date in trip['dates']:
                            if 'flights' in date and isinstance(date['flights'], list):
                                for flight in date['flights']:
                                    if 'flightKey' in flight:
                                        luchthaven = trip['originName'] 
                                        bestemming = trip['destinationName']
                                        vertrektijdstip = flight['time'][0]
                                        aankomsttijdstip = flight['time'][1]
                                        duur = flight['duration']
                                        aantal_stops = flight['segments'][0]['segmentNr']
                                        prijs = flight['regularFare']['fares'][0]['amount']
                                        vrije_plaatsen = flight['faresLeft']
                                        vluchtnummer = flight['flightNumber']
                                        flightkey = flight['flightKey']
                                        with open(bestandsnaam, mode="a", newline="") as csvfile:
                                            writer = csv.writer(csvfile)
                                            writer.writerow([luchthaven, bestemming, vertrektijdstip, aankomsttijdstip, prijs, duur, aantal_stops,vrije_plaatsen, vluchtnummer,flightkey])
                                        break
                                else:
                                    continue
                                break
                        else:
                            continue
                        break

