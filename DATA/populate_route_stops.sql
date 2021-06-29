insert into gtfs.route_stops
SELECT distinct stops.stop_name, stops.stop_lat, stops.stop_lon, routes.route_short_name FROM gtfs.routes, gtfs.trips, gtfs.stop_times, gtfs.stops
where routes.route_id = trips.route_id AND trips.trip_id = stop_times.trip_id and stop_times.stop_id = stops.stop_id;