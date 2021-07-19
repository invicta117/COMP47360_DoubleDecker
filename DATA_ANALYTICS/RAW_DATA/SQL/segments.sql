SELECT trip_id, arrival_time, departure_time, stop_sequence, stop_name, stop_lat, stop_lon FROM gtfs.stop_times st, gtfs.stops s
where s.stop_id = st.stop_id order by trip_id, stop_sequence;