from flask import Flask, render_template, request, redirect, url_for, current_app, session, jsonify
from datetime import datetime
from werkzeug.utils import secure_filename


from database import Database, Instructor
from models.student import Student
from models.room import Room
from models.classroom import Classroom
from models.people import People
from models.lesson import Lesson
from models.building import Building
from models.faculty import Faculty
from models.assistant import Assistant
from models.club import Club
from models.department import Department
from models.lab import Lab
from models.paper import Paper


import hashlib
import os

UPLOAD_FOLDER = '/static/img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'betterthanoriginalsis'
app.config['BASE_DIR'] = os.path.dirname(__file__)
app.config['UPLOAD_FOLDER'] = app.config['BASE_DIR'] + UPLOAD_FOLDER


@app.route("/")
def home_page():
    """
    This is the first page users get. We will have a login form here.

    :return:
    """
    return render_template("home.html", 
        authenticated = session.get("logged_in"),
        username = "anon" if not session.get("logged_in") else session["person"]["name"],
        person = session.get("person")
        )


@app.route("/add_course")
def add_course():
    """
    This is for professors to add a new course and relevant information about it e.g. date, TA's etc.
    :return:
    """
    return render_template("add_course.html")


@app.route("/grades")
def grades():
    """
    This webpage is intended for all users.
    Students -> Will be able to see their grades
    Assistants -> Will be able to see their grades(for grad level courses) and enter grades for courses they are TA'ing
    Professors -> Will be able to enter grades (choose a course, get a list of students)
    :return:
    """
    return render_template("grades.html")


@app.route("/courses")
def courses():
    """
    This page is common for users.

    If user is student, she will see the courses she is registered to.
    If user is an assistant, she will see the courses she is registered to and she is TA'ing.
    If user is a professor, she will see the courses she is giving.

    :return:
    """
    return render_template("courses.html")


@app.route("/settings")
def user_settings():
    """
    Users will be able to update their profile pictures, phone number etc.

    :return:
    """
    return render_template("settings.html")


@app.route("/exams")
def exams():
    """
    In this page we will show the exam dates for students.
    Same for assistants.

    Professors will see exam dates of their courses and they will be able to update the exam date if it is not
    colliding with another exam date.

    :return:
    """
    return render_template("exams.html")


@app.route("/su", methods = ["GET", "POST"])
def admin_page():
    """
    God mode.
    :return:
    """
    db = Database()

    if request.method == "GET":
        #print(session.get("person").get("admin"), "asdadsd")
        if session.get("person")["admin"]:
            return render_template("admin_page.html", 
                                    faculty_list=db.get_faculties(),
                                    prof_list=db.get_instructors(),
                                    student_list=db.get_students(),
                                    datetime=datetime.now(),
                                    clubs=db.get_clubs_info_astext(),
                                    faculties=db.get_all_faculties(),
                                    departments=db.get_departments_text(),
                                    buildings = db.get_buildings(),
                                    rooms=db.get_rooms(),
                                    instructors=db.get_instructors(),
                                    classrooms=db.get_classrooms(),
                                    assistants=db.get_assistant_info(),
                                    labs = db.get_lab_info(),
                                    labs2 = db.get_all_labs(),
                                    people=db.get_people()
                )
        else:
            return redirect(url_for("home_page"))
    return render_template("admin_page.html")


@app.route("/assistants", methods=["POST", "GET"])
def as_page():
    db = Database()
    assistants = db.get_assistant_info()
    return render_template("assistants.html", assistants=assistants)


@app.route("/assistant_edit", methods=["POST", "GET"])
def assistant_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("as_page"))

    db = Database()
    data = request.form
    if data["button"] == "delete":
        as_keys = request.form.getlist("as_id")
        for as_key in as_keys:
            db.delete_assistant(int(as_key))
    elif data["button"] == "update":
        try:
            assistant = db.get_assistant(request.form.getlist("as_id")[0])
            people = db.get_people()
            labs = db.get_all_labs()
            deps = db.get_all_departments()
            facs = db.get_faculties()
            return render_template("assistant_edit.html",
                                   assistant=assistant,
                                   labs=labs,
                                   deps=deps,
                                   facs=facs,
                                   people=people)
        except:
            return redirect(url_for("as_page"))
    else:
        pass

    return redirect(url_for("as_page"))


