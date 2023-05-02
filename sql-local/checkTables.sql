-- voer dit uit voor alle tabellen te selecteren van de dwh
use airfaresdwh;

select * from dimairline;
select * from dimairport;
select * from dimdate;
select * from dimflight;
select * from factflightfare;
-- tot hier voor dwh

-- voer dit uit voor alle tabellen te selecteren van de OLTP database
use groep8dep;

select * from groep8dep.airline;
select * from groep8dep.airport;
select * from groep8dep.flight;
select * from groep8dep.flightfare;
-- tot hier voor OLTP