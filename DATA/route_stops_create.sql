CREATE TABLE gtfs.route_stops (
stop_name varchar(255), 
stop_lat float, 
stop_lon float, 
route_short_name varchar(225),
PRIMARY KEY (`stop_name`,`route_short_name`)
); 