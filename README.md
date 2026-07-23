# Dashboard-meet-je-stad

This project requires postgres and pgAdmin 4.
Copy .env.example to .env and .env.test and fill in the blanks. Specify the start of the measurements in START_DATE. 
END_DATE should be empty and gets filled when the update_dataset command is executed.
The LAST_SENSOR_ID should be set to the newest sensor.
Make the database.
Run the migrations.
Run the update_dataset command.
Register and make the user a superuser to see the full site.

To update the site on the server execute the update.sh script.
