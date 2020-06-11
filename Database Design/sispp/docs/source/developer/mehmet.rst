Parts Implemented by Mehmet Altuner
================================

*****************
People
*****************

.. note:: All table creations exist in db_init.py file.
.. note:: All SQL operations in python files are wrapped with try-except statements in order to avoid and validate errors

1. Creation
~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: sql

	CREATE TABLE IF NOT EXISTS PEOPLE (
    P_ID SERIAL PRIMARY KEY,
    NAME VARCHAR(100),
    EMAIL VARCHAR(120) UNIQUE,
    PHOTO VARCHAR(120),
    PASSWORD VARCHAR(280),
    TYPE VARCHAR(120)
	)

2. Adding 
~~~~~~~~~~~~~~~~~~~~~~~~
Adding new person is handled in *add_person()* method in *database.py* file

.. code-block:: python

	def add_person(self, person):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO PEOPLE (NAME, EMAIL, PHOTO, PASSWORD, TYPE) VALUES (%s, %s, %s, %s, %s)"
                data = [person.name, person.mail, person.photo, person.password, person.type]
                cursor.execute(statement, data)
                statement = "SELECT P_ID FROM PEOPLE WHERE EMAIL = %s"
                data = [person.mail]
                cursor.execute(statement, data)
                value = cursor.fetchone()
                person.id = value[0]
                cursor.close()
        except Exception as err:
            print("Add Person Error : ", err)

        return person

*add_person()* method takes a *people* object as a parameter named *person*. (Person object is defined in models/people.py).
After inserting the new value into the table, its auto-incremented id instance is selected by another statement and written into the person instance to be used in the future.

.. warning:: The email instance is unique

3. Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

Reading from person table is implemented in the method *get_person()* in *database.py* file.

.. code-block:: python

	def get_person(self, p_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM PEOPLE WHERE P_ID = %s"
                data = [p_id]
                cursor.execute(statement, data)
                value = cursor.fetchone()
                cursor.close()
                if not value:
                    return None
                person = People(value[0], value[1], value[2], value[3])
                return person
        except Exception as err:
            print("Error: ", err)

        return None

*get_person()* method takes an integer named *p_id* and returns the data of the column having the id equal to*p_id*.

4. Updating 
~~~~~~~~~~~~~~~~~~~~~~~~

Deleting operation is handled in the method *update_person()* in *database.py* file.

.. code-block:: python

	def update_person(self, person_id, attrs, values):
        person = self.get_person(person_id)
        if not person:
            return False

        if person:
            try:
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    statement = "UPDATE PEOPLE SET "
                    for attr in attrs[:-1]:
                        statement += attr + " = %s , "
                    statement += attrs[-1] + " = %s "
                    statement += " WHERE p_id = %s"
                    values.append(person_id)
                    cursor.execute(statement, values)
                    cursor.close()
            except Exception as err:
                print("Update Person Error: ", err)

The structure of this method is a bit different than other operations' methods. It takes three parameters:
	- person_id: An integer that states the person column to be updated.
	- attrs: A list of names of the attributes that we want to update.
	- values: The new values of the person object.

The idea is that each instance of list *attr* must coincide with the each instance of the list *values*. 
*UPDATE PEOPLE SET person.attrs[i] = values[i] where id = p_id*

4. Deleting 
~~~~~~~~~~~~~~~~~~~~~~~~
By the nature of the table itself, there is no need to implement a deletion operation for this table. It is simply a base class. We have stated *ON DELETE CASCADE* on each table we reference people from.

*****************
Students
*****************

1. Creation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS STUDENTS (
    STU_ID INTEGER PRIMARY KEY ,
    NUMBER INTEGER,
    EARNED_CREDITS INTEGER,
    DEPARTMENT INTEGER NOT NULL,
    FACULTY INTEGER NOT NULL,
    CLUB INTEGER,
    LAB INTEGER,
    FOREIGN KEY (STU_ID) REFERENCES PEOPLE ON DELETE CASCADE,
    FOREIGN KEY (DEPARTMENT) REFERENCES DEPARTMENTS,
    FOREIGN KEY (FACULTY) REFERENCES FACULTIES,
    FOREIGN KEY (CLUB) REFERENCES CLUBS,
    FOREIGN KEY (LAB) REFERENCES LABS
    )

.. warning:: Student's pkey is also the fkey for the People table since People can only be students if they are students.

2. Adding 
~~~~~~~~~~~~~~~~~~~~~~~~

Adding operation is handled in the method *add_student()* in *database.py* file.

.. code-block:: python

	def add_student(self, student):
        person = self.add_person(student.get_person_obj())
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()

                statement = "INSERT INTO STUDENTS (STU_ID, NUMBER, EARNED_CREDITS, DEPARTMENT, FACULTY, CLUB, LAB) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                data = [person.id, student.number, student.cred, student.depart, student.facu, student.club,
                        student.lab]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Error: ", err)

3. Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

Reading operation is handled in the method *get_student()* in *database.py* file.

