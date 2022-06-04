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
semesters_view = Blueprint('semesters_view', __name__)

@semesters_view.route('/', methods=['POST', 'GET'])
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


@semesters_view.route('/delete_semester/<semester_id>')
def delete_semester(semester_id):
    # mySQL query to delete the semester with our passed id
    query = "DELETE FROM Semesters WHERE semester_id = %s;"
    cursor = db.execute_query(
        db_connection=db_connection, query=query, query_params=(semester_id,))

    # redirect back to Semesters page
    return redirect("/semesters")
