USE AirFaresDWH;	-- naam van de datawarehous

SET SQL_SAFE_UPDATES = 0; 	-- Anders is DELETE FROM niet mogelijk

-- temporarily disable constraints
SET FOREIGN_KEY_CHECKS=0;

-- Empty and recreate DimDate
DELETE FROM DimDATE;

-- Vul DimDate op: zoek script via Google + plaats dit in Stored procedure en roep de stored procedure aan

-- Update reeds bestaande records DimAirline (dit is geen Slowly Changing Dimension)
UPDATE DimAirline da SET airline_name = (SELECT airline_name FROM airfares.airline WHERE airfares.airline.airline_iata_code = da.airline_iata_code);

-- Insert nieuwe records
INSERT INTO DimAirline(airline_iata_code, airline_name)
SELECT DISTINCT airline_iata_code, airline_name FROM airfares.airline WHERE airline_iata_code NOT IN (SELECT DISTINCT airline_iata_code FROM DimAirline);

-- Update reeds bestaande records DimAirport (dit is geen Slowly Changing Dimension)
-- Insert nieuwe records DimAirport