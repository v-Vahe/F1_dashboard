use formula1;

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
  created_date datetime NOT NULL,
  modified_date datetime NOT NULL,
  CONSTRAINT PK_circuitId PRIMARY KEY (circuitId)
);

CREATE TABLE races (
  raceId int NOT NULL IDENTITY(1,1),
  year int NOT NULL DEFAULT '0',
  round int NOT NULL DEFAULT '0',
  circuitId tinyint NOT NULL,
  name varchar(255) NOT NULL DEFAULT '',
  date date NOT NULL,
  time time DEFAULT NULL,
  url varchar(255) DEFAULT NULL,
  fp1_date date DEFAULT NULL,
  fp1_time time DEFAULT NULL,
  fp2_date date DEFAULT NULL,
  fp2_time time DEFAULT NULL,
  fp3_date date DEFAULT NULL,
  fp3_time time DEFAULT NULL,
  quali_date date DEFAULT NULL,
  quali_time time DEFAULT NULL,
  sprint_date date DEFAULT NULL,
  sprint_time time DEFAULT NULL,
  created_date datetime NOT NULL,
  modified_date datetime NOT NULL,
  PRIMARY KEY (raceId),
  CONSTRAINT FK_circuitId_circuits FOREIGN KEY (circuitId) REFERENCES circuits(circuitId)
);

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
  created_date datetime NOT NULL,
  modified_date datetime NOT NULL,
  PRIMARY KEY (driverId),
);

CREATE TABLE constructors (
  constructorId int NOT NULL IDENTITY(1,1),
  constructorRef varchar(255) NOT NULL DEFAULT '',
  name varchar(255) NOT NULL DEFAULT '',
  nationality varchar(255) DEFAULT NULL,
  url varchar(255) DEFAULT '',
  created_date datetime NOT NULL,
  modified_date datetime NOT NULL,
  PRIMARY KEY (constructorId),
); 

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
  created_date datetime NOT NULL,
  modified_date datetime NOT NULL,
  PRIMARY KEY (qualifyId),
  CONSTRAINT FK_raceId_races_1 FOREIGN KEY (raceId) REFERENCES races(raceId),
  CONSTRAINT FK_driverId_drivers_0 FOREIGN KEY (driverId) REFERENCES drivers(driverId),
  CONSTRAINT FK_constructorId_constructors_1 FOREIGN KEY (constructorId) REFERENCES constructors(constructorId)
); 

CREATE TABLE lap_times (
  raceId int NOT NULL,
  driverId int NOT NULL,
  lap int NOT NULL,
  position int DEFAULT NULL,
  time varchar(255) DEFAULT NULL,
  milliseconds int DEFAULT NULL,
  created_date datetime NOT NULL,
  modified_date datetime NOT NULL,
  PRIMARY KEY (raceId,driverId,lap),
  CONSTRAINT FK_raceId_races_2 FOREIGN KEY (raceId) REFERENCES races(raceId),
  CONSTRAINT FK_driverId_drivers_1 FOREIGN KEY (driverId) REFERENCES drivers(driverId)
);

CREATE TABLE pit_stops (
  raceId int NOT NULL IDENTITY(1,1),
  driverId int NOT NULL,
  stop int NOT NULL,
  lap int NOT NULL,
  time time NOT NULL,
  duration varchar(255) DEFAULT NULL,
  milliseconds int DEFAULT NULL,
  created_date datetime NOT NULL,
  modified_date datetime NOT NULL,
  PRIMARY KEY (raceId,driverId,stop),
  CONSTRAINT FK_raceId_races_3 FOREIGN KEY (raceId) REFERENCES races(raceId),
  CONSTRAINT FK_driverId_drivers_2 FOREIGN KEY (driverId) REFERENCES drivers(driverId)
);

CREATE TABLE seasons (
  [year] int NOT NULL DEFAULT '0',
  url varchar(255) NOT NULL UNIQUE DEFAULT '',
  created_date datetime NOT NULL,
  modified_date datetime NOT NULL,
  PRIMARY KEY (year),
);

CREATE TABLE [status] (
  statusId int NOT NULL,
  status varchar(255) NOT NULL DEFAULT '',
  created_date datetime NOT NULL,
  modified_date datetime NOT NULL,
  PRIMARY KEY (statusId)
); 

CREATE TABLE constructor_results (
  constructorResultsId int NOT NULL IDENTITY(1,1),
  raceId int NOT NULL DEFAULT '0',
  constructorId int NOT NULL DEFAULT '0',
  points float DEFAULT NULL,
  status varchar(255) DEFAULT NULL,
  created_date datetime NOT NULL,
  modified_date datetime NOT NULL,
  PRIMARY KEY (constructorResultsId),
  CONSTRAINT FK_raceId_races_4 FOREIGN KEY (raceId) REFERENCES races(raceId),
  CONSTRAINT FK_constructorId_constructors_2 FOREIGN KEY (constructorId) REFERENCES constructors(constructorId)
); 

CREATE TABLE constructor_standings (
  constructorStandingsId int NOT NULL IDENTITY(1,1),
  raceId int NOT NULL DEFAULT '0',
  constructorId int NOT NULL DEFAULT '0',
  points float NOT NULL DEFAULT '0',
  position int DEFAULT NULL,
  positionText varchar(255) DEFAULT NULL,
  wins int NOT NULL DEFAULT '0',
  created_date datetime NOT NULL,
  modified_date datetime NOT NULL,
  PRIMARY KEY (constructorStandingsId),
  CONSTRAINT FK_raceId_races_5 FOREIGN KEY (raceId) REFERENCES races(raceId),
  CONSTRAINT FK_constructorId_constructors_3 FOREIGN KEY (constructorId) REFERENCES constructors(constructorId)
); 


CREATE TABLE driver_standings (
  driverStandingsId int NOT NULL IDENTITY(1,1),
  raceId int NOT NULL DEFAULT '0',
  driverId int NOT NULL DEFAULT '0',
  points float NOT NULL DEFAULT '0',
  position int DEFAULT NULL,
  positionText varchar(255) DEFAULT NULL,
  wins int NOT NULL DEFAULT '0',
  created_date datetime NOT NULL,
  modified_date datetime NOT NULL,
  PRIMARY KEY (driverStandingsId),
  CONSTRAINT FK_raceId_races_6 FOREIGN KEY (raceId) REFERENCES races(raceId),
  CONSTRAINT FK_driverId_drivers_3 FOREIGN KEY (driverId) REFERENCES drivers(driverId)
);


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
  created_date datetime NOT NULL,
  modified_date datetime NOT NULL,
  PRIMARY KEY (resultId),
  CONSTRAINT FK_raceId_races_7 FOREIGN KEY (raceId) REFERENCES races(raceId),
  CONSTRAINT FK_driverId_drivers_4 FOREIGN KEY (driverId) REFERENCES drivers(driverId),
  CONSTRAINT FK_constructorId_constructors_4 FOREIGN KEY (constructorId) REFERENCES constructors(constructorId)
); 


