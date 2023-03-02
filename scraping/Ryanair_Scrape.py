import requests
from bs4 import BeautifulSoup
import json
import datetime

start_date = datetime.date(2023, 4, 1)
end_date = datetime.date(2023, 10, 1)
delta = datetime.timedelta(days=1)

all_destinations = ['CFU', 'HER', 'RHO', 'BDS', 'NAP',
                    'PMO', 'FAO', 'ALC', 'IBZ', 'AGP', 'SPC', 'TFS']
all_airports = ['BRU', 'CRL']
all_dates = []

current_date = start_date

while current_date < end_date:
    all_dates.append(current_date.strftime("%Y-%m-%d"))
    current_date += delta

for dateIn in all_dates:
    for dateOut in all_dates:
        for destination in all_destinations:
            for airport in all_airports:
                url = f"https://www.ryanair.com/api/booking/v4/nl-nl/availability?ADT=1&CHD=0&DateIn={dateIn}&DateOut={dateOut}&Destination={destination}&Disc=0&INF=0&Origin={airport}&TEEN=0&promoCode=&IncludeConnectingFlights=false&FlexDaysBeforeOut=2&FlexDaysOut=2&FlexDaysBeforeIn=2&FlexDaysIn=2&RoundTrip=true&ToUs=AGREED"
                page = requests.get(url)
                soup = BeautifulSoup(page.content, "lxml")
                result = soup.find("p").text
                json_object = json.loads(result)
                # x = 0 tot lengte array
                # ["trips"][0]["dates"]["x"]["flights"]["flightkey"]
                print(json_object["trips"][0]["destinationName"] + " - " + json_object["trips"][0]["originName"])

