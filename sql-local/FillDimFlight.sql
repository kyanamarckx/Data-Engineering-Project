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
        isWeekDay,
        isHoliday
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
        END,
        CASE
            WHEN currentdate BETWEEN '2023-04-04' AND '2023-04-16' THEN 1
            WHEN currentdate LIKE '2023-05-01' THEN 1
            WHEN currentdate BETWEEN '2023-05-18' AND '2023-05-19' THEN 1
            WHEN currentdate LIKE '2023-05-29' THEN 1
            WHEN currentdate BETWEEN '2023-07-01' AND '2023-08-31' THEN 1
            ELSE 0
        END
    );
SET currentdate = DATE_ADD(currentdate, INTERVAL 1 DAY);
END WHILE;
END