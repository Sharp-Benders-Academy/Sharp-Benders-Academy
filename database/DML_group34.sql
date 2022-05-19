-- CS 340 - Databases
-- Group 34 - Sharp Squad: Elizabeth Thorne and Faihaan Arif
-- Project: Sharp Benders Academy
-- Database Manipulation Queries, in the follow order:
-- 1. Students
-- 2. Instructors
-- 3. Advisors
-- 4. Registrations (Update and Delete Queries)
-- 5. Grades (Search/Filter Queries)
-- 6. Courses (Delete Query)
-- 7. Courses_Instructors
-- 8. Majors
-- 9. Semesters

---------------------------------------------------------------------------
-- 1. Students

-- Majors dropdown menu: get all major_ids and titles to populate the Students dropdown
SELECT major_id, title FROM Majors

-- Advisors dropdown menu: get all advisor_ids and firstname, lastname to populate the Students dropdown
SELECT advisor_id, CONCAT(first_name, ' ', last_name) AS Advisor FROM Advisors

-- Select Students: get all students, their major title and advisor last name for the List Students page
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

-- Add a new Student
INSERT INTO Students 
(first_name, last_name, school_email, 
phone_number, address_line1, address_line2, 
city, state, postal_code, advisor_id, major_id) 
VALUES 
(:first_name_input, :last_name_input, :school_email_input, 
:phone_number_input, :address_line1_input, :address_line2_input, 
:city_input, :state_input, :postal_code_input, :advisor_id_from_dropdown_input, :major_id_from_dropdown_input)



---------------------------------------------------------------------------
-- 2. Instructors

-- Select Instructors: get all instructors for List Instructors page
SELECT instructor_id AS ID, first_name AS First, last_name AS Last, 
school_email AS Email, phone_number AS Phone, 
address_line1 AS "Address Line 1", address_line2 AS "Address Line 2", 
city AS City, state AS State, postal_code AS "Postal Code"
FROM Instructors

-- Add a new Instructor
INSERT INTO Instructors 
(first_name, last_name, school_email, 
phone_number, address_line1, address_line2, 
city, state, postal_code) 
VALUES 
(:first_name_input, :last_name_input, :school_email_input, 
:phone_number_input, :address_line1_input, :address_line2_input, 
:city_input, :state_input, :postal_code_input)



---------------------------------------------------------------------------
-- 3. Advisors

-- Select Advisors: get all advisors for List Advisors page
SELECT advisor_id AS ID, first_name AS First, last_name AS Last, school_email AS Email, phone_number AS Phone, 
address_line1 AS "Address Line 1", address_line2 AS "Address Line 2", 
city AS City, state AS State, postal_code AS "Postal Code"
FROM Advisors

-- Add a new Advisors
INSERT INTO Advisors 
(first_name, last_name, school_email, 
phone_number, address_line1, address_line2, 
city, state, postal_code) 
VALUES 
(:first_name_input, :last_name_input, :school_email_input, 
:phone_number_input, :address_line1_input, :address_line2_input, 
:city_input, :state_input, :postal_code_input)



---------------------------------------------------------------------------
-- 4. Registrations

-- Students Drop Down Menu
SELECT student_id, CONCAT(first_name, ' ', last_name) AS Student FROM Students

-- Courses Drop Down Menu
SELECT course_id, title AS Course FROM Courses

-- Semesters Drop Down Menu
SELECT semester_id, title AS Semester FROM Semesters

-- Select Registrations: get all registrations for List Registrations page
SELECT reg_id AS "Reg ID", CONCAT(Students.first_name, ' ', Students.last_name) AS Student, 
    Courses.title AS Course, Semesters.title AS Semester, year AS Year
    FROM Registrations 
    INNER JOIN Students ON Registrations.student_id = Students.student_id
    INNER JOIN Courses ON Registrations.course_id = Courses.course_id
    INNER JOIN Semesters ON Registrations.semester_id = Semesters.semester_id
    ORDER BY reg_id;

-- Add new Registrations
INSERT INTO Registrations 
(student_id, course_id, year, semester_id) 
VALUES 
(:student_id_from_dropdown_input, :course_id_from_dropdown_input, 
:year_input, :semester_id_from_dropdown_input)

-- get a single registration's data for the Update Registration form
SELECT reg_id, student_id, course_id, year, semester_id 
FROM Registrations 
WHERE reg_id = :reg_ID_selected_from_browse_registrations_page

