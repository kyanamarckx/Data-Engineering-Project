CREATE DATABASE IF NOT EXISTS AirFaresDWH;

CREATE TABLE IF NOT EXISTS DimAirport (
    airport_key INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    airport_iata_code VARCHAR(5) NOT NULL,
    airport_name VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL,
    country VARCHAR(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS DimAirline (
    airline_key INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    airline_iata_code VARCHAR(5) NOT NULL,
    airline_name VARCHAR(50) NOT NULL,
    country VARCHAR(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS DimFlight (
    flight_key INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    flight_id VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    flightnumber VARCHAR(10) NOT NULL,
    numberOfStops INT NOT NULL,
    departureTime TIME NOT NULL,
    arrivalTime TIME NOT NULL,
    duration TIME NOT NULL
);
CREATE TABLE IF NOT EXISTS DimDate (
    date_key INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    day_of_week INT NOT NULL,
    day_of_month INT NOT NULL,
    day_of_year INT NOT NULL,
    year INT NOT NULL,
    dayName VARCHAR(10) NOT NULL,
    monthName VARCHAR(10) NOT NULL,
    nameOfQuarter VARCHAR(10) NOT NULL,
    numberOfQuarter INT NOT NULL,
    isWeekend BIT NOT NULL,
    isWeekDay BIT NOT NULL,
    isHoliday BIT NOT NULL
);

CREATE TABLE IF NOT EXISTS FactFlightfare (
    flightfare_key INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    flight_key INT NOT NULL,
    airline_key INT NOT NULL,
    depatureAirportKey INT NOT NULL,
    arrivalAirportKey INT NOT NULL,
    scrapeDateKey INT NOT NULL,
    departureDateKey INT NOT NULL,
    arrivalDateKey INT NOT NULL,
    availableSeats INT NOT NULL,
    price DOUBLE NOT NULL,
    FOREIGN KEY (airline_key) REFERENCES DimAirline(airline_key),
    FOREIGN KEY (depatureAirportKey) REFERENCES DimAirport(airport_key),
    FOREIGN KEY (arrivalAirportKey) REFERENCES DimAirport(airport_key),
    FOREIGN KEY (scrapeDateKey) REFERENCES DimDate(date_key),
    FOREIGN KEY (departureDateKey) REFERENCES DimDate(date_key),
    FOREIGN KEY (arrivalDateKey) REFERENCES DimDate(date_key)
);