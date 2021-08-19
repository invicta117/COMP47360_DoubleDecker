CREATE DATABASE gtfs;

USE gtfs;

CREATE TABLE `calendar` (
	  `service_id` varchar(20) DEFAULT NULL,
	  `monday` int DEFAULT NULL,
	  `tuesday` int DEFAULT NULL,
	  `wednesday` int DEFAULT NULL,
	  `thursday` int DEFAULT NULL,
	  `friday` int DEFAULT NULL,
	  `saturday` int DEFAULT NULL,
	  `sunday` int DEFAULT NULL,
	  `start_date` varchar(20) DEFAULT NULL,
	  `end_date` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `calendar_dates` (
	  `service_id` varchar(10) DEFAULT NULL,
	  `date` varchar(10) DEFAULT NULL,
	  `exception_type` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `routes` (
	  `route_id` varchar(30) DEFAULT NULL,
	  `agency_id` varchar(10) DEFAULT NULL,
	  `route_short_name` varchar(10) DEFAULT NULL,
	  `route_long_name` varchar(255) DEFAULT NULL,
	  `route_type` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `shapes` (
	  `shape_id` varchar(30) DEFAULT NULL,
	  `shape_pt_lat` double DEFAULT NULL,
	  `shape_pt_lon` double DEFAULT NULL,
	  `shape_pt_sequence` smallint DEFAULT NULL,
	  `shape_dist_traveled` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `stop_times` (
	  `trip_id` varchar(60) DEFAULT NULL,
	  `arrival_time` time DEFAULT NULL,
	  `departure_time` time DEFAULT NULL,
	  `stop_id` varchar(30) DEFAULT NULL,
	  `stop_sequence` smallint DEFAULT NULL,
	  `stop_headsign` varchar(255) DEFAULT NULL,
	  `pickup_type` int DEFAULT NULL,
	  `drop_off_type` int DEFAULT NULL,
	  `shape_dist_traveled` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `stops` (
	  `stop_id` varchar(30) DEFAULT NULL,
	  `stop_name` varchar(255) DEFAULT NULL,
	  `stop_lat` double DEFAULT NULL,
	  `stop_long` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `trips` (
	  `route_id` varchar(30) DEFAULT NULL,
	  `service_id` varchar(30) DEFAULT NULL,
	  `trip_id` varchar(60) DEFAULT NULL,
	  `shape_id` varchar(30) DEFAULT NULL,
	  `trip_headsign` varchar(255) DEFAULT NULL,
	  `direction_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `weather` (
	  `lat` float DEFAULT NULL,
	  `lon` float DEFAULT NULL,
	  `timezone` varchar(128) DEFAULT NULL,
	  `current` datetime NOT NULL,
	  `weather_id` int NOT NULL,
	  `weather_icon` varchar(10) DEFAULT NULL,
	  `visibility` float DEFAULT NULL,
	  `wind_speed` float DEFAULT NULL,
	  `wind_deg` float DEFAULT NULL,
	  `wind_gust` float DEFAULT NULL,
	  `temperature` float DEFAULT NULL,
	  `feels_like` float DEFAULT NULL,
	  `temp_min` float DEFAULT NULL,
	  `temp_max` float DEFAULT NULL,
	  `pressure` float DEFAULT NULL,
	  `humidity` float DEFAULT NULL,
	  `rain_1h` float DEFAULT NULL,
	  `snow_1h` float DEFAULT NULL,
	  `sunrise` datetime DEFAULT NULL,
	  `sunset` datetime DEFAULT NULL,
	  `description` varchar(100) DEFAULT NULL,
	  PRIMARY KEY (`current`,`weather_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
