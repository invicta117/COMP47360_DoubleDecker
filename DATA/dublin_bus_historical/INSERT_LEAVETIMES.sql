LOAD DATA LOCAL INFILE "leavetimes.csv" INTO TABLE team11.rt_leavetimes
FIELDS TERMINATED BY ","
ENCLOSED BY "'"
LINES TERMINATED BY '\n';