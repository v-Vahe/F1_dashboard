
IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'qualifying')
BEGIN
ALTER TABLE [dbo].[qualifying] 
DROP CONSTRAINT [FK_raceId_qualifying],[FK_droverId_qualifying],[FK_constructorId_qualyfying]
END 
GO

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'lap_times')
BEGIN
ALTER TABLE [dbo].[lap_times] 
DROP CONSTRAINT [FK_raceId_lap],[FK_driverId_lap]
END 
GO

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'pit_stops')
BEGIN
ALTER TABLE [dbo].[pit_stops] 
DROP CONSTRAINT [FK_raceId_pit],[FK_driverId_pit]
END
GO

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'races')
BEGIN
ALTER TABLE [dbo].[races] 
DROP CONSTRAINT [FK_circuits_races]
END 
GO

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'constructor_results')
BEGIN
ALTER TABLE [dbo].[constructor_results] 
DROP CONSTRAINT [FK_raceId_constructor_results],[FK_constructorId_constructor_results]
END 
GO 

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'constructor_standings')
BEGIN
ALTER TABLE [dbo].[constructor_standings] 
DROP CONSTRAINT [FK_raceId_constructor_standings],[FK_constructorId_constructor_standings]
END 
GO

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'driver_standings')
BEGIN
ALTER TABLE [dbo].[driver_standings] 
DROP CONSTRAINT [FK_raceId_driver_standings],[FK_driverId_driver_standings]
END 
GO

IF EXISTS (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'results')
BEGIN
ALTER TABLE [dbo].[results] 
DROP CONSTRAINT [FK_raceId_results],[FK_driverId_results],[FK_constructorId_results]
END 
GO

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


CREATE TABLE circuits (
  circuitId TINYINT NOT NULL IDENTITY(1,1),
  circuitRef varchar(255) NOT NULL DEFAULT '',
  name varchar(255) NOT NULL DEFAULT '',
  location varchar(255) DEFAULT NULL,
  country varchar(255) DEFAULT NULL,
  lat float DEFAULT NULL,
  lng float DEFAULT NULL,
  alt SMALLINT DEFAULT NULL,
  url varchar(255) NOT NULL UNIQUE DEFAULT '',
  date_added  datetime NOT NULL DEFAULT getdate(),
  PRIMARY KEY (circuitId)
) 

CREATE TABLE races (
  raceId int NOT NULL IDENTITY(1,1),
  year int NOT NULL DEFAULT '0',
  round int NOT NULL DEFAULT '0',
  circuitId tinyint NOT NULL,
  name varchar(255) NOT NULL DEFAULT '',
  date date NOT NULL,
  time time DEFAULT NULL,
  url varchar(255) DEFAULT NULL,
  PRIMARY KEY (raceId),
  CONSTRAINT FK_circuits_races FOREIGN KEY (circuitId) REFERENCES circuits(circuitId)

) 

CREATE TABLE drivers (
  driverId int NOT NULL IDENTITY(1,1),
  driverRef varchar(255) NOT NULL DEFAULT '',
  number int DEFAULT NULL,
  code varchar(3) DEFAULT NULL,
  forename varchar(255) NOT NULL DEFAULT '',
  surname varchar(255) NOT NULL DEFAULT '',
  dob date DEFAULT NULL,
  nationality varchar(255) DEFAULT NULL,
  url varchar(255) NOT NULL UNIQUE DEFAULT '',
  PRIMARY KEY (driverId),
) 

CREATE TABLE constructors (
  constructorId int NOT NULL IDENTITY(1,1),
  constructorRef varchar(255) NOT NULL DEFAULT '',
  name varchar(255) NOT NULL DEFAULT '',
  nationality varchar(255) DEFAULT NULL,
  url varchar(255) DEFAULT '',
  PRIMARY KEY (constructorId),
) 

CREATE TABLE qualifying (
  qualifyId int NOT NULL IDENTITY(1,1),
  raceId int NOT NULL DEFAULT '0',
  driverId int NOT NULL DEFAULT '0',
  constructorId int NOT NULL DEFAULT '0',
  [number] int NOT NULL DEFAULT '0',
  position int DEFAULT NULL,
  q1 varchar(255) DEFAULT NULL,
  q2 varchar(255) DEFAULT NULL,
  q3 varchar(255) DEFAULT NULL,
  PRIMARY KEY (qualifyId),
  CONSTRAINT FK_raceId_qualifying FOREIGN KEY (raceId) REFERENCES races(raceId),
  CONSTRAINT FK_droverId_qualifying FOREIGN KEY (driverId) REFERENCES drivers(driverId),
  CONSTRAINT FK_constructorId_qualyfying FOREIGN KEY (constructorId) REFERENCES constructors(constructorId)
) 

