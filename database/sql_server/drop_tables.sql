use formula1;

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'qualifying')
BEGIN
ALTER TABLE [dbo].[qualifying] 
DROP CONSTRAINT [FK_raceId_qualifying],[FK_droverId_qualifying],[FK_constructorId_qualyfying]
END
;

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'lap_times')
BEGIN
ALTER TABLE [dbo].[lap_times] 
DROP CONSTRAINT [FK_raceId_lap],[FK_driverId_lap]
END
;

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'pit_stops')
BEGIN
ALTER TABLE [dbo].[pit_stops] 
DROP CONSTRAINT [FK_raceId_pit],[FK_driverId_pit]
END
;

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'races')
BEGIN
ALTER TABLE [dbo].[races] 
DROP CONSTRAINT [FK_circuits_races]
END
;

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'constructor_results')
BEGIN
ALTER TABLE [dbo].[constructor_results] 
DROP CONSTRAINT [FK_raceId_constructor_results],[FK_constructorId_constructor_results]
END
;
IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'constructor_standings')
BEGIN
ALTER TABLE [dbo].[constructor_standings] 
DROP CONSTRAINT [FK_raceId_constructor_standings],[FK_constructorId_constructor_standings]
END
;

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'driver_standings')
BEGIN
ALTER TABLE [dbo].[driver_standings] 
DROP CONSTRAINT [FK_raceId_driver_standings],[FK_driverId_driver_standings]
END
;

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'results')
BEGIN
ALTER TABLE [dbo].[results] 
DROP CONSTRAINT [FK_raceId_results],[FK_driverId_results],[FK_constructorId_results]
END
;

DROP TABLE IF EXISTS dbo.circuits
DROP TABLE IF EXISTS dbo.races
DROP TABLE IF EXISTS dbo.drivers
DROP TABLE IF EXISTS dbo.constructors
DROP TABLE IF EXISTS dbo.qualifying
DROP TABLE IF EXISTS dbo.lap_times
DROP TABLE IF EXISTS dbo.pit_stops
DROP TABLE IF EXISTS dbo.seasons
DROP TABLE IF EXISTS dbo.status
DROP TABLE IF EXISTS dbo.constructor_results
DROP TABLE IF EXISTS dbo.constructor_standings
DROP TABLE IF EXISTS dbo.driver_standings
DROP TABLE IF EXISTS dbo.results

