		-- Hierna bevat de temporary table de structuur van de tabel flight, maar de tabel is leeg (WHERE flight_id = 'A')
		CREATE TEMPORARY TABLE temp_tbl 
		SELECT *
		FROM flight
		WHERE flight_id = 'A';        
	
		LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\All.csv'
		INTO TABLE temp_tbl
		FIELDS TERMINATED BY ','
		LINES TERMINATED BY '\n'
		(@flight_id, @flightnumber, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
		SET flight_id = @flight_id, flightnumber = @flightnumber, departure_date = @departure_date, arrival_date = @arrival_date, departure_time = @departure_time, arrival_time = @arrival_time, duration = @duration, number_of_stops = @number_of_stops, airline_iata_code = @airline_iata_code, departure_airport_iata_code = @departure_airport_iata_code, arrival_airport_iata_code = @arrival_airport_iata_code;

        -- Merge de nieuwe data met de al bestaande data
        -- In SQL Server bestaat het commando Merge (Zie Chamilo > Relational Databases > Docmenten > Slides > 2. SQL Advanced > Slide 38 Merge
        -- In MySQL bestaat dat niet. In plaats daarvan kunnen we gebruik maken van het volgende
        -- https://dev.mysql.com/doc/refman/5.7/en/insert-on-duplicate.html
        
    INSERT INTO flight
		SELECT * FROM temp_tbl
		ON DUPLICATE KEY UPDATE flight.departure_time = temp_tbl.departure_time, flight.arrival_time = temp_tbl.arrival_time, flight.duration = temp_tbl.duration, flight.number_of_stops = temp_tbl.number_of_stops;
        
        
		DROP TABLE temp_tbl;
        
        
		CREATE TEMPORARY TABLE temp_tbl_2 (
			`flight_id` char(255) DEFAULT NULL,
			`scrape_date` date,
			`available_seats` int DEFAULT NULL,
			`price` double DEFAULT NULL
		);        
        
        
		LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\All.csv'
		INTO TABLE temp_tbl_2
		FIELDS TERMINATED BY ','
		LINES TERMINATED BY '\n'
		(@flight_id, @flightnumber, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
		SET flight_id=@flight_id, scrape_date=@scrape_date, available_seats=@available_seats, price=@price;
        
        
        
		-- Door de INSERT te doen met behulp van de temporary table, worden de AUTO INCREMENT primary keys gemaakt
        INSERT INTO flightfare(flight_id, scrape_date, available_seats, price)
		SELECT * FROM temp_tbl_2;

		DROP TABLE temp_tbl_2;