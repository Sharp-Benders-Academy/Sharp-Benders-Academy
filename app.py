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
from views.grades import grades_view

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
app.register_blueprint(grades_view, url_prefix='/grades')

# Index
@app.route('/')
def root():
    return render_template("home.j2")


# Listener
if __name__ == "__main__":

    app.run(port=7862, debug=True)
