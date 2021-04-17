import os
import openpyxl
import gunicorn

from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory
from werkzeug.utils import secure_filename
from helpers import apology, login_required, Convert, meeting_data_parser, powerschool_data_parser
from cs50 import SQL
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash 
from tempfile import mkdtemp
from flask_session import Session




#this path is the folder for the HEROKU server
UPLOAD_FOLDER = "/app/.heroku/python/bin:/usr/local/bin:/usr/bin:/bin"
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

app = Flask(__name__)

#designate upload foler for roster files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///attendanceHelper.db")


def allowed_file(filename):
    return'.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET'])
@login_required
def home_page():
    if request.method == "GET":

        name = session.get('username')
        return render_template('index.html', name = name)

@app.route('/uploader', methods = ["POST"])
@login_required
def uploading_meeting_file():
        if request.method == 'POST':
        #check if the post request has the file part
            if 'file' not in request.files:
                flash('No File part')
                return "File not in request.files" #redirect(request.url)

            file = request.files['file']

            #if user does not select file, browser also submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                session['meetingFile'] = filename

<<<<<<< HEAD
                return redirect("/attendanceDisplay")
=======
                start_line = 1 # this is hard coded for right now

                #this is a list of student ID's who attended the meeting
                studentID_in_meeting = meeting_data_parser(filename,start_line)

                print(studentID_in_meeting)

######THIS IS WHERE I LEFT OFF------CHANGE THIS FUNCTION SO IT DOESN"T RELY ON PULLING FROM ROSTER FILE---BUT INSTEAD FROM THE DICT in SESSION
                #this is a dict. Keys are student names, values are student ID's
                total_roster = session.get('total_roster')
                class_name = request.form.get('class_name')

                #{'Period 7': [{'student_name': 'Alexander, Joyce', 'student_id': '229391'}, {'student_name': 'Austin, Leroy', 'student_id': '225913'}, {'student_name': 'Bankston, Latayvon', 'student_id': '235369'},
                class_roster = total_roster[class_name]

                student_names = []
                student_numbers = []
            
                for item in class_roster:
                    student_names.append(item['student_name'])
                    student_numbers.append(item['student_id'])

                student_roster = {}
                for i in range(len(student_names)):
                    student_roster[student_names[i]] = student_numbers[i]

                print(student_roster)


                # compare the 2 sets of data to produce a list of names present and a list of names absent
                student_numbers_present = []
                student_names_present = []
            


##### GET STUDENT_ROSTER TO BE A DICT WHERE KEY IS STUDENT NAMES AND VALUES ARE STUDENT NUMBERS
                for key in student_roster:

                    for j in range(len(studentID_in_meeting)):

                        #if the student number in the roster matches the student number in the meeting
                        if student_roster[key] == studentID_in_meeting[j]:
                            print(f"{student_roster[key]} matches {studentID_in_meeting[j]}")

                            #this gets the key--which is the student name-- from the value -- which is the student number.
                            student_names_present.append(list(student_roster.keys())[list(student_roster.values()).index(studentID_in_meeting[j])])

                            student_numbers_present.append(student_roster[key])


                print(f"Present student ID's --> {student_numbers_present}")
                print(f"Present students --> {student_names_present}")

                #get list of of names in roster
                student_roster_names = student_roster.keys()

                students_absent = list(set(student_roster_names) - set(student_names_present))
                
                students_absent.sort()
                if "Name" in students_absent:
                    students_absent.remove("Name")

                for student in students_absent:
                    print(f"Absent-->{student}")
>>>>>>> parent of 2a1731f (Design Improvements & Bug fixes)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



#LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = request.form.get("username")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method== "POST":
        username = request.form.get('username')

        password = request.form.get('password')

        confirmation = request.form.get('confirmation')

        username_query = db.execute("SELECT * FROM users")

        print(username_query)

        username_list = []

        for i in range(len(username_query)):
            username_list.append(username_query[i]["username"])

        print(username_list)

        if not request.form.get('username'):
            return apology("Must provide username")

        if username in username_list:
            return apology("Username already taken")

        if not request.form.get('password') or not request.form.get('confirmation'):
            return apology("Password field cannot be blank")

        if password != confirmation:
            return apology("Passwords do not match")

        db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, generate_password_hash(password))

        return redirect("/login")

    if request.method == "GET":

        return render_template('register.html')

#LOGOUT
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/uploadMeeting")
@login_required

#display file uploader
def meetingUploader():
    if request.method == "GET":
        return render_template("uploadMeeting.html")




@app.route("/rosterManagement", methods = ["GET", "POST"])
@login_required
def rosterManagement():

    if request.method == "GET":
        
        # TODO detect current rosters in database and display them
<<<<<<< HEAD

        teacher_id = session.get("user_id")

