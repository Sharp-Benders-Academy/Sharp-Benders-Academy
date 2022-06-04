from flask import Flask, render_template, json, redirect, Blueprint
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

db_connection = db.connect_to_database()
courses_instructors_view = Blueprint('courses_instructors_view', __name__)

@courses_instructors_view.route('/', methods=['POST', 'GET'])
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


@courses_instructors_view.route('/delete_course_instructor/<int:course_instructor_id>')
def delete_course_instructor(course_instructor_id):
    # mySQL query to delete the course_instructor with our passed id
    query = "DELETE FROM Courses_Instructors WHERE course_instructor_id = %s;"
    cursor = db.execute_query(
        db_connection=db_connection, query=query, query_params=(course_instructor_id,))

    # redirect back to course_instructor page
    return redirect("/courses_instructors")