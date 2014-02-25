import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

def get_project_by_title(title):
    query = """SELECT title, description FROM projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Project Title: %s
Description: %s"""%(row[1], row[2])

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) VALUES (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Succesfully added project: %s" % (title)

def get_grade_by_project(project_title, first_name, last_name):
    query = """SELECT Students.first_name, students.last_name, grades.project_title, grades.grade
        FROM STUDENTS
        INNER JOIN Grades ON (Students.github=Grades.student_github)
        WHERE grades.project_title = ? AND students.first_name = ? AND students.last_name = ?"""
    DB.execute(query, (project_title, first_name, last_name))
    row = DB.fetchone()
    print """\
Project Title: %s
Student: %s %s
Grade: %d"""%(row[2], row[0], row[1], row[3]) 


def get_all_grades_by_project(title):
    query = """SELECT first_name, last_name, grade FROM Grades 
    JOIN Students 
    WHERE project_title = ?"""
    DB.execute(query, (title,))
    row=DB.fetchall()
    return row

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def new_grade(first_name, last_name, project, grade):
    query = """INSERT INTO grades (student_github, project_title, grade) VALUES ((SELECT github FROM students 
                WHERE last_name = ?), ?, ?)"""
    DB.execute(query,(last_name, project, grade))
    CONN.commit()
    print "Succesfully added grade %r for project %s to %s %s" % (grade, project, first_name, last_name)

def get_grades_by_student(first_name, last_name):
    query = """SELECT project_title, grade FROM grades
        INNER JOIN Students on (Students.github=Grades.student_github)
        WHERE students.first_name = ? AND students.last_name = ?"""
    DB.execute(query, (first_name, last_name))
    row = DB.fetchall()
    return row

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        # tokens_multistring = input_string.split('"')
        # command_multistring = tokens_multistring[0].split()[0]
        

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "get_grade":
            get_grade_by_project(*args)
        elif command == "new_project":
            input_title = raw_input("What is the title? ")
            input_description = raw_input("Description? ")
            input_max_grade = raw_input("Max grade? ")

            make_new_project(input_title,input_description, input_max_grade)    
            
            # Only works if user uses double quotation around description, and the title is one word.
            # make_new_project(tokens_multistring[0].split()[1], tokens_multistring[1], tokens_multistring[2].strip())
        elif command == "get_project":
            get_project_by_title(*args)
        elif command == "new_grade":
            input_project = raw_input("What is the project title? ")
            input_name = raw_input("Student name? ")
            input_grade = raw_input("Grade? ")

            new_grade(input_name.split()[0], input_name.split()[1], input_project, input_grade)
        elif command == "get_grades_by_student":
            get_grades_by_student(*args)

    CONN.close()

if __name__ == "__main__":
    main()


