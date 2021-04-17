import os
import requests
import urllib.parse
import csv
import openpyxl
import re

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

#Converts a list to dictionary
def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

def meeting_data_parser(meeting_file, start_line):

    #meeting attendance
    meeting_data = []
    path = "C:/Users/joelb/OneDrive/Documents/GitHub/attendanceHelper/static/%s" % meeting_file
    with open( path , newline = '', encoding = 'utf-16') as meeting_attendance:
        if int(start_line) == 6:
            for i in range(int(start_line)):
                next(meeting_attendance)

        reader = csv.DictReader(meeting_attendance, delimiter = '\t')

        for row in reader:
            meeting_data.append(row)

    meeting_names_and_numbers = []
    for i in range(len(meeting_data)):
        meeting_names_and_numbers.append(meeting_data[i]['Full Name'])

    #covert names list into a big string to perferm regex on
    names_numbers_conglomerate = "\n".join(meeting_names_and_numbers)

    studentID_in_meeting = re.findall(r'[1-9]\w+', names_numbers_conglomerate)

    return studentID_in_meeting


def powerschool_data_parser(roster_file):
    #Powerschool Roster
    workbook = openpyxl.load_workbook(roster_file)

    worksheet = workbook["Student Roster Report"]

    #load names and numbers into list
    pschool = []
    for row in worksheet.values:

        for value in row:
            if value != '':
                pschool.append(value)

    #convert list into dictionary
    pschool_dict = Convert(pschool)

    return pschool_dict
