from flask import Flask, render_template, json, redirect, Blueprint
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

db_connection = db.connect_to_database()
majors_view = Blueprint('majors_view', __name__)


@majors_view.route('/', methods=['POST', 'GET'])
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

@majors_view.route('/delete_major/<major_id>')
def delete_major(major_id):
    # mySQL query to delete the major with our passed id
    query = "DELETE FROM Majors WHERE major_id = %s;"
    cursor = db.execute_query(
        db_connection=db_connection, query=query, query_params=(major_id,))

    # redirect back to Majors page
    return redirect("/majors")