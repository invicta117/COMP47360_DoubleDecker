# Set up

Please create a new user for the application to use, this can be done using the following commands replacing 'yourpasswordhere' with your own password

    CREATE USER 'student'@'localhost' IDENTIFIED BY 'yourpasswordhere';

    GRANT ALL PRIVILEGES ON * . * TO 'student'@'localhost';

Please ensure that you save this password as an enviroment variable DBPASS

    export DBPASS='yourpasswordhere'
 
If you wish to run the django server please create the necessary database by running

    mysql -u student -p$DBPASS < create_django_db.sql
    
