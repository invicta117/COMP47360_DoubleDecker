SELECT t.DayOfService, t.TripID, t.LineId, t.Direction, t.PlannedTime_Arr as TPlannedTime_Arr, t.PlannedTime_Dep as TPlannedTime_Dep, t.ActualTime_Arr as TActualTime_Arr, t.ActualTime_Dep as TActualTime_Dep, l.progrnumber, l.stoppointid, l.plannedtime_arr as Lplannedtime_arr, l.plannedtime_dep as Lplannedtime_dep, l.actualtime_arr as Lactualtime_arr, l.actualtime_dep as Lactualtime_dep, l.vehicleid, l.lastupdate FROM team11.rt_leavetimes l, team11.rt_trips t
where t.tripid = l.tripid and t.dayofservice = l.dayofservice and t.dayofservice < "2018-02-01"; 