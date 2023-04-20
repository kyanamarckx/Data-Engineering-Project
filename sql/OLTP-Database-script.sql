create database groep8dep;
use groep8dep;
create table flight (
    flight_id VARCHAR(50) PRIMARY KEY,
    flightnumber VARCHAR(10),
    departure_date DATE,
    arrival_date DATE,
    departure_time TIME,
    arrival_time TIME,
    duration TIME,
    number_of_stops INT UNSIGNED,
    airline_iata_code VARCHAR(2),
    departure_airport_iata_code VARCHAR(5),
    arrival_airport_iata_code VARCHAR(5)
);
create table flightfare (
    flightfare_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    flight_id VARCHAR(50) DEFAULT NULL,
    scrape_date DATE DEFAULT NULL,
    available_seats INT DEFAULT NULL,
    price double DEFAULT NULL
);
create table airport (
    airport_iata_code VARCHAR(5) PRIMARY KEY,
    name VARCHAR(25),
    location VARCHAR(25),
    country VARCHAR(25)
);
create table airline (
    airline_iata_code VARCHAR(2) PRIMARY KEY,
    name VARCHAR(25),
    country VARCHAR(25)
);
# SHOW VARIABLES LIKE "secure_file_priv";
# SELECT * FROM mysql.user;
# drop table flightfare;
# drop table flight;
# drop table airline;
# drop table airport;
# drop database groep8DEP;