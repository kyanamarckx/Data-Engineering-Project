CREATE DEFINER = `root` @`localhost` PROCEDURE `UpdateDimFlight`() BEGIN
SET SQL_SAFE_UPDATES = 0;
create temporary table tmp_table
select gf.flight_id,
    gf.flightnumber,
    gf.number_of_stops,
    gf.departure_time,
    gf.arrival_time,
    gf.duration
from groep8dep.flight gf
    join dimflight df on gf.flight_id = df.flight_id
where (
        df.numberofstops <> gf.number_of_stops
        OR df.departureTime <> gf.departure_time
        OR df.arrivalTime <> gf.arrival_time
        OR df.duration <> gf.duration
    )
    and (end_date is null);
update dimflight
set end_date = date_add(curdate(), interval -1 day)
where flight_id in (
        select flight_id
        from tmp_table
    );
insert into dimflight (
        flight_id,
        flightnumber,
        numberOfStops,
        departureTime,
        arrivalTime,
        duration,
        start_date,
        end_date
    )
select *,
    curdate(),
    null
from tmp_table;
drop table tmp_table;
END