from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_github")
def get_github():
    return render_template("get_github.html")


@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row = hackbright_app.get_student_by_github(student_github)
    row2 = hackbright_app.get_grades_by_student(row[0], row[1])
    html = render_template("student_info.html", first_name=row[0], 
                                                last_name=row[1], 
                                                github=row[2],
                                                grade=row2)
    return html


@app.route("/project")
def get_project():
    hackbright_app.connect_to_db()
    project = request.args.get("projects")
    row = hackbright_app.get_all_grades_by_project(project)
    html = render_template("projects.html", project_name = project,
                                            projects=row)
    return html


@app.route("/create_student")
def create_student():
    html = render_template("create_student.html")
    return html


@app.route("/create_student_complete")
def create_student_complete():
    hackbright_app.connect_to_db()
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    github = request.args.get("github")
    row = hackbright_app.make_new_student(first_name, last_name, github)
    html = render_template("create_student_complete.html", first_name = first_name,
                                                           last_name = last_name,
                                                           github = github)
    return html


@app.route("/create_project")
def create_project():
    html = render_template("create_project.html")
    return html


@app.route("/create_project_complete")
def create_project_complete():
    hackbright_app.connect_to_db()
    title = request.args.get("title")
    description = request.args.get("description")
    max_grade = request.args.get("max_grade")
    row = hackbright_app.make_new_project(title, description, max_grade)
    html = render_template("create_project_complete.html", title = title,
                                                           description = description,
                                                           max_grade = max_grade)
    return html


@app.route("/add_grade")
def add_grade_complete():
    hackbright_app.connect_to_db()
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    project = request.args.get("project")
    grade = request.args.get("grade")
    if project == None:
        html = render_template("add_grade.html", first_name = first_name,
                                                 last_name = last_name,
                                                 project = project,
                                                 grade = grade)
        return html
    else:
        hackbright_app.new_grade(first_name, last_name, project, grade)
        html = render_template("add_grade_complete.html", first_name = first_name,
                                                          last_name = last_name,
                                                          project = project,
                                                          grade = grade)
        return html


# def new_grade(first_name, last_name, project, grade):
#     query = """INSERT INTO grades (student_github, project_title, grade) VALUES ((SELECT github FROM students 
#                 WHERE last_name = ?), ?, ?)"""
#     DB.execute(query, (last_name, project, grade))
#     CONN.commit()
#     print "Succesfully added grade %r for project %s to %s %s" % (grade, project, first_name, last_name)





if __name__ == "__main__":
    app.run(debug=True)