from crypt import methods
from distutils.log import debug
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

db_connection = db.connect_to_database()
app = Flask(__name__)

# Routes


@app.route('/')
def root():
    return render_template("home.j2")


@app.route('/students', methods=['POST', 'GET'])
def students():

    db_connection.ping(True)  # ping to avoid timeout

    # Insert Student
    if request.method == 'POST':
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        phone = request.form["phone"]
        aline1 = request.form["aline1"]
        aline2 = request.form["aline2"]
        city = request.form["city"]
        state = request.form["state"]
        postal = request.form["postal"]
        major = request.form["major"]
        advisor = request.form["advisor"]

        query = """
            INSERT INTO Students 
            (first_name, last_name, school_email, 
            phone_number, address_line1, address_line2, 
            city, state, postal_code, major_id, advisor_id) 
            VALUES 
            (%s, %s, %s, %s, %s, NULLIF(%s, ''), %s, %s, %s, NULLIF(%s, 'NULL'), %s)
            """
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(
            fname, lname, email, phone, aline1, aline2, city, state, postal, major, advisor))

        return redirect('/students')

    # Populate Students table
    query = '''
    SELECT Students.student_id AS "ID", Students.first_name AS First, Students.last_name AS Last, 
    Students.school_email AS Email, Students.phone_number AS Phone, 
    Students.address_line1 AS "Address Line 1", Students.address_line2 AS "Address Line 2", 
    Students.city AS City, Students.state AS State, Students.postal_code AS "Postal Code", 
    Majors.title AS Major, 
    CONCAT(Advisors.first_name, ' ', Advisors.last_name) AS Advisor
    FROM Students 
    INNER JOIN Advisors ON Students.advisor_id = Advisors.advisor_id
    LEFT JOIN Majors ON Students.major_id = Majors.major_id
    ORDER BY ID;
    '''
    cursor = db.execute_query(db_connection=db_connection, query=query)
    students = cursor.fetchall()

    # Populate Majors dropdown
    query2 = 'SELECT major_id, title FROM Majors;'
    cursor = db.execute_query(db_connection=db_connection, query=query2)
    majors = cursor.fetchall()

    # Populate Advisors dropdown
    query3 = "SELECT advisor_id, CONCAT(first_name, ' ', last_name) AS Advisor FROM Advisors;"
    cursor = db.execute_query(db_connection=db_connection, query=query3)
    advisors = cursor.fetchall()

    # Sends the results back to the web browser.
    return render_template("students.j2", students=students, majors=majors, advisors=advisors)


@app.route('/majors', methods=['POST', 'GET'])
def majors():

    db_connection.ping(True)  # ping to avoid timeout

    # Insert Major
    if request.method == "POST":
        majorid = request.form["majorid"]
        title = request.form["title"]

        query = '''
        INSERT INTO Majors 
        (major_id, title) 
        VALUES 
        (%s, %s)
        '''
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(
            majorid, title))

        return redirect('/majors')

    # Populate Majors table
    query = '''
    SELECT major_id AS "Major ID", title AS Title FROM Majors
    '''
    cursor = db.execute_query(db_connection=db_connection, query=query)
    majors = cursor.fetchall()

    return render_template("majors.j2", majors=majors)


@app.route('/advisors', methods=['POST', 'GET'])
def advisors():

    db_connection.ping(True)  # ping to avoid timeout

    # Insert Advisor
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        phone = request.form["phone"]
        aline1 = request.form["aline1"]
        aline2 = request.form["aline2"]
        city = request.form["city"]
        state = request.form["state"]
        postal = request.form["postal"]

        query = '''
        INSERT INTO Advisors 
        (first_name, last_name, school_email, 
        phone_number, address_line1, address_line2, 
        city, state, postal_code) 
        VALUES 
        (%s, %s, %s, %s, %s,  NULLIF(%s, ''), %s, %s, %s)
        '''
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(
            fname, lname, email, phone, aline1, aline2, city, state, postal))

        return redirect("/advisors")

    # Populate Advisors table
    query = '''
    SELECT advisor_id AS ID, first_name AS First, last_name AS Last, school_email AS Email, phone_number AS Phone, 
    address_line1 AS "Address Line 1", address_line2 AS "Address Line 2", 
    city AS City, state AS State, postal_code AS "Postal Code"
    FROM Advisors
    '''
    cursor = db.execute_query(db_connection=db_connection, query=query)
    advisors = cursor.fetchall()

    return render_template("advisors.j2", advisors=advisors)


