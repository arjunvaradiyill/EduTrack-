import mysql.connector
import csv

# Database connection functions
def connect_server():
    """Connect to the MySQL server."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="2065"  # Replace with your MySQL password
    )
    return conn

def create_database():
    """Create the `student_management` database if it doesn't exist."""
    conn = connect_server()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS student_management")
    print("Database `student_management` created (or already exists).")
    conn.close()

def connect_db():
    """Connect to the `student_management` database."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="2065",  # Replace with your MySQL password
        database="student_management"
    )
    return conn

def create_tables():
    """Create the required tables: `students`, `attendance`, and `grades`."""
    conn = connect_db()
    cursor = conn.cursor()

    # Create Students Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            dob DATE,
            email VARCHAR(255),
            phone VARCHAR(20)
        )
    ''')

    # Create Attendance Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            date DATE,
            status VARCHAR(50),
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    ''')

    # Create Grades Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            course VARCHAR(255),
            grade VARCHAR(10),
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Tables created successfully.")

# Functionalities

def add_student():
    """Add a new student."""
    name = input("Enter student's name: ")
    dob = input("Enter student's DOB (YYYY-MM-DD): ")
    email = input("Enter student's email: ")
    phone = input("Enter student's phone number: ")

    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO students (name, dob, email, phone) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, dob, email, phone))
    conn.commit()
    conn.close()
    print("Student added successfully!")

def view_students():
    """View all students."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    print("\nStudents:")
    print("ID | Name | DOB | Email | Phone")
    
    for student in students:
        # Extract student information
        student_id, name, dob, email, phone = student
        
        # Convert 'dob' to string in the format 'YYYY-MM-DD'
        if dob:
            dob_str = dob.strftime('%Y-%m-%d')
        else:
            dob_str = "N/A"  # Handle cases where dob might be None
        
        print(f"{student_id} | {name} | {dob_str} | {email} | {phone}")

    conn.close()

def modify_student():
    """Modify an existing student's details."""
    student_id = int(input("Enter student ID to modify: "))
    name = input("Enter new name (or press enter to keep current): ")
    dob = input("Enter new DOB (YYYY-MM-DD) (or press enter to keep current): ")
    email = input("Enter new email (or press enter to keep current): ")
    phone = input("Enter new phone number (or press enter to keep current): ")

    # Prepare the SQL query
    query = "UPDATE students SET "
    values = []

    if name:
        query += "name = %s, "
        values.append(name)
    if dob:
        query += "dob = %s, "
        values.append(dob)
    if email:
        query += "email = %s, "
        values.append(email)
    if phone:
        query += "phone = %s, "
        values.append(phone)

    query = query.rstrip(', ')  # Remove the last comma
    query += " WHERE id = %s"
    values.append(student_id)

    # Execute the query to update the student details
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, tuple(values))
    conn.commit()
    conn.close()
    print(f"Student with ID {student_id} updated successfully!")

def mark_attendance():
    """Mark attendance for a student."""
    student_id = int(input("Enter student ID: "))
    date = input("Enter date (YYYY-MM-DD): ")
    status = input("Enter status (Present/Absent): ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)", (student_id, date, status))
    conn.commit()
    conn.close()
    print("Attendance marked successfully!")

def view_attendance():
    """View attendance records."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    attendance = cursor.fetchall()
    print("\nAttendance Records:")
    print("ID | Student ID | Date | Status")
    for record in attendance:
        print(record)
    conn.close()

def add_grade():
    """Add a grade for a student."""
    student_id = int(input("Enter student ID: "))
    course = input("Enter course name: ")
    grade = input("Enter grade: ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO grades (student_id, course, grade) VALUES (%s, %s, %s)", (student_id, course, grade))
    conn.commit()
    conn.close()
    print("Grade added successfully!")

def view_grades():
    """View grades of all students."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grades")
    grades = cursor.fetchall()
    print("\nGrades:")
    print("ID | Student ID | Course | Grade")
    for record in grades:
        print(record)
    conn.close()

def export_to_csv():
    """Export all tables to CSV files."""
    conn = connect_db()
    cursor = conn.cursor()

    # Export Students
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "DOB", "Email", "Phone"])
        writer.writerows(students)

    # Export Attendance
    cursor.execute("SELECT * FROM attendance")
    attendance = cursor.fetchall()
    with open("attendance.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Student ID", "Date", "Status"])
        writer.writerows(attendance)

    # Export Grades
    cursor.execute("SELECT * FROM grades")
    grades = cursor.fetchall()
    with open("grades.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Student ID", "Course", "Grade"])
        writer.writerows(grades)

    conn.close()
    print("Data exported to CSV files successfully!")

# Menu-Driven Program
def menu():
    while True:
        print("\nMenu:")
        print("1. Create Database")
        print("2. Create Tables")
        print("3. Add Student")
        print("4. View Students")
        print("5. Modify Student")
        print("6. Mark Attendance")
        print("7. View Attendance")
        print("8. Add Grade")
        print("9. View Grades")
        print("10. Export Data to CSV")
        print("11. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            create_database()
        elif choice == "2":
            create_tables()
        elif choice == "3":
            add_student()
        elif choice == "4":
            view_students()
        elif choice == "5":
            modify_student()
        elif choice == "6":
            mark_attendance()
        elif choice == "7":
            view_attendance()
        elif choice == "8":
            add_grade()
        elif choice == "9":
            view_grades()
        elif choice == "10":
            export_to_csv()
        elif choice == "11":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

# Main Script Execution
if __name__ == "__main__":
    menu()
