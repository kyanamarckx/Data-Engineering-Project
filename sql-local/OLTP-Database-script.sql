CREATE DATABASE IF NOT EXISTS groep8dep;

USE groep8dep;

CREATE TABLE IF NOT EXISTS flightfare (
    flightfare_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    flight_id VARCHAR(50) DEFAULT NULL,
    scrape_date DATE DEFAULT NULL,
    available_seats INT DEFAULT NULL,
    price double DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS airport (
    airport_iata_code VARCHAR(5) NOT NULL PRIMARY KEY,
    airport_name VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL,
    country VARCHAR(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS airline (
    airline_iata_code VARCHAR(5) NOT NULL PRIMARY KEY,
    airline_name VARCHAR(25) NOT NULL,
    country VARCHAR(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS flight (
    flight_id VARCHAR(50) NOT NULL PRIMARY KEY,
    flightnumber VARCHAR(10) NOT NULL,
    departure_date DATE NOT NULL,
    arrival_date DATE NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    duration TIME NOT NULL,
    number_of_stops INT NOT NULL,
    airline_iata_code VARCHAR(5) NOT NULL,
    departure_airport_iata_code VARCHAR(5) NOT NULL,
    arrival_airport_iata_code VARCHAR(5) NOT NULL,
    FOREIGN KEY (departure_airport_iata_code) REFERENCES airport (airport_iata_code),
    FOREIGN KEY (arrival_airport_iata_code) REFERENCES airport (airport_iata_code),
    FOREIGN KEY (airline_iata_code) REFERENCES airline (airline_iata_code)
);

# SHOW VARIABLES LIKE "secure_file_priv";
# SELECT * FROM mysql.user;
# drop table flightfare;
# drop table flight;
# drop table airline;
# drop table airport;
# drop database groep8DEP;