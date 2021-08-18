Please create a new user for the application to use, this can be done using the following commands replacing 'yourpasswordhere' with your own password

  CREATE USER 'student'@'localhost' IDENTIFIED BY 'yourpasswordhere';

  GRANT ALL PRIVILEGES ON * . * TO 'student'@'localhost';

Please ensure that you save this password as an enviroment variable DBPASS

  export DBPASS='yourpasswordhere'
 
