USE AirFaresDWH; -- naam van de datawarehous

SET SQL_SAFE_UPDATES = 0; -- Anders is DELETE FROM niet mogelijk
SET FOREIGN_KEY_CHECKS = 0; -- temporarily disable constraints

-- DimDate
DELETE FROM DimDate; -- Empty and recreate DimDate
call FillDimDate();

-- DimAirline
-- Update reeds bestaande records DimAirline (dit is geen Slowly Changing Dimension)
UPDATE DimAirline da SET airline_name = (SELECT airline_name FROM groep8dep.airline WHERE groep8dep.airline.airline_iata_code = da.airline_iata_code);
-- Insert nieuwe records
INSERT INTO DimAirline(airline_iata_code, airline_name)
SELECT DISTINCT airline_iata_code, airline_name FROM groep8dep.airline WHERE airline_iata_code NOT IN (SELECT DISTINCT airline_iata_code FROM DimAirline);

-- DimAirport
-- Update reeds bestaande records DimAirport (dit is geen Slowly Changing Dimension)
UPDATE DimAirport da SET airport_name = (SELECT airport_name FROM groep8dep.airport WHERE groep8dep.airport.airport_iata_code = da.airport_iata_code);
-- Insert nieuwe records DimAirport
INSERT INTO DimAirport(airport_iata_code, airport_name)
SELECT DISTINCT airport_iata_code, airport_name FROM groep8dep.airport WHERE airport_iata_code NOT IN (SELECT DISTINCT airport_iata_code FROM DimAirport);

-- DimFlight (Slowly Changing Dimension)
call FillDimFlight('2023-04-01', '2023-10-01');

-- FactFlightfare
