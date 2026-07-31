# Dashboard-meet-je-stad

This project requires mysql.\
Copy .env.example to .env and .env.test and fill in the blanks.\
Specify the start of the measurements in START_DATE.\
END_DATE should be empty and gets filled when the update_dataset command is executed.\
The LAST_SENSOR_ID should be set to the newest sensor.\
Make a virtual env and run pip install -r requirements.\
Make the database.\
Run the migrations.\
Run the update_dataset command.\
Register and make the user a staff user to see the full site.\
Run run-tests.sh to test the site.\
To update the site on the server execute the update.sh script.
