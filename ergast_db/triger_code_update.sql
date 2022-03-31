USE formula1
GO

CREATE TRIGGER code_update
ON drivers
    AFTER INSERT AS
    WITH t as (
    SELECT 
    driverId, code,
    trim(upper(left(forename,1) + left(surname,1))) +
    trim(str(ROW_NUMBER() OVER(PARTITION BY upper(left(forename,1) + left(surname,1)) ORDER BY upper(left(forename,1) + left(surname,1)) ASC))) as num
    FROM drivers
    )

    UPDATE drivers
    SET code = (SELECT num from t where t.driverId = drivers.driverId)
    WHERE code = '';

select top 1000 * from drivers
