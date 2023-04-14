CREATE TEMPORARY TABLE temp_tbl
SELECT *
FROM flight
WHERE flight_id = 'A';
LOAD DATA INFILE '/var/lib/mysql-files/Tui.csv' INTO TABLE temp_tbl FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' (
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
LOAD DATA INFILE '/var/lib/mysql-files/Tui.csv' INTO TABLE temp_tbl_2 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' (
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