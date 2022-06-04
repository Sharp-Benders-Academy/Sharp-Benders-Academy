from flask import Flask, render_template, json, redirect, Blueprint
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

db_connection = db.connect_to_database()
courses_view = Blueprint('courses_view', __name__)

@courses_view.route('/', methods=['POST', 'GET'])
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
        instructor_ids = request.form.getlist('instructor_ids')

        query = """
        INSERT INTO Courses 
        (course_id, title, start_time, end_time, num_of_credits, is_remote, capacity) 
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(
            course_id, title, start_time, end_time, num_of_credits, is_remote, capacity))

        # Insert into Courses_Instructors Table
        query2 = """
        INSERT INTO Courses_Instructors 
        (instructor_id, course_id) 
        VALUES 
        (%s, %s)
        """
        for instructor_id in instructor_ids:
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


@courses_view.route('/delete_course/<int:courseID>')
def delete_course(courseID):
    # mySQL query to delete the course with our passed id
    query = "DELETE FROM Courses WHERE course_id = %s;"
    cursor = db.execute_query(
        db_connection=db_connection, query=query, query_params=(courseID,))

    # redirect back to course page
    return redirect("/courses")