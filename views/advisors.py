from flask import Flask, render_template, json, redirect, Blueprint
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

db_connection = db.connect_to_database()
advisors_view = Blueprint('advisors_view', __name__)

@advisors_view.route('/', methods=['POST', 'GET'])
def advisors():

    db_connection.ping(True)  # ping to avoid timeout

    # Insert Advisor
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        phone = request.form["phone"]
        aline1 = request.form["aline1"]
        aline2 = request.form["aline2"]
        city = request.form["city"]
        state = request.form["state"]
        postal = request.form["postal"]

        query = '''
        INSERT INTO Advisors 
        (first_name, last_name, school_email, 
        phone_number, address_line1, address_line2, 
        city, state, postal_code) 
        VALUES 
        (%s, %s, %s, %s, %s,  NULLIF(%s, ''), %s, %s, %s)
        '''
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(
            fname, lname, email, phone, aline1, aline2, city, state, postal))

        return redirect("/advisors")

    # Populate Advisors table
    query = '''
    SELECT advisor_id AS ID, first_name AS First, last_name AS Last, school_email AS Email, phone_number AS Phone, 
    address_line1 AS "Address Line 1", address_line2 AS "Address Line 2", 
    city AS City, state AS State, postal_code AS "Postal Code"
    FROM Advisors
    '''
    cursor = db.execute_query(db_connection=db_connection, query=query)
    advisors = cursor.fetchall()

    return render_template("advisors.j2", advisors=advisors)


@advisors_view.route('/delete_advisor/<int:advisor_id>')
def delete_advisor(advisor_id):
    # mySQL query to delete the advisor with our passed id
    query = "DELETE FROM Advisors WHERE advisor_id = %s;"
    cursor = db.execute_query(
        db_connection=db_connection, query=query, query_params=(advisor_id,))

    # redirect back to Advisors page
    return redirect("/advisors")