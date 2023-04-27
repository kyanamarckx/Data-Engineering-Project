CREATE DEFINER = `root` @`localhost` PROCEDURE `FillDimFlight`(IN start_date DATE, IN end_date DATE) BEGIN
SET SQL_SAFE_UPDATES = 0;
DROP TEMPORARY TABLE IF EXISTS tempFlightData;
-- Step 1: Extract data from the OLTP database
CREATE TEMPORARY TABLE tempFlightData AS
SELECT f.flight_id,
    start_date,
    end_date,
    f.flightnumber,
    f.number_of_stops,
    f.departure_time,
    f.arrival_time,
    f.duration
FROM groep8dep.flight f;
-- add any necessary joins or filters here
-- Step 2: Transform the data as needed
UPDATE tempFlightData
SET start_date = DATE(start_date),
    end_date = DATE(end_date),
    duration = CAST(duration AS TIME),
    departure_time = CAST(departure_time AS TIME),
    arrival_time = CAST(arrival_time AS TIME);
-- Step 3: Load the data into the DimFlight table
INSERT INTO DimFlight (
        flight_id,
        start_date,
        end_date,
        flightnumber,
        numberOfStops,
        departureTime,
        arrivalTime,
        duration
    )
SELECT flight_id,
    start_date,
    end_date,
    flightnumber,
    number_of_stops,
    departure_time,
    arrival_time,
    duration
FROM tempFlightData;
-- Clean up temporary table
DROP TEMPORARY TABLE IF EXISTS tempFlightData;
END