.. code-block:: python

	def get_student(self, stu_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM STUDENTS WHERE STU_ID = %s"
                values = [stu_id]
                cursor.execute(statement, values)
                data = cursor.fetchone()
                cursor.close()
                return data
        except Exception as err:
            print("Get Student Error: ", err)

        return None

Selects the student that has the id as same as the stu_id which are taken by a parameter.

4. Updating 
~~~~~~~~~~~~~~~~~~~~~~~~

Updating operation is handled in the method *update_student()* in *database.py* file.

.. code-block:: python

	def update_student(self, student_key, attrs, values):
        student = self.get_student(student_key)
        if not student:
            return False

        if student:
            try:
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    statement = "UPDATE STUDENTS SET "
                    for attr in attrs[:-1]:
                        statement += attr + " = %s , "
                    statement += attrs[-1] + " = %s "
                    statement += " WHERE stu_id = %s"
                    values.append(student_key)
                    cursor.execute(statement, values)
                    cursor.close()
            except Exception as err:
                print("Update Student Error: ", err)

The same approach is followed as the update operation of the People table.
*UPDATE STUDENTS SET students.attr[i] = values[i] where stu_id = student_key*

5. Deleting
~~~~~~~~~~~~~~~~~~~~~~~~

Updating operation is handled in the method *delete_student()* in *database.py* file.

.. code-block:: python

	def delete_student(self, student_key):
        student = self.get_student(student_key)

        if student:
            try:
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    statement = "DELETE FROM STUDENTS WHERE stu_id = %s"
                    values = [student_key]
                    cursor.execute(statement, values)
                    cursor.close()
            except Exception as err:
                print("Delete Student Error: ", err)

.. warning:: If you delete a student, the People instance it references to is also deleted.

****************
Lessons
****************

1. Creation
~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: sql

	CREATE TABLE IF NOT EXISTS LESSONS (
	    LESSON_ID SERIAL PRIMARY KEY,
	    CAP INTEGER,
	    ENROLLED INTEGER,
	    DATE VARCHAR(280),
	    CRN INTEGER UNIQUE NOT NULL,
	    CODE VARCHAR(7),
	    INSTRUCTOR INTEGER,
	    LOCATION INTEGER, 
	    ASSISTANT INTEGER,
	    CREDIT INTEGER,
	    FOREIGN KEY (INSTRUCTOR) REFERENCES INSTRUCTORS(INS_ID),
	    FOREIGN KEY (ASSISTANT) REFERENCES ASSISTANTS(AS_ID),
	    FOREIGN KEY (LOCATION) REFERENCES CLASSES(CL_ID)
	    )

2. Adding
~~~~~~~~~~~~~~~~~~~~

Adding operation is handled in the method *create_lesson()* in *database.py* file.

.. code-block:: python

	def create_lesson(self, lesson):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = """INSERT INTO LESSONS (CRN, DATE, CODE, INSTRUCTOR, LOCATION, ASSISTANT, CREDIT, CAP, ENROLLED) 
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                values = [lesson.crn, lesson.date, lesson.code, lesson.instructor, lesson.location, lesson.assistant, lesson.credit, lesson.cap, lesson.enrolled]
                cursor.execute(statement, values)
                cursor.close()
                return True

        except Exception as err:
            print("Create Lesson Error: ", err) 

        return False

3. Reading
~~~~~~~~~~~~~~~~~~~~

Reading operation is handled in the methods *search_lesson_by_crn()* and *search_lesson_by_instructor()* in *database.py* file.
The obvious difference between the methods is that one of them selects the lessons by the given CRN while the other does the same operation with the name of its instructor.

.. code-block:: python

	def search_lesson_by_crn(self, crn):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = """SELECT * FROM LESSONS 
                JOIN INSTRUCTORS ON (LESSONS.instructor = INSTRUCTORS.ins_id) 
                JOIN PEOPLE ON (INSTRUCTORS.ins_id = PEOPLE.p_id)
                JOIN CLASSES ON (LESSONS.location = CLASSES.cl_id)
                WHERE LESSONS.crn = %s
                """
                values = [crn]
                cursor.execute(statement, values)
                data = cursor.fetchall()
                cursor.close()
                return data

        except Exception as err:
            print("Search Lesson Error: ", err) 

        return False

.. code-block:: python

	def search_lesson_by_instructor(self, instructor):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = """SELECT * FROM 
                LESSONS 
                JOIN INSTRUCTORS ON (LESSONS.instructor = INSTRUCTORS.ins_id) 
                JOIN PEOPLE ON (INSTRUCTORS.ins_id = PEOPLE.p_id)
                JOIN CLASSES ON (LESSONS.location = CLASSES.cl_id)
                WHERE PEOPLE.name = %s
                """
                values = [instructor]
                cursor.execute(statement, values)
                data = cursor.fetchall()
                cursor.close()
                return data

        except Exception as err:
            print("Search Lesson Error: ", err)

Here in both of the methods. JOIN operations are used.