@app.route("/as_edit", methods=["POST", "GET"])
def as_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("as_page"))
    db = Database()
    data = request.form
    attrs = ["person", "lab", "degree", "department", "faculty"]
    values = [data["p_id"], data["lab_id"], data["deg"], data["dep_id"], data["fac_id"]]
    db.update_assistant(data["id"], attrs, values)

    return redirect(url_for("as_page"))


@app.route("/as_create", methods=["POST", "GET"])
def as_cr():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("as_page"))
    db = Database()
    data = request.form
    assistant = Assistant(data["p_id"], data["lab_id"], data["deg"], data["dep_id"], data["fac_id"])
    db.add_assistant(assistant)
    return redirect(url_for("as_page"))


@app.route("/buildings", methods=["POST", "GET"])
def bu_page():
    db = Database()
    buildings = db.get_buildings()
    return render_template("buildings.html", buildings=buildings)


@app.route("/building_edit", methods=["POST", "GET"])
def building_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("bu_page"))

    db = Database()
    data = request.form
    if data["button"] == "delete":
        bu_keys = request.form.getlist("bu_id")
        for bu_key in bu_keys:
            db.delete_building(int(bu_key))
    elif data["button"] == "update":
        try:
            building = db.get_building(request.form.getlist("bu_id")[0])
            print(building)
            return render_template("building_edit.html",
                                   building=building[0])
        except:
            return redirect(url_for("bu_page"))
    else:
        pass

    return redirect(url_for("bu_page"))


@app.route("/bu_edit", methods=["POST", "GET"])
def bu_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("bu_page"))
    db = Database()
    data = request.form
    attrs = ["name", "code", "campus"]
    values = [data["name"], data["code"], data["campus"]]
    db.update_building(data["id"], attrs, values)

    return redirect(url_for("bu_page"))

@app.route("/building_create", methods=["POST", "GET"])
def bu_cr():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("bu_page"))
    db = Database()
    data = request.form
    building = Building(data["name"], data["code"], data["campus"])
    db.add_building(building)

    return redirect(url_for("bu_page"))

@app.route("/club_create", methods=["POST", "GET"])
def club_create():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("cl_page"))
    db = Database()
    data = request.form
    club = Club(data["name"], data["fac_id"], data["adv_id"], data["ch_id"], data["v1_id"], data["v2_id"])
    db.add_club(club)
    return redirect(url_for("cl_page"))


@app.route("/clubs", methods=["POST", "GET"])
def cl_page():
    db = Database()
    clubs = db.get_clubs_info_astext()
    return render_template("clubs.html", clubs=clubs)


@app.route("/club_edit", methods=["POST", "GET"])
def club_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("cl_page"))

    db = Database()
    data = request.form
    if data["button"] == "delete":
        cl_keys = request.form.getlist("cl_id")
        for cl_key in cl_keys:
            db.delete_club(int(cl_key))
    elif data["button"] == "update":
        try:
            people = db.get_people()
            faculty = db.get_all_faculties()
            club = db.get_club(request.form.getlist("cl_id")[0])[0]
            return render_template("club_edit.html",
                                   faculties=faculty,
                                   club=club,
                                   people=people)
        except:
            return redirect(url_for("cl_page"))
    else:
        pass

    return redirect(url_for("cl_page"))


@app.route("/cl_edit", methods=["POST", "GET"])
def cl_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("cl_page"))
    db = Database()
    data = request.form
    attrs = ["name", "faculty", "advisor", "chairman", "vice_1", "vice_2"]
    values = [data["name"], data["fac_id"], data["adv_id"], data["ch_id"], data["v1_id"], data["v2_id"]]
    db.update_club(data["id"], attrs, values)
    return redirect(url_for("cl_page"))


@app.route("/dep_create", methods=["POST", "GET"])
def dep_create():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("dep_page"))
    db = Database()
    data = request.form
    dep= Department(data["name"], data["fac_id"], data["bu_id"], data["ch_id"])
    db.add_department(dep)
    return redirect(url_for("dep_page"))


@app.route("/departments", methods=["POST", "GET"])
def dep_page():
    db = Database()
    departments = db.get_departments_text()
    return render_template("departments.html", departments=departments)