@app.route('/instructors', methods=['POST', 'GET'])
def instructors():

    db_connection.ping(True)  # ping to avoid timeout

    # Insert Instructor
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        phone = request.form["phone"]
        aline1 = request.form["aline1"]
        aline2 = request.form["aline2"]
        city = request.form["city"]
        state = request.form["state"]
        postal = request.form["postal"]

        query = '''
        INSERT INTO Instructors 
        (first_name, last_name, school_email, 
        phone_number, address_line1, address_line2, 
        city, state, postal_code) 
        VALUES 
        (%s, %s, %s, %s, %s,  NULLIF(%s, ''), %s, %s, %s)
        '''
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(
            fname, lname, email, phone, aline1, aline2, city, state, postal))

        return redirect("/instructors")

    # Populate Advisors table
    query = '''
    SELECT instructor_id AS ID, first_name AS First, last_name AS Last, 
    school_email AS Email, phone_number AS Phone, 
    address_line1 AS "Address Line 1", address_line2 AS "Address Line 2", 
    city AS City, state AS State, postal_code AS "Postal Code"
    FROM Instructors
    '''
    cursor = db.execute_query(db_connection=db_connection, query=query)
    instructors = cursor.fetchall()

    return render_template("instructors.j2", instructors=instructors)


@app.route('/courses', methods=['POST', 'GET'])
def courses():
    
    db_connection.ping(True)  # ping to avoid timeout

    # Insert Course into Courses
    if request.method == "POST":
        course_id = request.form["course_id"]
        title = request.form["title"]
        start_time = request.form["start_time"]
        num_of_credits = request.form["num_of_credits"]
        end_time = request.form["end_time"]
        is_remote = request.form["is_remote"]
        capacity = request.form["capacity"]

        query = """
        INSERT INTO Courses 
        (course_id, title, start_time, end_time, num_of_credits, end_time, is_remote, capacity) 
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(
            course_id, title, start_time, end_time, num_of_credits, end_time, is_remote, capacity))

        # Insert into Courses_Instructors Table
        query2 = """
        INSERT INTO Courses_Instructors 
        (instructor_id, course_id) 
        VALUES 
        (%s, %s)
        """
        cursor = db.execute_query(db_connection=db_connection, query=query2, query_params=(
            instructor_id, course_id))

        return redirect("/courses")

    # Populate Courses table
    query = '''
    SELECT course_id AS "Course ID", title AS Title, start_time AS "Start Time", end_time AS "End Time", 
    num_of_credits AS "Num. of Credits",
    CASE
        WHEN is_remote = 1 THEN 'YES'
        WHEN is_remote = 0 THEN 'NO'
    END AS "Is Remote", 
    capacity AS Capacity
    FROM Courses;
    '''
    cursor = db.execute_query(db_connection=db_connection, query=query)
    courses = cursor.fetchall()

    # Populate Instructor menu
    query2 = """
    SELECT instructor_id, CONCAT(first_name, ' ', last_name) AS Instructor FROM Instructors
    """
    cursor = db.execute_query(db_connection=db_connection, query=query2)
    instructors = cursor.fetchall()

    return render_template("courses.j2", courses=courses, instructors=instructors)


@app.route('/courses_instructors', methods=['POST', 'GET'])
def courses_instructors():
    
    db_connection.ping(True)  # ping to avoid timeout

    # Insert into Courses_Instructors
    if request.method == 'POST':
        instructor_id = request.form["instructor_id"]
        course_id = request.form["course_id"]

        query = """
            INSERT INTO Courses_Instructors 
            (instructor_id, course_id) 
            VALUES 
            (%s, %s)
            """
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(
            instructor_id, course_id))

        return redirect('/courses_instructors')

    # Populate Courses_Instructors table
    query = '''
    SELECT course_instructor_id AS "Course_Instructor ID", 
    CONCAT(Instructors.first_name, " ", Instructors.last_name) AS Instructor,
    Courses.title AS Course 
    FROM Courses_Instructors 
    INNER JOIN Instructors ON Courses_Instructors.instructor_id = Instructors.instructor_id
    INNER JOIN Courses ON Courses_Instructors.course_id = Courses.course_id;
    '''
    cursor = db.execute_query(db_connection=db_connection, query=query)
    courses_instructors = cursor.fetchall()

    # Populate Course dropdown menu
    query2 = 'SELECT course_id, title AS Course FROM Courses;'
    cursor = db.execute_query(db_connection=db_connection, query=query2)
    courses = cursor.fetchall()

    # Populate Instructor dropdown menu
    query3 = """
    SELECT instructor_id, CONCAT(first_name, ' ', last_name) AS Instructor FROM Instructors;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query3)
    instructors = cursor.fetchall()

    # Sends the results back to the web browser.
    return render_template("courses_instructors.j2", courses_instructors=courses_instructors, courses=courses, instructors=instructors)













