from flask import Flask, render_template, json, redirect, Blueprint
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

db_connection = db.connect_to_database()
students_view = Blueprint('students_view', __name__)

@students_view.route('/', methods=['POST', 'GET'])
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

@students_view.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    # mySQL query to delete the student with our passed id
    query = "DELETE FROM Students WHERE student_id = %s;"
    cursor = db.execute_query(
        db_connection=db_connection, query=query, query_params=(student_id,))

    # redirect back to Students page
    return redirect("/students")

@students_view.route('/edit_student/<int:student_id>', methods=['POST', 'GET'])
def edit_student(student_id):
    if request.method == 'GET':
        # mySQL query to grab the info of the student with our passed student_id
        query = """
        SELECT Students.student_id AS "ID", Students.first_name AS First, Students.last_name AS Last, 
        Students.school_email AS Email, Students.phone_number AS Phone, 
        Students.address_line1 AS "Address Line 1", Students.address_line2 AS "Address Line 2", 
        Students.city AS City, Students.state AS State, Students.postal_code AS "Postal Code", 
        Majors.title AS Major, 
        CONCAT(Advisors.first_name, ' ', Advisors.last_name) AS Advisor
        FROM Students 
        INNER JOIN Advisors ON Students.advisor_id = Advisors.advisor_id
        LEFT JOIN Majors ON Students.major_id = Majors.major_id
        WHERE student_id = %s;
        """ % (student_id)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        print(data)

        # Populate Majors dropdown
        query2 = 'SELECT major_id, title AS Major FROM Majors;'
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        majors = cursor.fetchall()

        # Populate Advisors dropdown
        query3 = "SELECT advisor_id, CONCAT(first_name, ' ', last_name) AS Advisor FROM Advisors;"
        cursor = db.execute_query(db_connection=db_connection, query=query3)
        advisors = cursor.fetchall()

        # render students_edit page passing our query data, majors and advisors to the edit_student template
        return render_template('students_edit.j2', data=data, majors=majors, advisors=advisors, student_id=student_id)

    if request.method == "POST":
        # fire off if user clicks the 'Edit Student' button

        # grab user form inputs
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        phone = request.form["phone"]
        aline1 = request.form["aline1"]
        aline2 = request.form["aline2"]
        city = request.form["city"]
        state = request.form["state"]
        postal = request.form["postal"]
        major_id = request.form["major_id"]
        advisor_id = request.form["advisor_id"]

        query = '''
        UPDATE Students 
        SET first_name = %s, last_name = %s, school_email = %s, phone_number = %s, 
        address_line1 = %s, address_line2 = %s, city = %s, 
        state = %s, postal_code = %s, major_id = NULLIF(%s, 'NULL'), advisor_id = %s
        WHERE student_id = %s;
        '''
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(
            fname, lname, email, phone, aline1, aline2, city, state, 
            postal, major_id, advisor_id, student_id))

        return redirect("/students")