@app.route("/department_edit", methods=["POST", "GET"])
def department_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("dep_page"))

    db = Database()
    data = request.form
    if data["button"] == "delete":
        dep_keys = request.form.getlist("dep_id")
        for dep_key in dep_keys:
            db.delete_department(int(dep_key))
    elif data["button"] == "update":
        try:
            people = db.get_people()
            faculties = db.get_all_faculties()
            department = db.get_department(request.form.getlist("dep_id")[0])[0]
            return render_template("department_edit.html",
                                   faculties=faculties,
                                   people=people,
                                   buildings=db.get_buildings(),
                                   dep=department)
        except:
            return redirect(url_for("dep_page"))
    else:
        pass

    return redirect(url_for("dep_page"))


@app.route("/dep_edit", methods=["POST", "GET"])
def dep_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("dep_page"))
    db = Database()
    data = request.form
    attrs = ["name", "faculty", "building", "dean"]
    values = [data["name"], data["fac_id"], data["bu_id"], data["ch_id"]]
    db.update_department(data["id"], attrs, values)
    return redirect(url_for("dep_page"))


@app.route("/faculties", methods=["POST", "GET"])
def fac_page():
    db = Database()
    faculties = db.get_faculty_as_text()
    return render_template("faculties.html", faculties=faculties)


@app.route("/faculty_edit", methods=["POST", "GET"])
def faculty_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("fac_page"))

    db = Database()
    data = request.form
    if data["button"] == "delete":
        fac_keys = request.form.getlist("fac_id")
        for fac_key in fac_keys:
            db.delete_faculty(int(fac_key))
    elif data["button"] == "update":
        try:
            people = db.get_people()
            buildings = db.get_buildings()
            faculty = db.get_faculty(request.form.getlist("fac_id")[0])[0]
            return render_template("faculty_edit.html",
                                   faculty=faculty,
                                   buildings=buildings,
                                   people=people)
        except:
            return redirect(url_for("fac_page"))
    else:
        pass

    return redirect(url_for("fac_page"))


@app.route("/fac_edit", methods=["POST", "GET"])
def fac_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("fac_page"))
    db = Database()
    data = request.form
    attrs = ["name", "building", "dean", "vdean_1", "vdean_2"]
    values = [data["name"], data["b_id"], data["dean_id"], data["vdean1_id"]]
    if data["vdean2_id"] != "0":
        values.append(data["vdean2_id"])
    else:
        values.append(None)
    db.update_faculty(data["id"], attrs, values)



    return redirect(url_for("fac_page"))


@app.route("/fac_create", methods=["POST", "GET"])
def fac_cr():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("fac_page"))
    db = Database()
    data = request.form
    a = None
    if data["vdean2_id"] != "0":
        a = data["vdean2_id"]
    fac = Faculty(data["name"], data["b_id"], data["dean_id"], data["vdean1_id"], a)
    db.add_faculty(fac)
    return redirect(url_for("fac_page"))


@app.route("/lab_create", methods=["POST", "GET"])
def lab_create():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("lab_page"))
    db = Database()
    data = request.form
    lab = Lab(data["name"], data["dep_id"], data["fac_id"], data["r_id"], data["p_id"], data["bu_id"])
    db.add_lab(lab)
    return redirect(url_for("lab_page"))

@app.route("/labs", methods=["POST", "GET"])
def lab_page():
    db = Database()
    labs = db.get_lab_info()
    return render_template("labs.html", labs=labs)


@app.route("/lab_edit", methods=["POST", "GET"])
def lab_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("lab_page"))

    db = Database()
    data = request.form
    if data["button"] == "delete":
        lab_keys = request.form.getlist("lab_id")
        for lab_key in lab_keys:
            db.delete_lab(int(lab_key))
    elif data["button"] == "update":
        try:
            return render_template("lab_edit.html",
                                   people = db.get_people(),
                                   deps=db.get_all_departments(),
                                   faculties = db.get_all_faculties(),
                                   buildings = db.get_buildings(),
                                   rooms = db.get_rooms(),
                                   lab = db.get_lab(request.form.getlist("lab_id")[0])[0])
        except:
            return redirect(url_for("lab_page"))
    else:
        pass

    return redirect(url_for("lab_page"))


@app.route("/l_edit", methods=["POST", "GET"])
def l_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("lab_page"))
    db = Database()
    data = request.form
    attrs = ["name", "department", "faculty", "building", "room", "investigator"]
    values = [data["name"], data["dep_id"], data["fac_id"], data["bu_id"], data["r_id"], data["p_id"]]
    db.update_lab(data["id"], attrs, values)
    return redirect(url_for("lab_page"))


