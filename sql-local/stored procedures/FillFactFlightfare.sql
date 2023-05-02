CREATE DEFINER = `root` @`localhost` PROCEDURE `FillFactflightfare`() BEGIN
INSERT INTO factflightfare (
        flight_key,
        airline_key,
        depatureAirportKey,
        arrivalAirportKey,
        scrapeDateKey,
        departureDateKey,
        arrivalDateKey,
        availableSeats,
        price
    )
SELECT df.flight_key,
    da.airline_key,
    dp.airport_key,
    dpt.airport_key,
    dd.date_key,
    dda.date_key,
    ddz.date_key,
    ff.available_seats,
    ff.price
FROM groep8dep.flightfare ff
    JOIN dimflight df on ff.flight_id = df.flight_id
    JOIN groep8dep.flight f on ff.flight_id = f.flight_id
    JOIN dimairline da on f.airline_iata_code = da.airline_iata_code
    JOIN dimairport dp on f.departure_airport_iata_code = dp.airport_iata_code
    JOIN dimairport dpt on f.arrival_airport_iata_code = dpt.airport_iata_code
    JOIN dimdate dd on ff.scrape_date = dd.date
    join dimdate dda on f.departure_date = dda.date
    join dimdate ddz on f.arrival_date = ddz.date
WHERE ff.scrape_date >= df.start_date
    and (
        df.end_date is null
        or ff.scrape_date <= df.end_date
    )
    AND ff.flightfare_id > (
        SELECT IFNULL(MAX(flightfare_key), 0)
        from factflightfare
    );
END