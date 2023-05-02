CREATE DEFINER = `root` @`localhost` PROCEDURE `FillDimFlight`() BEGIN -- Add OLTP data to DWH
INSERT INTO dimflight (
        flight_id,
        flightnumber,
        numberOfStops,
        departureTime,
        arrivalTime,
        duration,
        start_date,
        end_date
    )
SELECT flight_id,
    flightnumber,
    number_of_stops,
    departure_time,
    arrival_time,
    duration,
    '2023-04-01',
    null
FROM groep8dep.flight;
END