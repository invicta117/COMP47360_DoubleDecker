import pandas as pd
import json

stop_times = pd.read_csv("../DATA_ANALYTICS/RAW_DATA/gtfs/stop_times.txt", delimiter=",")
stops = pd.read_csv("../DATA_ANALYTICS/RAW_DATA/gtfs/stops.txt", delimiter=",")
routes = pd.read_csv("../DATA_ANALYTICS/RAW_DATA/gtfs/routes.txt", delimiter=",")
trips = pd.read_csv("../DATA_ANALYTICS/RAW_DATA/gtfs/trips.txt", delimiter=",")
calendar = pd.read_csv("../DATA_ANALYTICS/RAW_DATA/gtfs/calendar.txt", delimiter=",")
stop_times["arrival_time"] = pd.to_timedelta(stop_times["arrival_time"])


def explore(day, bus_route):
    day = day.lower()
    bus_route = bus_route.lower()

    def trips_day(day):
        """Get all trips for that day"""
        days = list(calendar[calendar[day] == 1]["service_id"].values)
        day_trips = set(trips[trips["service_id"].isin(days)]["trip_id"].values)
        return day_trips

    def trips_route(bus_route):
        """Get all the trips for that route"""
        route_trips = set(
            trips[trips["route_id"].isin(list(routes[routes["route_short_name"] == bus_route]["route_id"].values))][
                "trip_id"].values)
        return route_trips

    def station_to_station_explore(tripid):
        seq = stop_times[stop_times["trip_id"] == tripid][["stop_id", "stop_sequence", "departure_time"]].sort_values(
            by="stop_sequence")
        final = seq.merge(stops, how='left', on='stop_id')
        return final[["stop_lat", "stop_lon", "departure_time"]].iloc[[0, -1]]

    r = trips_day(day).intersection(trips_route(bus_route))  # get intersection of trips for that route and day
    trip = r.pop()
    result = station_to_station_explore(trip).to_json(orient="records")
    parsed = json.loads(result)
    return parsed
