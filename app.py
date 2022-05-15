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

    # Insert student
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

    print(students)

    # Populate Majors dropdown
    query2 = 'SELECT major_id, title FROM Majors;'
    cursor = db.execute_query(db_connection=db_connection, query=query2)
    majors = cursor.fetchall()

    print(majors)

    # Populate Advisors dropdown
    query3 = "SELECT advisor_id, CONCAT(first_name, ' ', last_name) AS Advisor FROM Advisors;"
    cursor = db.execute_query(db_connection=db_connection, query=query3)
    advisors = cursor.fetchall()

    print(advisors)

    # Sends the results back to the web browser.
    return render_template("students.j2", students=students, majors=majors, advisors=advisors)


@app.route('/majors')
def majors():
    return render_template("majors.j2")


@app.route('/advisors')
def advisors():
    return render_template("advisors.j2")


@app.route('/instructors')
def instructors():
    return render_template("instructors.j2")


@app.route('/courses')
def courses():
    return render_template("courses.j2")


@app.route('/courses_instructors')
def courses_instructors():
    return render_template("courses_instructors.j2")


@app.route('/registrations')
def registrations():
    return render_template("registrations.j2")


@app.route('/semesters')
def semesters():
    return render_template("semesters.j2")


@app.route('/grades')
def grades():
    return render_template("grades.j2")


# Listener


if __name__ == "__main__":

    app.run(port=7862, debug=True)