@app.route("/papers", methods=["POST", "GET"])
def paper_page():
    db = Database()
    authors = db.get_authors()
    if request.method == "GET":
        return render_template("papers.html", authors=authors)
    else:
        data = request.form
        try:
            papers = db.get_paper_by_author(int(data["a_id"]))
            return render_template("papers.html", authors=authors, papers=papers)
        except:
            return render_template("papers.html", authors=authors)


@app.route("/paper_edit", methods=["POST", "GET"])
def paper_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("paper_page"))

    db = Database()
    data = request.form
    if data["button"] == "delete":
        p_keys = request.form.getlist("paper_id")
        for p_key in p_keys:
            db.delete_paper(int(p_key))
    elif data["button"] == "update":
        try:
            return render_template("paper_edit.html",
                                   people = db.get_people(),
                                   paper = db.get_paper(request.form.getlist("paper_id")[0])[0])
        except:
            return redirect(url_for("paper_page"))
    else:
        pass

    return redirect(url_for("paper_page"))


@app.route("/p_edit", methods=["POST", "GET"])
def p_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("paper_page"))
    db = Database()
    data = request.form
    attrs = ["title", "platform", "citation", "author", "isConference"]
    values = [data["name"], data["pl"], data["cc"], data["a_id"]]
    if data["conf"] == "t":
        values.append(True)
    else:
        values.append(False)
    db.update_paper(data["id"], attrs, values)
    return redirect(url_for("paper_page"))

@app.route("/paper_create", methods=["POST", "GET"])
def paper_create():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("paper_page"))
    db = Database()
    data = request.form
    h = False
    if data["conf"] == "t":
        h = True
    paper = Paper(data["name"], data["pl"], data["cc"], data["a_id"], h)
    db.add_paper(paper)
    return redirect(url_for("paper_page"))

@app.route("/rooms_list", methods = ["GET", "POST"])
def rooms_page():
    '''
    In this page we will show the rooms
    :return:
    '''
    db = Database()
    rooms = db.get_rooms()
    return render_template("rooms_list.html", rooms = rooms)


@app.route("/room_create", methods= ["POST", "GET"])
def room_create():
    db = Database()
    data = request.form
    is_class = 'FALSE'
    is_room = 'FALSE'
    is_lab = 'FALSE'
    if data["type"] == "class":
        is_class = 'TRUE'
    elif data["type"] == "room":
        is_room = 'TRUE'
    elif data["type"] == "lab":
        is_lab = 'TRUE'
    room = Room(data["building"], data["name"], data["availability"], is_class, is_room, is_lab)
    db.add_room(room)
    return redirect(url_for("admin_page"))


@app.route("/room_edit", methods= ["POST", "GET"])
def room_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("home_page"))

    db = Database()
    data = request.form
    if data["button"] == "delete":
        room_keys = request.form.getlist("room_keys")
        for room_key in room_keys:
            db.delete_classroom(int(room_key))
    elif data["button"] == "update":
        room = db.get_room(request.form.getlist("room_keys")[0])
        return render_template("room_update.html", room=room, buildings=db.get_buildings())
    else:
        pass
    return redirect(url_for("rooms_page"))


@app.route("/room_update", methods= ["POST", "GET"])
def room_update():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("home_page"))

    db = Database()
    data = request.form
    attrs = ["room_name","building","class", "lab" ,"room" ,"available"]
    classFlag = labFlag = roomFlag = "FALSE"
    if data["type"] == "class":
        classFlag = "TRUE"
    elif data["type"] == "lab":
        labFlag = "TRUE"
    elif data["type"] == "room":
        roomFlag = "TRUE"
    values = [data["name"], data["building"], classFlag, labFlag, roomFlag, data["availability"]]
    db.update_room(data["id"], attrs, values)
    return redirect(url_for("rooms_page"))


@app.route("/classrooms_list", methods = ["GET", "POST"])
def classrooms_page():
    '''
    In this page we will show the classrooms
    :return:
    '''
    db = Database()
    classrooms = db.get_classrooms()
    return render_template("classrooms_list.html", classrooms = classrooms)

@app.route("/classroom_create", methods= ["POST", "GET"])
def classroom_create():
    db = Database()
    data = request.form
    newroom = Room(data["building"], data["name"], data["availability"], classroom="TRUE",lab="FALSE",room="FALSE")
    room = db.add_room(newroom)

    classroom = Classroom(room.id, room.name, room.building, data["type"], data["restoration_date"], data["capacity"], data["conditioner"], data["board_type"])
    db.add_classroom(classroom)
    return redirect(url_for("admin_page"))

