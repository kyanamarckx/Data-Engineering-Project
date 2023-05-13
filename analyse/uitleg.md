# Uitleg voor loadAllFiles.sql maar 1 keer uit te moeten voeren
## Context en uitgebreide uitleg

Wanneer je de database en tabellen van groep8dep en airFaresDWH met de nodige Stored Procedures hebt aangemaakt (OLTP-Database-script.sql en DWH-Database-script.sql) voer je mijn nieuw bestand (deleteRows.sql) uit om alle (als die al aanwezig zou zijn) rijen van alle tabellen uit de databases te verwijderen. Deze file run je telkens wanneer er nieuwe data beschikbaar is (elke dag dus). Al deze bestanden staan in de sql-local directory

Als tweede voer je ReadInto1CSV.py uit. Daarvoor heb je de juiste csv All-files in de uploadsmap nodig van MySQL. (Dit kan je makkelijk laten gebeuren door copyFiles.py uit te voeren, je moet in die file juist controleren dat de source_folder variabele het juiste pad van de snelkoppeling bevat van AirFares, de shared OneDrive).
De ReadInto1CSV.py gaat 1 grote CSV genaamd COMBINED.csv aanmaken in de Uploads map die bestaat uit alle All-csv's. Omdat we nu 1 grote CSV-file hebben met alle data in moeten we ons ook geen zorgen maken over duplicates dus dat is ook een probleem vermijden.

Nu dat we 1 volledige csv hebben voer je de laatste nieuwe file uit (loadCSV.sql in de sql-local directory). Dit is ongeveer dezelfde file als de LoadAllFiles.sql, enkel is het pad naar de csv veranderd dus make sure dat je loadCSV.sql uitvoert!! Hou er ook rekening mee dat deze file dus maar **één** keer moet uitgevoerd worden (in de zin van je moet niet telkens het pad naar een andere csv file aanpassen en opnieuw uitvoeren, je voert de file 1 keer volledig uit en je bent klaar).

Alle data staat nu dus al in de OLTP-database en dit moet nog gemigreerd worden naar de datawarehouse.

Hiervoor volg je het stappenplan van Levi:
  - open het bestand DWH-script.sql
  - kijk eerst of je de juiste database hebt geselecteerd. (airfaresdwh)
  - voer dan eerst lijn 10 uit of call FillDimDate();
  - voer dan het INSERT statement van DimAirline uit.
  - voer dan het INSERT statement van DimAirport uit.
  - dan voer je call FillDimFlight(); uit. (DIT MAG MAAR 1 KEER GEBEUREN MET NIEUWE DATA)
  - dan voer je UpdateDimFlight(); uit.
  - dan als laatste voer je call FillFactflightfare(); uit.


## Kort samengevat
1. Zorg ervoor dat groep8dep en airfaresdwh bestaan met alle tabellen en stored procedures
2. voer ``deleteRows.sql`` uit
3. voer ``ReadInto1CSV.py`` uit
4. voer ``loadCSV.sql`` uit (**éénmalig**, telkens wanneer er een nieuwe All-file van Sabine beschikbaar is)
5. open ```DWH-script.sql`` uit
6. selecteer airfaresdwh
7. voer ``call FillDimDate()`` uit
8. voer INSERT statement van DimAirline uit
9. voer INSERT statement van DimAirport uit
10. voer ``call FillDimFlight()`` uit
11. voer ``UpdateDimFlight()`` uit
12. voer ``FillFactflightfare()`` uit

DONE :)))