CREATE TABLE lap_times (
  raceId int NOT NULL,
  driverId int NOT NULL,
  lap int NOT NULL,
  position int DEFAULT NULL,
  time varchar(255) DEFAULT NULL,
  milliseconds int DEFAULT NULL,
  PRIMARY KEY (raceId,driverId,lap),
  CONSTRAINT FK_raceId_lap FOREIGN KEY (raceId) REFERENCES races(raceId),
  CONSTRAINT FK_driverId_lap FOREIGN KEY (driverId) REFERENCES drivers(driverId)
)

CREATE TABLE pit_stops (
  raceId int NOT NULL IDENTITY(1,1),
  driverId int NOT NULL,
  stop int NOT NULL,
  lap int NOT NULL,
  time time NOT NULL,
  duration varchar(255) DEFAULT NULL,
  milliseconds int DEFAULT NULL,
  PRIMARY KEY (raceId,driverId,stop),
  CONSTRAINT FK_raceId_pit FOREIGN KEY (raceId) REFERENCES races(raceId),
  CONSTRAINT FK_driverId_pit FOREIGN KEY (driverId) REFERENCES drivers(driverId)
) 

CREATE TABLE seasons (
  year int NOT NULL DEFAULT '0',
  url varchar(255) NOT NULL UNIQUE DEFAULT '',
  PRIMARY KEY (year),
) 

CREATE TABLE [status] (
  statusId int NOT NULL,
  status varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (statusId)
) 

CREATE TABLE constructor_results (
  constructorResultsId int NOT NULL IDENTITY(1,1),
  raceId int NOT NULL DEFAULT '0',
  constructorId int NOT NULL DEFAULT '0',
  points float DEFAULT NULL,
  status varchar(255) DEFAULT NULL,
  PRIMARY KEY (constructorResultsId),
  CONSTRAINT FK_raceId_constructor_results FOREIGN KEY (raceId) REFERENCES races(raceId),
  CONSTRAINT FK_constructorId_constructor_results FOREIGN KEY (constructorId) REFERENCES constructors(constructorId)
) 

CREATE TABLE constructor_standings (
  constructorStandingsId int NOT NULL IDENTITY(1,1),
  raceId int NOT NULL DEFAULT '0',
  constructorId int NOT NULL DEFAULT '0',
  points float NOT NULL DEFAULT '0',
  position int DEFAULT NULL,
  positionText varchar(255) DEFAULT NULL,
  wins int NOT NULL DEFAULT '0',
  PRIMARY KEY (constructorStandingsId),
  CONSTRAINT FK_raceId_constructor_standings FOREIGN KEY (raceId) REFERENCES races(raceId),
  CONSTRAINT FK_constructorId_constructor_standings FOREIGN KEY (constructorId) REFERENCES constructors(constructorId)
) 


CREATE TABLE driver_standings (
  driverStandingsId int NOT NULL IDENTITY(1,1),
  raceId int NOT NULL DEFAULT '0',
  driverId int NOT NULL DEFAULT '0',
  points float NOT NULL DEFAULT '0',
  position int DEFAULT NULL,
  positionText varchar(255) DEFAULT NULL,
  wins int NOT NULL DEFAULT '0',
  PRIMARY KEY (driverStandingsId),
  CONSTRAINT FK_raceId_driver_standings FOREIGN KEY (raceId) REFERENCES races(raceId),
  CONSTRAINT FK_driverId_driver_standings FOREIGN KEY (driverId) REFERENCES drivers(driverId)
)


CREATE TABLE results (
  resultId int NOT NULL IDENTITY(1,1),
  raceId int NOT NULL DEFAULT '0',
  driverId int NOT NULL DEFAULT '0',
  constructorId int NOT NULL DEFAULT '0',
  number int NOT NULL DEFAULT '0',
  grid int NOT NULL DEFAULT '0',
  position int DEFAULT NULL,
  positionText varchar(255) NOT NULL DEFAULT '',
  positionOrder int NOT NULL DEFAULT '0',
  points float NOT NULL DEFAULT '0',
  laps int NOT NULL DEFAULT '0',
  time varchar(255) DEFAULT NULL,
  milliseconds int DEFAULT NULL,
  fastestLap int DEFAULT NULL,
  rank int DEFAULT '0',
  fastestLapTime varchar(255) DEFAULT NULL,
  fastestLapSpeed varchar(255) DEFAULT NULL,
  statusId int NOT NULL DEFAULT '0',
  PRIMARY KEY (resultId),
  CONSTRAINT FK_raceId_results FOREIGN KEY (raceId) REFERENCES races(raceId),
  CONSTRAINT FK_driverId_results FOREIGN KEY (driverId) REFERENCES drivers(driverId),
  CONSTRAINT FK_constructorId_results FOREIGN KEY (constructorId) REFERENCES constructors(constructorId)
) 


