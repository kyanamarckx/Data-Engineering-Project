SET SQL_SAFE_UPDATES = 0;

-- verwijder inhoud van groep8dep
DELETE FROM groep8dep.airline;
DELETE FROM groep8dep.airport;
DELETE FROM groep8dep.flight;
DELETE FROM groep8dep.flightfare;

-- verwijder inhoud van airfaresdwh
DELETE FROM airfaresdwh.dimairline;
DELETE FROM airfaresdwh.dimairport;
DELETE FROM airfaresdwh.dimdate;
DELETE FROM airfaresdwh.dimflight;
DELETE FROM airfaresdwh.factflightfare;