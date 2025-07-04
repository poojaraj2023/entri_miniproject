# entri_miniproject
Student Grading Management System
=================================

DESCRIPTION:
------------
This is a command-line based Python application using SQLite to manage student records and grades.

There are two user roles:
1. Student:
   - Can register and log in
   - Can view profile, subject marks, total, average, grade
   - Can see eligibility for next class

2. Teacher:
   - Can register and log in
   - Can update/add marks for students
   - Can view passed and failed student lists

GRADE CALCULATION:
------------------
Grades are assigned based on average marks:
- A+: >= 90
- A:  >= 85
- B:  >= 70
- C:  >= 60
- D:  >= 40
- F : < 40


PROMOTION ELIGIBILITY:
-----------------------
- Students are eligible for the next class if their average is >= 40.

HOW TO RUN:
-----------
python Student_System_Management.py



FILES:
------
- Student_System_Management.py : Main application
- Student_grading_system.db : Auto-created SQLite database