@app.route("/classroom_edit", methods= ["POST", "GET"])
def classroom_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("home_page"))

    db = Database()
    data = request.form
    if data["button"] == "delete":
        classroom_keys = request.form.getlist("classroom_keys")
        for classroom_key in classroom_keys:
            db.delete_classroom(int(classroom_key))
    elif data["button"] == "update":
        classroom = db.get_classroom(request.form.getlist("classroom_keys")[0])
        return render_template("classroom_update.html", classroom=classroom, datetime=datetime.now())
    else:
        pass
    return redirect(url_for("classrooms_page"))

@app.route("/classroom_update", methods= ["POST", "GET"])
def classroom_update():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("home_page"))

    db = Database()
    data = request.form
    attrs = ["type","air_conditioner","last_restoration" ,"board_type" ,"cap"]
    values = [data["type"], data["conditioner"], data["restoration_date"], data["board_type"], data["capacity"]]
    db.update_classroom(data["id"], attrs, values)
    return redirect(url_for("classrooms_page"))

@app.route("/instructors", methods = ["GET", "POST"])
def instructors_page():
    '''
    In this page we will show the instructors
    :return:
    '''
    db = Database()
    instructors = db.get_instructors()

    return render_template("instructors.html", instructors = instructors)

@app.route("/instructor_create", methods= ["POST", "GET"])
def instructor_create():
    db = Database()
    data = request.form
    password = hashlib.md5(data["password"].encode())
    person = People(name=data["name"], password=password.hexdigest(), mail=data["mail"])
    db.add_person(person) 
    instructor = Instructor(person.id, data["name"], data["bachelors"], data["masters"], data["doctorates"], data["department"], data["room"], data["lab"])
    db.add_instructor(instructor)
    return redirect(url_for("admin_page"))

@app.route("/instructor_edit", methods= ["POST", "GET"])
def instructor_edit():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("home_page"))
    db = Database()
    data = request.form
    if data["button"] == "delete":
        instructor_keys = request.form.getlist("instructor_keys")
        for ins_key in instructor_keys:
            db.delete_instructor(int(ins_key))
    elif data["button"] == "update":
        instructor = db.get_instructor(request.form.getlist("instructor_keys")[0])
        return render_template("instructor_update.html", instructor=instructor, rooms=db.get_rooms(), departments=db.get_all_departments(), labs=db.get_all_labs())
    else:
        pass
    return redirect(url_for("instructors_page"))

@app.route("/instructor_update", methods= ["POST", "GET"])
def instructor_update():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("home_page"))
    db = Database()
    data = request.form
    attrs = ["department", "room", "lab", "bachelors", "masters", "doctorates"]
    lab = data["lab"]
    if data["lab"] == "":
        lab = None
    values = [data["department"], data["room"], lab, data["bachelors"], data["masters"], data["doctorates"]]
    db.update_instructor(data["id"], attrs, values)
    return redirect(url_for("instructors_page"))

@app.route("/student_create", methods= ["POST", ])
def student_create():
    db = Database()
    data = request.form

    password = hashlib.md5(data["password"].encode()).hexdigest()

    file = request.files["pic"]

    if file and file.filename[-3:] in ALLOWED_EXTENSIONS:
        basedir = os.path.abspath(os.path.dirname(__file__))
        filename = secure_filename(file.filename[:-4] + data["mail"][:-4] + file.filename[-4:])
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    if not file:
        filename = "defaultpfp.jpg"

    student = Student(data["name"], data["number"], data["mail"], data["cred"], data["depart"], data["facu"], data["club"], data["lab"], password, filename)
    db.add_student(student)
    return redirect(url_for("admin_page"))

@app.route("/student_list", methods = ["GET", ])
def students_list():
    if not session["logged_in"]:
        return redirect(url_for("home_page"))

    db = Database()
    students = db.get_students()

    return render_template("students_list.html", 
        students = students,
        person = session.get("person")
        )

