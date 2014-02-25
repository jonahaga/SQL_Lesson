from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("get_github.html")


@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row = hackbright_app.get_student_by_github(student_github)
    # print "THIS IS THE ROW", row
    row2 = hackbright_app.get_grades_by_student(row[0], row[1])
    # print "THIS IS ROW2", row2
    # print "THIS IS ROW2[2]", row2[2]
    # print "THIS IS ROW2[1]", row2[1]
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


if __name__ == "__main__":
    app.run(debug=True)