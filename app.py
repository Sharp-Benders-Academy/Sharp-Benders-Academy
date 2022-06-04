from crypt import methods
from distutils.log import debug
from flask import Flask, render_template, json, redirect, Blueprint
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

# blueprint imports
from views.students import students_view
from views.majors import majors_view
from views.advisors import advisors_view
from views.instructors import instructors_view
from views.courses import courses_view
from views.courses_instructors import courses_instructors_view
from views.registrations import registrations_view
from views.semesters import semesters_view

db_connection = db.connect_to_database()
app = Flask(__name__)


# register blueprints
app.register_blueprint(students_view, url_prefix='/students')
app.register_blueprint(majors_view, url_prefix='/majors')
app.register_blueprint(advisors_view, url_prefix='/advisors')
app.register_blueprint(instructors_view, url_prefix='/instructors')
app.register_blueprint(courses_view, url_prefix='/courses')
app.register_blueprint(courses_instructors_view, url_prefix='/courses_instructors')
app.register_blueprint(registrations_view, url_prefix='/registrations')
app.register_blueprint(semesters_view, url_prefix='/semesters')

# Index
@app.route('/')
def root():
    return render_template("home.j2")


@app.route('/grades', methods=['POST', 'GET'])
def grades():
    
    db_connection.ping(True)  # ping to avoid timeout

    # Insert Grade into Grades
    if request.method == "POST":
        student_id = request.form["student_id"]
        course_id = request.form["course_id"]
        passed_course = request.form["passed_course"]

        query = """
        INSERT INTO Grades 
        (passed_course, student_id, course_id) 
        VALUES 
        (%s, %s, %s)
        """
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(
            passed_course, student_id, course_id))

        return redirect("/grades")

    # Populate Grades table
    query = '''
    SELECT grade_id AS "Grade ID", 
    CONCAT(Students.first_name, ' ', Students.last_name) AS Student, 
    Courses.title AS Course,
    CASE 
        WHEN passed_course = 1 THEN 'YES'
        WHEN passed_course = 0 THEN 'NO'
    END AS "Passed Course"
    FROM Grades 
    INNER JOIN Students ON Grades.student_id = Students.student_id
    INNER JOIN Courses ON Grades.course_id = Courses.course_id
    '''
    cursor = db.execute_query(db_connection=db_connection, query=query)
    grades = cursor.fetchall()

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

    # Populate Filter Students dropdown (only if they have a Grade)
    query4 = """
    SELECT DISTINCT Students.student_id, CONCAT(Students.first_name, ' ', Students.last_name) AS Student FROM Students
    INNER JOIN Grades ON Grades.student_id = Students.student_id;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query4)
    students_with_grades = cursor.fetchall()

    return render_template("grades.j2", grades=grades, students=students, courses=courses, students_with_grades=students_with_grades)

@app.route('/filter_grades', methods=['POST', 'GET'])
def filter_grades():

    # get filter student id from the form on grades page
    filter_student_id = request.form["filter_student_id"]

    # mySQL query to grab the info of the grades with our passed student_id
    query = """
    SELECT grade_id AS "Grade ID", 
    CONCAT(Students.first_name, ' ', Students.last_name) AS Student, 
    Courses.title AS Course,
    CASE 
        WHEN passed_course = 1 THEN 'YES'
        WHEN passed_course = 0 THEN 'NO'
    END AS "Passed Course"
    FROM Grades 
    INNER JOIN Students ON Grades.student_id = Students.student_id
    INNER JOIN Courses ON Grades.course_id = Courses.course_id
    WHERE Students.student_id 
    = %s;
    """ % (filter_student_id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    grades = cursor.fetchall()

    # Populate Student Name
    query2 = """
    SELECT CONCAT(first_name, ' ', last_name) AS Student FROM Students
    WHERE Students.student_id
    = %s;
    """ % (filter_student_id)
    cursor = db.execute_query(db_connection=db_connection, query=query2)
    student_name = cursor.fetchall()

    # render grades_filter page passing our query data for grades and the student_id to the template
    return render_template("grades_filter.j2", grades=grades, student_name=student_name)


@app.route('/delete_grade/<int:grade_id>')
def delete_grade(grade_id):
    # mySQL query to delete the grade with our passed id
    query = "DELETE FROM Grades WHERE grade_id = %s;"
    cursor = db.execute_query(
        db_connection=db_connection, query=query, query_params=(grade_id,))

    # redirect back to grades page
    return redirect("/grades")


# Listener
if __name__ == "__main__":

    app.run(port=7862, debug=True)
