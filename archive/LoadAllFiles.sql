CREATE TEMPORARY TABLE temp_tbl
SELECT *
FROM flight
WHERE flight_id = 'A';
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/All_2023_04_20.csv' INTO TABLE temp_tbl FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' (
	@flight_id,
	@flightnumber,
	@departure_date,
	@arrival_date,
	@departure_time,
	@arrival_time,
	@duration,
	@number_of_stops,
	@airline_iata_code,
	@departure_airport_iata_code,
	@arrival_airport_iata_code,
	@scrape_date,
	@available_seats,
	@price
)
SET flight_id = @flight_id,
	flightnumber = @flightnumber,
	departure_date = @departure_date,
	arrival_date = @arrival_date,
	departure_time = @departure_time,
	arrival_time = @arrival_time,
	duration = @duration,
	number_of_stops = @number_of_stops,
	airline_iata_code = @airline_iata_code,
	departure_airport_iata_code = @departure_airport_iata_code,
	arrival_airport_iata_code = @arrival_airport_iata_code;
    
INSERT INTO flight
SELECT *
FROM temp_tbl ON DUPLICATE KEY
UPDATE flight.departure_time = temp_tbl.departure_time,
	flight.arrival_time = temp_tbl.arrival_time,
	flight.duration = temp_tbl.duration,
	flight.number_of_stops = temp_tbl.number_of_stops;
DROP TABLE temp_tbl;

CREATE TEMPORARY TABLE temp_tbl_2 (
	`flight_id` char(255) DEFAULT NULL,
	`scrape_date` date DEFAULT NULL,
	`available_seats` int DEFAULT NULL,
	`price` double DEFAULT NULL
);
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/All_2023_04_20.csv' INTO TABLE temp_tbl_2 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' (
	@flight_id,
	@flightnumber,
	@departure_date,
	@arrival_date,
	@departure_time,
	@arrival_time,
	@duration,
	@number_of_stops,
	@airline_iata_code,
	@departure_airport_iata_code,
	@arrival_airport_iata_code,
	@scrape_date,
	@available_seats,
	@price
)
SET flight_id = @flight_id,
	scrape_date = @scrape_date,
	available_seats = @available_seats,
	price = @price;
    
INSERT INTO flightfare(flight_id, scrape_date, available_seats, price)
SELECT *
FROM temp_tbl_2;
DROP TABLE temp_tbl_2;

CREATE TEMPORARY TABLE temp_tbl_3 (
	`airline_iata_code` VARCHAR(5) NOT NULL,
    `airline_name` VARCHAR(25) NOT NULL,
    `country` VARCHAR(25) NOT NULL
);

INSERT INTO temp_tbl_3 (airline_iata_code, airline_name, country)
VALUES 
	('FR', 'Ryanair', 'Ireland'),
	('HV', 'Transavia', 'Netherlands'),
	('SN', 'Brussels Airlines', 'Belgium'),
    ('TB', 'Tui', 'Belgium');

INSERT INTO airline(airline_iata_code, airline_name, country)
SELECT *
FROM temp_tbl_3;
DROP TABLE temp_tbl_3;

CREATE TEMPORARY TABLE temp_tbl_4 (
	`airport_iata_code` VARCHAR(5) NOT NULL,
    `airport_name` VARCHAR(50) NOT NULL,
    `location` VARCHAR(50) NOT NULL,
    `country` VARCHAR(25) NOT NULL
);

INSERT INTO temp_tbl_4 (airport_iata_code, airport_name, location, country)
VALUES 
	('CRL', 'Aereport De Chaleroi Bruxelles Sud', 'Charleroi', 'Belgium'),
	('BRU', 'Brussels Airline', 'Zaventem', 'Belgium'),
	('ANR', 'Antwerpen International Airport', 'Antwerp', 'Belgium'),
	('LGG', 'Liege Airport', 'Liege', 'Belgium'),
    ('OST', 'Oostende-Brugge International Airport', 'Ostend', 'Belgium'),
    ('ALC', 'Alicante Airport', 'Alicante', 'Spain'),
    ('CFU', 'Corfu Airport', 'Corfu', 'Greece'),
    ('HER', 'Heraklion Airport', 'Heraklion', 'Greece'),
    ('RHO', 'Rhodes International Airport', 'Rhodes', 'Greece'),
    ('BDS', 'Salento Airport', 'Brindisi', 'Italy'),
    ('NAP', 'Aeroporto di Napoli', 'Napoli', 'Italy'),
    ('PMO', 'Palermo Airport', 'Cinisi', 'Italy'),
    ('FAO', 'Gago Coutinho Airport', 'Faro', 'Portugal'),
    ('AGP', 'Malaga-Costa del Sol Airport', 'Malaga', 'Spain'),
    ('PMI', 'Palma de Mallorca Airport', 'Palma de Mallorca', 'Spain'),
    ('TFS', 'Tenerife South Airport', 'Santa Cruz de Tenerife', 'Spain'),
    ('IBZ', 'Ibiza Airport', 'Ibiza', 'Spain');

INSERT INTO airport(airport_iata_code, airport_name, location, country)
SELECT *
FROM temp_tbl_4;
DROP TABLE temp_tbl_4;