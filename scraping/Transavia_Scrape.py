import http.client, urllib.request, urllib.parse, urllib.error, base64
import datetime
import json
import csv
import pandas as pd

start_date = datetime.date(2023, 4, 1)
end_date = datetime.date(2023, 10, 1)
delta = datetime.timedelta(days=1)

dates = []
while start_date < end_date:
    dates.append(start_date.strftime('%Y%m%d'))
    start_date += delta

destinations = ['CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'AGP', 'TFS']

def switchDestination(destination):
   match destination:
      case 'CFU':
          return 'Corfu'
      case 'HER':
          return 'Kreta'
      case 'RHO':
          return 'Rhodos'
      case 'BDS':
          return 'Brindisi'
      case 'NAP':
          return 'Napels'
      case 'PMO':
          return 'Palermo'
      case 'FAO':
          return 'Faro'
      case 'ALC':
          return 'Alicante'
      case 'IBZ':
          return 'Ibiza'
      case 'AGP':
          return 'Malaga'
      case 'TFS':
          return 'Tenerife'

header = ["Departure", "Destination", "Date", "Departure time", "Arrival time", "Flightnumber", "Duration", "Price"]
filename = "csv/Transavia.csv"

with open(filename, mode='w', newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)

for destination in destinations:
    for date in dates:
      headers = {
          # Request headers
          'apikey': '17c5625ff4424000b95a0ae6f3a23586',
      }
      params = urllib.parse.urlencode({
          # Request parameters
          'origin': 'BRU',
          'destination': destination,
          'originDepartureDate': date,
      })

      try:
        conn = http.client.HTTPSConnection('api.transavia.com')
        conn.request("GET", "/v1/flightoffers/?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()

        destinationFull = switchDestination(destination)

        if data == b'':
            departureTime = 'None'
            arrivalTime = 'None'
            price = 'None'
            duration = 'None'
            flightkey = 'None'
            date = datetime.datetime.strptime(date, '%Y%m%d').strftime('%d/%m/%Y')

            with open(filename, mode='a', newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Brussels', destinationFull, date, departureTime, arrivalTime, flightkey, duration, price])
            
            conn.close()
            continue
        data = json.loads(data)

        try:
            departure = data['flightOffer'][0]['outboundFlight']['departureDateTime']
            durationDeparture = departure
            departureTime = departure.split('T')[1]
            departureDate = departure.split('T')[0]
            departureTime = datetime.datetime.strptime(departureTime, '%H:%M:%S').strftime('%H:%M')
            departureDate = datetime.datetime.strptime(departureDate, '%Y-%m-%d').strftime('%d/%m/%Y')

            arrivalTime = data['flightOffer'][0]['outboundFlight']['arrivalDateTime']
            durationArrival = arrivalTime
            arrivalTime = arrivalTime.split('T')[1]
            arrivalTime = datetime.datetime.strptime(arrivalTime, '%H:%M:%S').strftime('%H:%M')

            price = data['flightOffer'][0]['pricingInfoSum']['totalPriceOnePassenger']
            price = float(price)

            durationDeparture = datetime.datetime.strptime(durationDeparture, '%Y-%m-%dT%H:%M:%S')
            durationArrival = datetime.datetime.strptime(durationArrival, '%Y-%m-%dT%H:%M:%S')
            duration = durationArrival - durationDeparture
            duration = duration.seconds / 60
            duration = int(duration)

            flightShortName = data['flightOffer'][0]['outboundFlight']['marketingAirline']['companyShortName']
            flightnumber = data['flightOffer'][0]['outboundFlight']['flightNumber']
            flightnumber = str(flightnumber)
            flightkey = flightShortName + flightnumber
        except:
            departureTime = 'None'
            arrivalTime = 'None'
            price = 'None'
            duration = 'None'
            flightkey = 'None'

        with open(filename, mode='a', newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Brussels', destinationFull, departureDate, departureTime, arrivalTime, flightkey, duration, price])

        conn.close()
      except Exception as e:
        print("Error has occured")
        print(e)

df = pd.read_csv(filename)
df.drop_duplicates(subset=None, inplace=True)
df.to_csv(filename, index=False)