-- get a single registration's data for the Update Registration form (updated)
SELECT CONCAT(Students.first_name, ' ', Students.last_name) AS Student, 
    Courses.title AS Course, Semesters.title AS Semester, year AS Year
    FROM Registrations 
    INNER JOIN Students ON Registrations.student_id = Students.student_id
    INNER JOIN Courses ON Registrations.course_id = Courses.course_id
    INNER JOIN Semesters ON Registrations.semester_id = Semesters.semester_id
    WHERE reg_id = :reg_ID_selected_from_browse_registrations_page;

-- update a Registration data based on submission of the Update Registraton form 
UPDATE Registrations 
SET student_id = :student_id_from_dropdown_Input, course_id = :course_id_from_dropdown_Input, 
year = :yearInput, semester_id = :semester_id_from_dropdown_Input
WHERE reg_id= :reg_id_from_the_update_form

-- Delete a Registration (M-to-M relationship deletion)
DELETE FROM Registrations 
WHERE student_id = :student_id_selected_from_registrations_list 
AND course_id = :course_id_selected_from_registrations_list

-- Delete a Registration
DELETE FROM Registrations
WHERE reg_id = :reg_id_input



---------------------------------------------------------------------------
-- 5. Grades

-- Students Drop Down Menu
SELECT student_id, CONCAT(first_name, ' ', last_name) AS Student FROM Students

-- Courses Drop Down Menu
SELECT course_id, title AS Course FROM Courses

-- Select Grades: get all grades for List Grades page
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

-- Add new Grade
INSERT INTO Grades
(passed_course, student_id, course_id)
VALUES
(passed_course_input, :student_id_from_dropdown_input, :course_id_from_dropdown_input)

-- Search/Filter Query for Finding a Student
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
WHERE CONCAT(Students.first_name, ' ', Students.last_name) 
 = :student_selected_from_browse_students_page


---------------------------------------------------------------------------
-- 6. Courses

-- Select Courses: get all courses for List Courses page
SELECT course_id AS "Course ID", title AS Title, start_time AS "Start Time", end_time AS "End Time", 
num_of_credits AS "Num. of Credits",
CASE
    WHEN is_remote = 1 THEN 'YES'
    WHEN is_remote = 0 THEN 'NO'
END AS "Is Remote", 
capacity AS Capacity
FROM Courses

-- Add a new Course
INSERT INTO Courses 
(course_id, title, start_time, end_time, num_of_credits, is_remote, capacity) 
VALUES 
(:course_id_input, :title_input, :start_time_input, :end_time_input, :num_of_credits_input, 
:is_remote_input, :capacity_input)

-- Add a new Courses_Instructors associated with the new course
-- May be called multiple times if Multiple Instructors teach the course
INSERT INTO Courses_Instructors 
(instructor_id, course_id) 
VALUES 
(:instructor_id_from_dropdown_input, :course_id_from_dropdown_input)


-- Delete a Course (M-to-M relationship deletion)
DELETE FROM Courses 
WHERE course_id = :course_id_selected_from_courses_list



---------------------------------------------------------------------------
-- 7. Courses_Instructors

-- Courses Drop Down Menu
SELECT course_id, title AS Course FROM Courses

-- Instructors Drop Down Menu
SELECT instructor_id, CONCAT(first_name, ' ', last_name) AS Instructor FROM Instructors

-- Select Courses_Instructors: get all courses_instructors for List Courses_Instructors page
SELECT course_instructor_id AS "Course_Instructor_ID", 
CONCAT(Instructors.first_name, " ", Instructors.last_name) AS Instructor,
Courses.title AS Course 
FROM Courses_Instructors 
INNER JOIN Instructors ON Courses_Instructors.instructor_id = Instructors.instructor_id
INNER JOIN Courses ON Courses_Instructors.course_id = Courses.course_id

-- Add a new Courses_Instructors
INSERT INTO Courses_Instructors 
(instructor_id, course_id) 
VALUES 
(:instructor_id_from_dropdown_input, :course_id_from_dropdown_input)



---------------------------------------------------------------------------
-- 8. Majors

-- Select Majors: get all majors for List Majors page
SELECT major_id AS "Major ID", title AS Title
FROM Majors

-- Add a new Major
INSERT INTO Majors 
(major_id, title) 
VALUES 
(:major_id_input, :title_input)



---------------------------------------------------------------------------
-- 9. Semesters

-- Select Semesters: get all semesters for List Semesters page
SELECT semester_id AS "Semester ID", title AS Title
FROM Semesters

-- Add a new Semester
INSERT INTO Semesters 
(semester_id, title) 
VALUES 
(:semester_id_input, :title_input)
