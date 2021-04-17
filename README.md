# attendanceHelper
#### Video 
Demo: https://youtu.be/J1OFyyqdTGA
#### Description:
Final Project for CS50 GitHub Repo: https://github.com/JoelBiere/attendanceHelper


### app.py
is the controller for the webapp managing routes through the flask.
The app controls where uploaded files are stored, the app relies on knowing the file locations of these stored files.
Directories are set up to run with a Heroku server.

The main program is takeAttendance() which reads the data uploaded from a meeting file .csv file and measures it against the rosters loaded from the database in the session.

### helpers.py
A key part of the file is:

meeting_data_parser(meeting_file, start_line):

-this parses the data using the .csv file functions built in to python. Ultimately, the data needed is a list of strings of the student id numbers. These will be measured against the student numbers from the student roster files.

powerschool_data_parser(roster_file):

-this parses data from a .xlxs file using openpyxl modules. This data is loaded into a SQLite database.

get_current_roster():

-this function loads the most recent iteration of the user's rosters found in the database.

### attendanceHelper.db
is a SQLite3 database with 2 tables. The schema for which is below.

TABLE'users' ('id' integer PRIMARY KEY AUTOINCREMENT NOT NULL,
              'username' text NOT NULL,
              'hash' text NOT NULL);

TABLE "rosters" (
        "teacher_id"    INTEGER,
        "teacher_username"      TEXT NOT NULL,
        "class_name"    TEXT NOT NULL,
        "student_name"  TEXT NOT NULL,
        "student_id"    TEXT NOT NULL
);



### index.html
is a homepage that loads up the users current rosters and loads it to the flask_session as a large dictionary

### uploadMeeting.html
is where teacher load there .csv files from their TEAMS meeting to check against there rosters in the sqlite db

### attendanceDisplay.html
shows 2 tables, one which displays present students the other absent.

### addRoster.html
displays the current rosters in the db and also offers user manipulation of that db with add and delete roster functionality.


### TODO (known issues)

in the future, there should be options for users to manipulate the table based on individual student rather than only being limited to uploading whole excel files


--if a teacher downloads the meeting attendance after the meeting has conlcuded--the format of the .csv file changes
        the data the program reads into memory would then start on line 6 of the csv--not line 1
            -currently the start_line variable is hard coded to 1
