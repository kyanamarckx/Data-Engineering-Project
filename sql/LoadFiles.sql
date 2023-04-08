
		-- DEEL 1 --
        -- De tabel flight wordt gevuld. Dit moet gebeuren vóór het vullen van de tabel flightfare omwille van foreign keys
        -- De tabel flight bevat o.a. flight_id, flightnumber, departure_date, arrival_date, departure_time, arrival_time, ...
        -- De bestanden móeten in de map C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\ staan
        -- Het pad C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\ is te vinden via het commando SHOW VARIABLES LIKE "secure_file_priv";
        -- Anders krijg je Error Code: 1290. The MySQL server is running with the --secure-file-priv option so it cannot execute this statement

		-- Hierna bevat de temporary table de structuur van de tabel flight, maar de tabel is leeg (WHERE flight_id = 'A')
		CREATE TEMPORARY TABLE temp_tbl 
		SELECT *
		FROM flight
		WHERE flight_id = 'A';        
	
		LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Ryanair.csv'
		INTO TABLE temp_tbl
		FIELDS TERMINATED BY ','
		LINES TERMINATED BY '\n'
		(@flight_id, @flightnumber, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
		SET flight_id=@flight_id, flightnumber=@flightnumber, departure_date=@departure_date, arrival_date=@arrival_date, departure_time=@departure_time, arrival_time=@arrival_time, duration=@duration, number_of_stops=@number_of_stops,
		airline_iata_code=@airline_iata_code, departure_airport_iata_code=@departure_airport_iata_code, arrival_airport_iata_code=@arrival_airport_iata_code;
        
		LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Tui.csv'
		INTO TABLE temp_tbl
		FIELDS TERMINATED BY ','
		LINES TERMINATED BY '\n'
		(@flight_id, @flightnumber, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
		SET flight_id=@flight_id, flightnumber=@flightnumber, departure_date=@departure_date, arrival_date=@arrival_date, departure_time=@departure_time, arrival_time=@arrival_time, duration=@duration, number_of_stops=@number_of_stops,
		airline_iata_code=@airline_iata_code, departure_airport_iata_code=@departure_airport_iata_code, arrival_airport_iata_code=@arrival_airport_iata_code;   
        
		LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Transavia.csv'
		INTO TABLE temp_tbl
		FIELDS TERMINATED BY ','
		LINES TERMINATED BY '\n'
		(@flight_id, @flightnumber, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
		SET flight_id=@flight_id, flightnumber=@flightnumber, departure_date=@departure_date, arrival_date=@arrival_date, departure_time=@departure_time, arrival_time=@arrival_time, duration=@duration, number_of_stops=@number_of_stops,
		airline_iata_code=@airline_iata_code, departure_airport_iata_code=@departure_airport_iata_code, arrival_airport_iata_code=@arrival_airport_iata_code;
        
        -- Merge de nieuwe data met de al bestaande data
        -- In SQL Server bestaat het commando Merge (Zie Chamilo > Relational Databases > Docmenten > Slides > 2. SQL Advanced > Slide 38 Merge
        -- In MySQL bestaat dat niet. In plaats daarvan kunnen we gebruik maken van het volgende
        -- https://dev.mysql.com/doc/refman/5.7/en/insert-on-duplicate.html
        
        INSERT INTO flight
		SELECT * FROM temp_tbl
		ON DUPLICATE KEY UPDATE flight.departure_time = temp_tbl.departure_time, flight.arrival_time = temp_tbl.arrival_time, flight.duration = temp_tbl.duration, flight.number_of_stops = temp_tbl.number_of_stops;
        
        
		DROP TABLE temp_tbl;

		-- DEEL 2 --        
        -- De tabel flightfare wordt gevuld met Ryanair.csv, Transavia.csv en Tui.csv
        -- De tabel flightfare bevat o.a. flightfare_id (AUTO INCREMENT), flight_id, scrape_date, available_seats, price
		-- Ook hier moet er gebruik gemaakt worden van een temporary table. Er is bewust geen primary key voorzien.
        -- Anders wordt de Load into flightfare niet uitgevoerd vanuit het Python script omdat er met auto-increment gewerkt wordt en er geen primary keys zijn
		
		CREATE TEMPORARY TABLE temp_tbl_2 (
			`flight_id` char(255) DEFAULT NULL,
			`scrape_date` date DEFAULT NULL,
			`available_seats` int DEFAULT NULL,
			`price` double DEFAULT NULL
		);

		LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Ryanair.csv'
		INTO TABLE temp_tbl_2
		FIELDS TERMINATED BY ','
		LINES TERMINATED BY '\n'
		(@flight_id, @flightnumber, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
		SET flight_id=@flight_id, scrape_date=@scrape_date, available_seats=@available_seats, price=@price;
        
		LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Tui.csv'
		INTO TABLE temp_tbl_2
		FIELDS TERMINATED BY ','
		LINES TERMINATED BY '\n'
		(@flight_id, @flightnumber, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
		SET flight_id=@flight_id, scrape_date=@scrape_date, available_seats=@available_seats, price=@price;
        
        
		LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Transavia.csv'
		INTO TABLE temp_tbl_2
		FIELDS TERMINATED BY ','
		LINES TERMINATED BY '\n'
		(@flight_id, @flightnumber, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
		SET flight_id=@flight_id, scrape_date=@scrape_date, available_seats=@available_seats, price=@price;

		-- Door de INSERT te doen met behulp van de temporary table, worden de AUTO INCREMENT primary keys gemaakt
        INSERT INTO flightfare(flight_id, scrape_date, available_seats, price)
		SELECT * FROM temp_tbl_2;

		DROP TABLE temp_tbl_2;
