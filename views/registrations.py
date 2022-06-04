# Citation for the Design of our views using Blueprints
# Date: June 2022
# Resource: Flask.palletsprojects.com
# Source URL: https://flask.palletsprojects.com/en/2.1.x/blueprints

from flask import Flask, render_template, json, redirect, Blueprint
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

db_connection = db.connect_to_database()
registrations_view = Blueprint('registrations_view', __name__)

@registrations_view.route('/', methods=['POST', 'GET'])
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


@registrations_view.route('/delete_reg/<int:regID>')
def delete_reg(regID):
    # mySQL query to delete the registration with our passed id
    query = "DELETE FROM Registrations WHERE reg_id = %s;"
    cursor = db.execute_query(
        db_connection=db_connection, query=query, query_params=(regID,))

    # redirect back to registrations page
    return redirect("/registrations")


@registrations_view.route('/edit_reg/<int:regID>', methods=['POST', 'GET'])
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