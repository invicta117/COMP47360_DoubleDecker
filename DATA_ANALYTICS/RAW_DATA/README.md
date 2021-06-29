# Extracting data from database

Please execute the following command to process the data from the database into a useabale csv format for data analytics, based on the answer provided by https://stackoverflow.com/questions/356578/how-to-output-mysql-query-results-in-csv-format.

    nohup mysql -u team11 -p$PASSWORD < ./SQL/jan.sql | sed 's/\t/,/g' > dublinbus_jan.csv &

Please repeat this command for each of the monthly sql files provided in the SQL folder replacing "jan" where appropriate. Please ensure to inspect the file as any SQL output will be added to the top of the file, in particular warnings.
