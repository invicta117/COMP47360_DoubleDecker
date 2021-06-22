This scraper uses the open weather maps one call API: https://openweathermap.org/api/one-call-api

Please create the weather database by running the following command

    mysql -u $USER -p$PASSWORD < CREATE_WEATHER_DATABASE.sql

In this database -1 hr represents the current weather, 0 represents the open weather maps weather forcast for the current hour, hr 1 for current hour + 1 hour etc. This allows for easy identification of times in the future. Another reason for doing this was to allow update statements to be used rather than insert to ensure that the database does not grow when more and more data is added. As we do not need historical weather data this means we only need to store current and future weather forcast.

Finally the following command is run to scrape the data every 15 mins:

    nohup python scraper.py &> scraper.log &

Please check the scraper.log file periodically for error messages and other information on how the scraper is running.