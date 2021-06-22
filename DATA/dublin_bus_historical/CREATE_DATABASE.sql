CREATE DATABASE IF NOT exists team11;

CREATE TABLE if not exists team11.rt_trips (
    TripID int,
    DataSource varchar(255),
    DayOfService datetime,
    LineId varchar(255),
    RouteId varchar(255),
    Direction boolean,
    PlannedTime_Arr int,
    PlannedTime_Dep int,
    ActualTime_Arr int,
    ActualTime_Dep int,
    Basin varchar(225),
    TenderLot varchar(225),
    Suppressed varchar(225),
    JustificationId int,
    LastUpdate datetime,
    Note varchar(225)
);

CREATE TABLE if not exists team11.rt_leavetimes (
datasource varchar(225),
dayofservice datetime,
tripid int,
progrnumber int,
stoppointid int,
plannedtime_arr int,
plannedtime_dep int,
actualtime_arr int,
actualtime_dep int,
vehicleid int,
passengers int,
passengersin int,
passengersout int,
distance varchar(225),
suppressed varchar(225),
justificationid int,
lastupdate datetime,
note varchar(225)
);