@app.route('/registrations', methods=['POST', 'GET'])
def registrations():

    db_connection.ping(True)  # ping to avoid timeout

    # Insert Registration
    if request.method == "POST":
        studentid = request.form["studentid"]
        courseid = request.form["courseid"]
        semesterid = request.form["semesterid"]
        year = request.form["year"]

        query = """
        INSERT INTO Registrations 
        (student_id, course_id, year, semester_id) 
        VALUES 
        (%s, %s, %s, %s)
        """
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(
            studentid, courseid, year, semesterid))

        return redirect("/registrations")

    # Populate Registrations table
    query = '''
    SELECT reg_id AS "Reg ID", CONCAT(Students.first_name, ' ', Students.last_name) AS Student, 
    Courses.title AS Course, Semesters.title AS Semester, year AS Year
    FROM Registrations 
    INNER JOIN Students ON Registrations.student_id = Students.student_id
    INNER JOIN Courses ON Registrations.course_id = Courses.course_id
    INNER JOIN Semesters ON Registrations.semester_id = Semesters.semester_id
    ORDER BY reg_id;
    '''
    cursor = db.execute_query(db_connection=db_connection, query=query)
    registrations = cursor.fetchall()

    # Populate Student dropdown
    query2 = """
    SELECT student_id, CONCAT(first_name, ' ', last_name) AS Student FROM Students
    """
    cursor = db.execute_query(db_connection=db_connection, query=query2)
    students = cursor.fetchall()

    # Populate Courses dropdown
    query3 = """
    SELECT course_id, title AS Course FROM Courses
    """
    cursor = db.execute_query(db_connection=db_connection, query=query3)
    courses = cursor.fetchall()

    # Populate Semesters dropdown
    query4 = """
    SELECT semester_id, title AS Semester FROM Semesters
    """
    cursor = db.execute_query(db_connection=db_connection, query=query4)
    semesters = cursor.fetchall()

    return render_template("registrations.j2", registrations=registrations, students=students, courses=courses, semesters=semesters)


@app.route('/delete_reg/<int:regID>')
def delete_reg(regID):
    # mySQL query to delete the registration with our passed id
    query = "DELETE FROM Registrations WHERE reg_id = %s;"
    cursor = db.execute_query(
        db_connection=db_connection, query=query, query_params=(regID,))

    # redirect back to registrations page
    return redirect("/registrations")


@app.route('/edit_reg/<int:regID>', methods=['POST', 'GET'])
def edit_reg(regID):
    if request.method == 'GET':
        # mySQL query to grab the info of the registration with our passed regID
        query = """
        SELECT CONCAT(Students.first_name, ' ', Students.last_name) AS Student, 
        Courses.title AS Course, Semesters.title AS Semester, year AS Year
        FROM Registrations 
        INNER JOIN Students ON Registrations.student_id = Students.student_id
        INNER JOIN Courses ON Registrations.course_id = Courses.course_id
        INNER JOIN Semesters ON Registrations.semester_id = Semesters.semester_id
        WHERE reg_id = %s;
        """ % (regID)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        # Populate Student dropdown
        query2 = """
        SELECT student_id, CONCAT(first_name, ' ', last_name) AS Student FROM Students
        """
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        students = cursor.fetchall()

        # Populate Courses dropdown
        query3 = """
        SELECT course_id, title AS Course FROM Courses
        """
        cursor = db.execute_query(db_connection=db_connection, query=query3)
        courses = cursor.fetchall()

        # Populate Semesters dropdown
        query4 = """
        SELECT semester_id, title AS Semester FROM Semesters
        """
        cursor = db.execute_query(db_connection=db_connection, query=query4)
        semesters = cursor.fetchall()

        # render edit_registrations page passing our query data, students, courses and semesters to the edit_registrations template
        return render_template('edit_registrations.j2', data=data, students=students, courses=courses, semesters=semesters, regID=regID)

    if request.method == "POST":
        # fire off if user clicks the 'Edit Registration' button

        # if request.form.get("Edit_Registration"): <- wouldn't work with this line for some reason

        # grab user form inputs
        studentid = request.form["studentid"]
        courseid = request.form["courseid"]
        semesterid = request.form["semesterid"]
        year = request.form["year"]

        query = '''
        UPDATE Registrations 
        SET student_id = %s, course_id = %s, 
        year = %s, semester_id = %s
        WHERE reg_id= %s
        '''
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(
            studentid, courseid, year, semesterid, regID))

        return redirect("/registrations")


@app.route('/semesters', methods=['POST', 'GET'])
def semesters():
    return render_template("semesters.j2")


@app.route('/grades', methods=['POST', 'GET'])
def grades():
    return render_template("grades.j2")


# Listener
if __name__ == "__main__":

    app.run(port=7862, debug=True)
