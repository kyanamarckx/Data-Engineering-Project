CREATE DEFINER = `root` @`localhost` PROCEDURE `FillDimDate`() BEGIN
DECLARE currentdate DATE DEFAULT DATE_FORMAT('2023-04-04', '%Y-%m-%d');
WHILE currentdate <= DATE_FORMAT('2023-10-01', '%Y-%m-%d') DO
INSERT INTO DimDate(
        date,
        day_of_week,
        day_of_month,
        day_of_year,
        year,
        dayName,
        monthName,
        nameOfQuarter,
        numberOfQuarter,
        isWeekend,
        isWeekDay
    )
VALUES (
        currentdate,
        DAYOFWEEK(currentdate),
        DAY(currentdate),
        DAYOFYEAR(currentdate),
        YEAR(currentdate),
        DATE_FORMAT(currentdate, '%W'),
        DATE_FORMAT(currentdate, '%M'),
        CONCAT('Q', QUARTER(currentdate)),
        QUARTER(currentdate),
        CASE
            DAYOFWEEK(currentdate)
            WHEN 1 THEN 1 -- Sunday
            WHEN 7 THEN 1 -- Saturday
            ELSE 0
        END,
        CASE
            DAYOFWEEK(currentdate)
            WHEN 1 THEN 0 -- Sunday
            WHEN 7 THEN 0 -- Saturday
            ELSE 1
        END
    );
SET currentdate = DATE_ADD(currentdate, INTERVAL 1 DAY);
END WHILE;
END