CREATE DATABASE IF NOT EXISTS `gtfs`;

USE gtfs;

DROP TABLE IF EXISTS calendar;

CREATE TABLE `calendar`
(
  `service_id` varchar(20) PRIMARY KEY,
  `monday` int,
  `tuesday` int,
  `wednesday` int,
  `thursday` int,
  `friday` int,
  `saturday` int,
  `sunday` int,
  `start_date` varchar(20),
  `end_date` varchar(20)
);

DROP TABLE IF EXISTS calendar_dates;

CREATE TABLE `calendar_dates`
(
  `service_id` varchar(10),
  `date` varchar(10),
  `exception_type` int,
  CONSTRAINT pk_calendar_dates PRIMARY KEY(`service_id`, `date`)
);

DROP TABLE IF EXISTS routes;

CREATE TABLE `routes`
(
  `route_id` varchar(30) PRIMARY KEY,
  `agency_id` varchar(10),
  `route_short_name` varchar(10),
  `route_long_name` varchar(255),
  `route_type` int
);

DROP TABLE IF EXISTS shapes;

CREATE TABLE `shapes`
(
  `shape_id` varchar(30),
  `shape_pt_lat` double,
  `shape_pt_lon` double,
  `shape_pt_sequence` smallint,
  `shape_dist_traveled` double,
  CONSTRAINT pk_shapes PRIMARY KEY(`shape_id`, `shape_pt_sequence`)
);

DROP TABLE IF EXISTS stop_times;

CREATE TABLE `stop_times`
(
  `trip_id` varchar(60),
  `arrival_time` time,
  `departure_time` time,
  `stop_id` varchar(30),
  `stop_sequence` smallint,
  `stop_headsign` varchar(255),
  `pickup_type` int,
  `drop_off_type` int,
  `shape_dist_traveled` double,
  CONSTRAINT pk_stop_times PRIMARY KEY(`trip_id`, `arrival_time`, `stop_id`)
);

DROP TABLE IF EXISTS stops;

CREATE TABLE `stops`
(
  `stop_id` varchar(30),
  `stop_name` varchar(255),
  `stop_lat` double,
  `stop_long` double,
  CONSTRAINT pk_stops PRIMARY KEY(`stop_id`, `stop_name`)
);

DROP TABLE IF EXISTS trips;

CREATE TABLE `trips`
(
  `route_id` varchar(30),
  `service_id` varchar(30),
  `trip_id` varchar(60) PRIMARY KEY,
  `shape_id` varchar(30),
  `trip_headsign` varchar(255),
  `direction_id` int
);

ALTER TABLE `calendar_dates` ADD FOREIGN KEY (`service_id`) REFERENCES `calendar` (`service_id`);

ALTER TABLE `stop_times` ADD FOREIGN KEY (`stop_id`) REFERENCES `stops` (`stop_id`);

ALTER TABLE `trips` ADD FOREIGN KEY (`route_id`) REFERENCES `routes` (`route_id`);

ALTER TABLE `trips` ADD FOREIGN KEY (`service_id`) REFERENCES `calendar` (`service_id`);

ALTER TABLE `trips` ADD FOREIGN KEY (`shape_id`) REFERENCES `shapes` (`shape_id`);

ALTER TABLE `stop_times` ADD FOREIGN KEY (`trip_id`) REFERENCES `trips` (`trip_id`);
