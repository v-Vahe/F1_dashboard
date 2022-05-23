use formula1;

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'qualifying')
BEGIN
ALTER TABLE [dbo].[qualifying] 
DROP CONSTRAINT [FK_raceId_races_1],[FK_driverId_drivers_0],[FK_constructorId_constructors_1]
END
;

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'lap_times')
BEGIN
ALTER TABLE [dbo].[lap_times] 
DROP CONSTRAINT [FK_raceId_races_2],[FK_driverId_drivers_1]
END
;

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'pit_stops')
BEGIN
ALTER TABLE [dbo].[pit_stops] 
DROP CONSTRAINT [FK_raceId_races_3],[FK_driverId_drivers_2]
END
;

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'races')
BEGIN
ALTER TABLE [dbo].[races] 
DROP CONSTRAINT [FK_circuitId_circuits]
END
;

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'constructor_results')
BEGIN
ALTER TABLE [dbo].[constructor_results] 
DROP CONSTRAINT [FK_raceId_races_4],[FK_constructorId_constructors_2]
END
;
IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'constructor_standings')
BEGIN
ALTER TABLE [dbo].[constructor_standings] 
DROP CONSTRAINT [FK_raceId_races_5],[FK_constructorId_constructors_3]
END
;

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'driver_standings')
BEGIN
ALTER TABLE [dbo].[driver_standings] 
DROP CONSTRAINT [FK_raceId_races_6],[FK_driverId_drivers_3]
END
;

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'results')
BEGIN
ALTER TABLE [dbo].[results] 
DROP CONSTRAINT [FK_raceId_races_7],[FK_driverId_drivers_4],[FK_constructorId_constructors_4]
END
;

DROP TABLE IF EXISTS dbo.circuits;
DROP TABLE IF EXISTS dbo.races;
DROP TABLE IF EXISTS dbo.drivers;
DROP TABLE IF EXISTS dbo.constructors;
DROP TABLE IF EXISTS dbo.qualifying;
DROP TABLE IF EXISTS dbo.lap_times;
DROP TABLE IF EXISTS dbo.pit_stops;
DROP TABLE IF EXISTS dbo.seasons;
DROP TABLE IF EXISTS dbo.status;
DROP TABLE IF EXISTS dbo.constructor_results;
DROP TABLE IF EXISTS dbo.constructor_standings;
DROP TABLE IF EXISTS dbo.driver_standings;
DROP TABLE IF EXISTS dbo.results;

