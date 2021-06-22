Please download the historical weather data using the following command

    wget https://cli.fusio.net/cli/climate_data/webdata/hly175.zip

To extract the file please run the following to extract the data

    unzip hly175.zip -d hly175

The database for the data can be created by running the following

    mysql -u $USER -p$PASSWORD < CREATE_DATABASE.sql

Where $USER is your username for the mysql database and $PASSWORD is your password for the mysql database. This will create the database and schema for the weather data.

To create a formatted csv that can be put into the database run the following:

    python weather_create_csv.py

This will create the file weather.csv in the current directory.

To place the data into the database run the following

    mysql -u $USER -p$PASSWORD < INSERT_WEATHER.sql