@app.route("/student_delete_update", methods = ["POST", ])
def student_delete_update():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("home_page"))

    data = request.form
    db = Database()
    
    if data["button"] == "delete":
        students = data.getlist("selected")
        for stu in students:
            db.delete_student(int(stu))
    elif data["button"] == "update":
        return render_template("student_update.html",
            student = db.get_student_w_join(int(data.getlist("selected")[0]))
            )

    return redirect(url_for("students_list"))

@app.route("/student_update", methods = ["POST", ])
def student_update():
    if not session["logged_in"] or not session.get("person")["admin"]:
        return redirect(url_for("home_page"))

    data = request.form
    db = Database()

    attrs = ["NUMBER", "EARNED_CREDITS"]
    values = [int(data["number"]), data["credit"]]

    db.update_student(data["id"], attrs, values)

    attrs = ["NAME", "EMAIL"]
    values = [data["name"], data["email"]]

    db.update_person(data["id"], attrs, values)

    return redirect(url_for("students_list"))

@app.route("/login", methods = ["GET", ])
def login_page():
    return render_template("login_page.html")

@app.route("/login_action", methods = ["POST", ])
def login_action():
    data = request.form
    
    db = Database()
    person = db.get_person_by_mail(data["mail"])

    attempted_hashed_passw = hashlib.md5(data["password"].encode()).hexdigest()

    if not person or person.password != attempted_hashed_passw:
        return redirect(url_for("login_page"))

    session["logged_in"] = 1
    session["person"] = vars(person)
    return redirect(url_for("home_page")) 

@app.route("/logout", methods = ["GET", ])
def logout():
    if session["logged_in"]:
        session["logged_in"] = 0
        session["person"] = None

    return redirect(url_for("home_page"))

@app.route("/lesson_create", methods = ["POST", ])
def lesson_create():
    data = request.form
    lesson = Lesson(data["crn"], data["date"], data["code"], data["instructor"], data["location"], data["assistant"], data["credit"], data["cap"])
    db = Database()
    db.create_lesson(lesson)

    return redirect(url_for("admin_page"))

@app.route("/enroll", methods = ["GET", "POST"])
def enroll_page():
    db = Database()
    enrolled_list = db.get_enrolled(session.get("person")["id"])
    enrolled = []
    for enr in enrolled_list:
        enrolled.append(enr[2])

    if request.method == "GET":
        if not session["logged_in"]:
            return redirect(url_for("login_page"))

        return render_template("enroll_page.html",
            authenticated = session.get("logged_in"),
            username = "anon" if not session.get("logged_in") else session["person"]["name"],
            person = session.get("person"),
            enrolled = enrolled
            )

    else:
        data = request.form
        if data["type"] == "1": # searched by CRN
            result = db.search_lesson_by_crn(data["value"])
        else:
            result = db.search_lesson_by_instructor(data["value"])

        return render_template("enroll_page.html",
            authenticated = session.get("logged_in"),
            username = "anon" if not session.get("logged_in") else session["person"]["name"],
            person = session.get("person"),
            result = result,
            enrolled = enrolled
            )


@app.route("/enroll_action", methods = ["GET", ])
def enroll_action():
    lesson_id = request.args.get("lesson_id")
    if not lesson_id or not session["logged_in"]:
        return redirect(url_for("home_page"))

    db = Database()
    enrollments = db.get_enrolled(session["person"]["id"])
    for enr in enrollments:
        if enr[2] == lesson_id:
            return redirect(url_for("enroll_page"))

    if db.enroll_for_student(student_id = session["person"]["id"], lesson_id = lesson_id):
        return jsonify({"Success": True})

    return jsonify({"Success": False})

@app.route("/leave_action", methods = ["GET", ])
def leave_action():
    lesson_id = request.args.get("lesson_id")
    if not lesson_id or not session["logged_in"]:
        return redirect(url_for("home_page"))

    db = Database()
    if db.leave_for_student(student_id = session["person"]["id"], lesson_id = lesson_id):
        return jsonify({"Success": True})

    return jsonify({"Success": False})

@app.route("/schedule", methods = ["GET", ])
def schedule():
    if not session["logged_in"] or session.get("person")["type"] != "student":
        return redirect(url_for("home_page"))


    db = Database()
    enrollments = db.get_enrolled_w_join(session["person"]["id"])

    return render_template("schedule.html",
            authenticated = session.get("logged_in"),
            username = "anon" if not session.get("logged_in") else session["person"]["name"],
            person = session.get("person"),
            enrollments = enrollments
            )

if __name__ == "__main__":
    app.run(debug=True)
