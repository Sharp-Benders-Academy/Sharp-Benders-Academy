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

db_connection = db.connect_to_database()
app = Flask(__name__)


# register blueprints
app.register_blueprint(students_view, url_prefix='/students')
app.register_blueprint(majors_view, url_prefix='/majors')
app.register_blueprint(advisors_view, url_prefix='/advisors')
app.register_blueprint(instructors_view, url_prefix='/instructors')
app.register_blueprint(courses_view, url_prefix='/courses')
app.register_blueprint(courses_instructors_view, url_prefix='/courses_instructors')

# Index
@app.route('/')
def root():
    return render_template("home.j2")


# @app.route('/courses_instructors', methods=['POST', 'GET'])
# def courses_instructors():
    
#     db_connection.ping(True)  # ping to avoid timeout

#     # Insert into Courses_Instructors
#     if request.method == 'POST':
#         instructor_id = request.form["instructor_id"]
#         course_id = request.form["course_id"]

#         query = """
#             INSERT INTO Courses_Instructors 
#             (instructor_id, course_id) 
#             VALUES 
#             (%s, %s)
#             """
#         cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(
#             instructor_id, course_id))

#         return redirect('/courses_instructors')

#     # Populate Courses_Instructors table
#     query = '''
#     SELECT course_instructor_id AS "Course_Instructor ID", 
#     CONCAT(Instructors.first_name, " ", Instructors.last_name) AS Instructor,
#     Courses.title AS Course 
#     FROM Courses_Instructors 
#     INNER JOIN Instructors ON Courses_Instructors.instructor_id = Instructors.instructor_id
#     INNER JOIN Courses ON Courses_Instructors.course_id = Courses.course_id;
#     '''
#     cursor = db.execute_query(db_connection=db_connection, query=query)
#     courses_instructors = cursor.fetchall()

#     # Populate Course dropdown menu
#     query2 = 'SELECT course_id, title AS Course FROM Courses;'
#     cursor = db.execute_query(db_connection=db_connection, query=query2)
#     courses = cursor.fetchall()

#     # Populate Instructor dropdown menu
#     query3 = """
#     SELECT instructor_id, CONCAT(first_name, ' ', last_name) AS Instructor FROM Instructors;
#     """
#     cursor = db.execute_query(db_connection=db_connection, query=query3)
#     instructors = cursor.fetchall()

#     # Sends the results back to the web browser.
#     return render_template("courses_instructors.j2", courses_instructors=courses_instructors, courses=courses, instructors=instructors)


# @app.route('/delete_course_instructor/<int:course_instructor_id>')
# def delete_course_instructor(course_instructor_id):
#     # mySQL query to delete the course_instructor with our passed id
#     query = "DELETE FROM Courses_Instructors WHERE course_instructor_id = %s;"
#     cursor = db.execute_query(
#         db_connection=db_connection, query=query, query_params=(course_instructor_id,))

#     # redirect back to course_instructor page
#     return redirect("/courses_instructors")


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

    db_connection.ping(True)  # ping to avoid timeout

    # Insert Semester
    if request.method == "POST":
        semesterid = request.form["semesterid"]
        semestertitle = request.form["semestertitle"]

        query='''
        INSERT INTO Semesters 
        (semester_id, title) 
        VALUES 
        (%s, %s)
        '''

        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(
            semesterid, semestertitle))
        
        return redirect("/semesters")

    query = '''
    SELECT semester_id AS "Semester ID", title AS Title
    FROM Semesters
    '''
    cursor = db.execute_query(db_connection=db_connection, query=query)
    semesters = cursor.fetchall()

    print(semesters)

    return render_template("semesters.j2", semesters=semesters)


@app.route('/delete_semester/<semester_id>')
def delete_semester(semester_id):
    # mySQL query to delete the semester with our passed id
    query = "DELETE FROM Semesters WHERE semester_id = %s;"
    cursor = db.execute_query(
        db_connection=db_connection, query=query, query_params=(semester_id,))

    # redirect back to Semesters page
    return redirect("/semesters")


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
