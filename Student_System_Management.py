import sqlite3

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("Student_grading_system.db")
cursor = conn.cursor()

# ===================== DATABASE SETUP =====================

# Students table with profile info and login credentials
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Firstname TEXT,
        Lastname TEXT,
        DOB TEXT,
        Gender TEXT,
        Student_class TEXT,
        Username TEXT UNIQUE,
        Password TEXT
    )
''')

# Marks table linked to Students by student_id
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Marks (
        Student_id INTEGER,
        Subject TEXT,
        Marks INTEGER,
        PRIMARY KEY (Student_id, Subject),
        FOREIGN KEY (Student_id) REFERENCES students(ID)
    )
''')

# Teachers table with login credentials
cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT UNIQUE,
        Password TEXT
    )
''')

conn.commit()

# Calculate grade based on average

def calculate_grade(avg):
    if avg >= 90:
        return 'A+'
    elif avg >= 85:
        return 'A'
    elif avg >= 70:
        return 'B'
    elif avg >= 60:
        return 'C'
    elif avg >= 40:
        return 'D'
    else:
        return 'F'

def is_eligible(avg):
    return avg >= 40

# Student Registration
def register_student():
    try:
        print("\n--- Student Registration ---")
        fname = input("First Name: ")
        lname = input("Last Name: ")
        dob = input("Date of Birth (DD-MM-YYYY): ")
        gender = input("Gender: ")
        student_class = input("Class: ")
        username = input("Username: ")
        password = input("Password: ")

        cursor.execute('''
            INSERT INTO Students (Firstname, Lastname, DOB, Gender, Student_class, Username, Password)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (fname, lname, dob, gender, student_class, username, password))
        conn.commit()
        print("Student registered successfully!\n")
    except Exception as e:
        print("Registration failed:", e)

def student_login():
    try:
        print("\n--- Student Login ---")
        username = input("Username: ")
        password = input("Password: ")

        cursor.execute("SELECT * FROM Students WHERE Username=? AND Password=?", (username, password))
        student = cursor.fetchone()

        if student:
            student_id = student[0]
            print(f"\nWelcome {student[1]} {student[2]}")
            print(f"DOB: {student[3]}")
            print(f"Gender: {student[4]}")
            print(f"Class: {student[5]}")

            cursor.execute("SELECT Subject, Marks FROM Marks WHERE Student_id=?", (student_id,))
            subjects = cursor.fetchall()

            if not subjects:
                print("\nNo marks entered yet.")
                return

            total = sum(m[1] for m in subjects)
            count = len(subjects)
            average = total / count
            grade = calculate_grade(average)
            if average >= 40:
                print("Eligible for Next Class: Yes")
            else:
                print("Eligible for Next Class: No")


            print("\n--- Subject Marks ---")
            for subject, marks in subjects:
                print(f"{subject}: {marks}")

            print(f"\nTotal Marks: {total}")
            print(f"Average Marks: {average:.2f}")
            print(f"Grade: {grade}")

        else:
            print("Invalid student credentials.")
    except Exception as e:
        print("Error during student login:", e)

# Teacher Registration
def register_teacher():
    try:
        print("\n--- Teacher Registration ---")
        username = input("Username: ")
        password = input("Password: ")

        cursor.execute("INSERT INTO Teachers (Username, Password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Teacher registered successfully!\n")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    except Exception as e:
        print(f"Error: {e}")

# Teacher Login
def teacher_login():
    try:
        print("\n--- Teacher Login ---")
        username = input("Username: ")
        password = input("Password: ")

        cursor.execute("SELECT * FROM Teachers WHERE Username=? AND Password=?", (username, password))
        teacher = cursor.fetchone()

        if teacher:
            print("Teacher login successful!")
            while True:
                print("\n--- Teacher Menu ---")
                print("1. Add/Update Student Marks")
                print("2. View Passed Students")
                print("3. View Failed Students")
                print("4. Logout")
                choice = input("Enter your choice: ")

                if choice == '1':
                    update_student_marks()
                elif choice == '2':
                    view_students(True)
                elif choice == '3':
                    view_students(False)
                elif choice == '4':
                    print("Logging out.")
                    break
                else:
                    print("Invalid choice.")
        else:
            print("Invalid teacher credentials.")
    except Exception as e:
        print("Error during teacher login:", e)

# Teacher updates marks for a student
def update_student_marks():
    try:
        username = input("Enter student username: ")
        cursor.execute("SELECT ID FROM Students WHERE Username=?", (username,))
        student = cursor.fetchone()

        if not student:
            print("Student not found.")
            return

        student_id = student[0]
        print("Enter marks for subjects (type 'done' to finish):")
        while True:
            subject = input("Subject name: ")
            if subject.lower() == 'done':
                break
            marks = int(input(f"Marks for {subject}: "))
            # Insert or update the marks
            cursor.execute('''
                INSERT INTO marks (student_id, Subject, Marks)
                VALUES (?, ?, ?)
                ON CONFLICT(student_id, Subject) 
                DO UPDATE SET Marks=excluded.Marks
            ''', (student_id, subject, marks))
            conn.commit()
            print(f"Marks for '{subject}' updated.")
    except Exception as e:
        print("Error updating marks:", e)

#View students Passed or Failed
def view_students(passed=True):
    try:
        cursor.execute("SELECT ID, Firstname, Lastname FROM Students")
        students = cursor.fetchall()
        count = 0

        print(f"\n--- {'Passed' if passed else 'Failed'} Students ---")
        for student_id, fname, lname in students:
            cursor.execute("SELECT Marks FROM Marks WHERE Student_id=?", (student_id,))
            marks_data = cursor.fetchall()

            if not marks_data:
                continue

            total = sum([m[0] for m in marks_data])
            average = total / len(marks_data)

            if is_eligible(average) == passed:
                print(f"{fname} {lname} - Average: {average:.2f}")
                count += 1

        print(f"\nTotal {'Passed' if passed else 'Failed'} Students: {count}")
    except Exception as e:
        print("Error viewing students:", e)

# Main menu loop
def run():
    while True:
        print("\n===== Student Grading Management System =====")
        print("1. Register as Student")
        print("2. Login as Student")
        print("3. Register as Teacher")
        print("4. Login as Teacher")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            register_student()
        elif choice == '2':
            student_login()
        elif choice == '3':
            register_teacher()
        elif choice == '4':
            teacher_login()
        elif choice == '5':
            print("Exit!")
            break
        else:
            print("Invalid choice. Try again.")
run()
