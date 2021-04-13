import csv
import openpyxl
import re

#Converts a list to dictionary
def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

def meeting_data_parser(meeting_file, start_line):

    #meeting attendance
    meeting_data = []

    with open(meeting_file , newline = '', encoding = 'utf-16') as meeting_attendance:
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



#COMPARE THE 2 ATTENDANCE DATA SETS
def main():


    meeting_attendance_file = input("what is the file name of the meeting attendance: ")

    powerschool_roster_file = input("what is the file name of the powerschool roster report: ")

    while True:
        start_line = input("In the meeting attendance file, which row includes the header (FULL NAME) line 1 or 6?: ")

        if start_line == '1' or start_line == '6':
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

main()