=======
>>>>>>> parent of 2a1731f (Design Improvements & Bug fixes)
        total_roster = get_current_roster()
        list_of_class_names = session.get('list_of_class_names')
        class_size = session.get('class_size')


        class_list = db.execute(" SELECT DISTINCT class_name FROM rosters WHERE teacher_id = ?", teacher_id)
        # [{'class_name':'Period 8'}, {'class_name':'Period 7}, {} , {}]   ----DB.EXECUTE RETURNS A LIST OF DICTIONARIES WHERE THE KEY IS THE FIELD AND VALUE IS VALUE
        
        #convert list of dicts into list of all the values
       
        list_of_class_names = []
        for i in range(len(class_list)):
            list_of_class_names.append(class_list[i]['class_name'])
            
        print(list_of_class_names)
        #['Period 8', 'Period 7']
       
        # what I want
        # list of dicts where each dict is the entire roster of one of the classes in class_list
        total_roster = {}
        class_size = {}
        for class_name in list_of_class_names:
            total_roster[class_name] = db.execute(" SELECT DISTINCT student_name, student_id FROM rosters WHERE teacher_id = ? AND class_name = ? ", teacher_id, class_name)
            print(f"{class_name} has {len(total_roster[class_name])} students ")
            class_size[class_name] = len(total_roster[class_name])
        return render_template("rosterManagement.html", list_of_class_names = list_of_class_names, total_roster = total_roster, class_size = class_size)

    if request.method == "POST":
        #should get passed the roster file
        #check if the post request has the file part
        if 'rosterFile' not in request.files:
            flash('No File part')
            return "File not in request.files" #redirect(request.url)

        file = request.files['rosterFile']

        #if user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            print(filename)
            # TODO add file data to SQL data base
            path = ("/app/.heroku/python/bin:/usr/local/bin:/usr/bin:/bin%s" % filename)
            workbook = openpyxl.load_workbook(path)
            worksheet = workbook ["Student Roster Report"]

            #load names and numbers into a dict
            pschool = []
            for row in worksheet.values:
                for value in row:
                    if value != '':
                        pschool.append(value)
            #first 2 elements are ["name", "Id"] so remove those
            pschool.pop(0)
            pschool.pop(0)

            pschool_dict = Convert(pschool)
            print(pschool)
            print(pschool_dict)
            #seed this into the database
            class_name = request.form.get("className")
            for key in pschool_dict:
                db.execute("INSERT INTO rosters (teacher_id, teacher_username, class_name, student_name, student_id) VALUES (?, ?, ?, ?, ?)", session.get("user_id"), session.get("username"), class_name, key, pschool_dict[key] )
                print(F" teacher_id -->{session.get('user_id')} teacher_username--> {session.get('username')} class_name ---> {class_name} student_name --> {key} student_id-->{pschool_dict[key]} ")
            
            message = "Roster Added Successfully!"
            flash(message)
            return redirect("/rosterManagement")

@app.route("/addRoster")
@login_required
def addRoster():
    if request.method =="GET":
        return render_template("addRoster.html")



@app.route("/attendanceDisplay")
@login_required
#COMPARE THE 2 ATTENDANCE DATA SETS
def takeAttendance():

    if request.method == "GET":

        meeting_attendance_file = session.get('meetingFile')

        powerschool_roster_file = 'studentRosterReport (2).xlsx' #this is hardcoded for right now

        while True:
            start_line = 1 # this is hard coded for right now

            if start_line == 1 or start_line == 6:
                break

        #this is a list of student ID's who attended the meeting
        studentID_in_meeting = meeting_data_parser(meeting_attendance_file,start_line)

        #this is a dict. Keys are student names, values are student ID's
        student_roster = powerschool_data_parser(powerschool_roster_file)

        # compare the 2 sets of data to produce a list of names present and a list of names absent
        student_numbers_present = []
        student_names_present = []

        for key in student_roster:

            for j in range(len(studentID_in_meeting)):

                #if the student number in the roster matches the student number in the meeting
                if student_roster[key] == studentID_in_meeting[j]:
                    print(f"{student_roster[key]} matches {studentID_in_meeting[j]}")

                    #this gets the key--which is the student name-- from the value -- which is the student number.
                    student_names_present.append(list(student_roster.keys())[list(student_roster.values()).index(studentID_in_meeting[j])])

                    student_numbers_present.append(student_roster[key])


        print(f"Present student ID's --> {student_numbers_present}")
        print(f"Present students --> {student_names_present}")

        #get list of of names in roster
        student_roster_names = student_roster.keys()

        students_absent = list(set(student_roster_names) - set(student_names_present))
        students_absent.remove("Name")

        for student in students_absent:
            print(f"Absent-->{student}")

        num_of_absents = len(students_absent)

        return render_template('attendanceDisplay.html', num_of_absents = num_of_absents, students_absent = students_absent)
