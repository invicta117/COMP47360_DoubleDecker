# Dublin Bikes Data

Please first run the provided wget... command to download the data to this folder and extract the data. Please then run the following command:

    nohup python dublin_bikes_create_csv.py &> create_csv.log &

This will create two csv files trips.csv and leavetimes.csv which can be imported into the database.

Please then run the following command to create the necessary database and tables:

    mysql -u $USER -p$PASSWORD < CREATE_DATABASE.sql

Where $USER is your username for the mysql database and $PASSWORD is your password for the mysql database. This will create the database and schema.

Once this is completed the data can then be inserted into the database. This is done by running the following commands

    nohup mysql -u $USER -p$PASSWORD < INSERT_LEAVETIMES.sql &>LEAVETIMES.log &

    nohup mysql -u $USER -p$PASSWORD < INSERT_TRIPS.sql &>TRIPS.log &

This will take the data from the newly created leavetimes.csv and trips.csv an place them into the database. Please ensure to check the log files for any errors caused and delete the csv files when completed.
