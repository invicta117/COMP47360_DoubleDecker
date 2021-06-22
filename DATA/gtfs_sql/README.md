1. Log into server and naviagte to gtfs directory.
2. Download gtfs static data into the directory with 'wget' at https://www.transportforireland.ie/transitData/PT_Data.html.
3. Run:
``` mysql -u USER -pPASSWORD < create_db.sql``` 

4. Set the global variables by using this command:
```mysql> SET GLOBAL local_infile=1;```
`` Query OK, 0 rows affected (0.00 sec)``

5. quit current server:
```mysql> quit```
``Bye``

6. connect to the server with local-infile system variable :
```mysql --local-infile=1 -u USER -pPASSWORD```

7. run the following commands to load the .txt files to your db:
```
mysql> LOAD DATA LOCAL INFILE 'calendar.txt' INTO TABLE calendar FIELDS TERMINATED BY ','  ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES; 

mysql> LOAD DATA LOCAL INFILE 'calendar_dates.txt' INTO TABLE calendar_dates FIELDS TERMINATED BY ','  ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES;

mysql> LOAD DATA LOCAL INFILE 'routes.txt' INTO TABLE routes FIELDS TERMINATED BY ','  ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES;

mysql> LOAD DATA LOCAL INFILE 'trips.txt' INTO TABLE trips FIELDS TERMINATED BY ','  ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES;

mysql> LOAD DATA LOCAL INFILE 'stops.txt' INTO TABLE stops FIELDS TERMINATED BY ','  ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES;

mysql> LOAD DATA LOCAL INFILE 'shapes.txt' INTO TABLE shapes FIELDS TERMINATED BY ','  ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES;

mysql> LOAD DATA LOCAL INFILE 'stop_times.txt' INTO TABLE stop_times FIELDS TERMINATED BY ','  ENCLOSED BY '"'  LINES TERMINATED BY '\n' IGNORE 1 LINES;
```
