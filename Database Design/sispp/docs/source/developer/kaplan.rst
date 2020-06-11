Parts Implemented by Uğur Ali Kaplan
=====================================

Assistants
------------------------------

SQL Table Creation
~~~~~~~~~~~~~~~~~~~~~~~~

This is how Assistants table is defined in the database. As we are holding foreign keys, it is impossible to
create an assistant entry before having the right values for foreign key attributes. Related information 
about how to create entries for those tables can be found in the other parts of this documentation.

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS ASSISTANTS (
        AS_ID SERIAL PRIMARY KEY,
        AS_PERSON INTEGER NOT NULL,
        LAB INTEGER,
        DEGREE VARCHAR(10),
        DEPARTMENT INTEGER,
        FACULTY INTEGER,
        FOREIGN KEY (AS_PERSON) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (LAB) REFERENCES LABS(LAB_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (DEPARTMENT) REFERENCES DEPARTMENTS(DEP_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (FACULTY) REFERENCES FACULTIES(FAC_ID) ON UPDATE CASCADE ON DELETE RESTRICT
    )

Assistant Class
~~~~~~~~~~~~~~~~~~~~~~~~

Since it makes it easier to create, we have defined an assistant class for creating an entry into our database.
Therefore, before adding a new assistant an object of class Assistant must be initialized. Here is the definition of
the Assistant class:

.. code-block:: python

    class Assistant:
        def __init__(self, person, lab, degree, department, faculty):
            self.person = person
            self.lab = lab
            self.degree = degree
            self.department = department
            self.faculty = faculty


Adding 
~~~~~~~~~~~~~~~~~~~~~~~~

Adding an assistant into the database is pretty straigthforward. You have to pass the object you have initialized
into add_assistant() function.

.. code-block:: python

   def add_assistant(self, assistant):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [assistant.person, assistant.lab, assistant.degree, assistant.department, assistant.faculty]
                statement = "INSERT INTO ASSISTANTS (AS_PERSON, LAB, DEGREE, DEPARTMENT, FACULTY) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add assistant Error: ", err)


Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

It turns out, reading assistants is not as straigthforward as creating an entry. There are multiple options.

**Option 1: get_assistant**

get_assistant takes assistant id as input and returns a dictionary. It also returns assistant's name, email and photo from people
table.

.. code-block:: python

   def get_assistant(self, as_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT (a.as_id, p.name, p.email, p.photo, a.degree, a.as_person, a.lab, a.department, a.faculty) FROM assistants a JOIN people p ON a.as_person = p.p_id WHERE a.as_id = %s"
                data = [as_id]
                cursor.execute(statement, data)
                data = cursor.fetchall()
                cursor.close()
                retval = []
                for datum in data:
                    datum = datum[0].lstrip("(").rstrip(")").split(",")
                    val = {
                        "ID": datum[0],
                        "Name": datum[1].strip('"'),
                        "Email": datum[2].strip('"'),
                        "Photo": datum[3].strip('"'),
                        "Degree": datum[4].strip('"'),
                        "Person": int(datum[5]),
                        "Lab": int(datum[6]),
                        "Dep": int(datum[7]),
                        "Fac": int(datum[8])
                    }
                    retval.append(val)
                return retval[0]
        except Exception as err:
            print("Get assistant DB Error: ", err)

        return None

**Option 2: get_assistants**

Notice the "s" at the end of the function name. This is used to get all the assistants in the database.
It returns the query result as a list.

.. code-block:: python

   def get_assistants(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM ASSISTANTS JOIN PEOPLE ON (ASSISTANTS.as_person = PEOPLE.p_id)"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                return data
        except Exception as err:
            print("Delete assistant Error: ", err)

**Option 3: get_assistant_info**

This is a combination of get_assistant and get_assistants. It returns a list of dictionaries where each dictionary is for an
entry in the assistants table.

.. code-block:: python

    def get_assistant_info(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT (a.as_id, p.name, p.email, p.photo, a.degree) FROM assistants a JOIN people p ON a.as_person = p.p_id"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                retval = []
                for datum in data:
                    datum = datum[0].lstrip("(").rstrip(")").split(",")
                    val = {
                        "ID": datum[0],
                        "Name": datum[1].strip('"'),
                        "Email": datum[2],
                        "Photo": datum[3],
                        "Degree": datum[4]
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Assistant Info(The one with the string parsing) DB Error: ", err)

Updating 
~~~~~~~~~~~~~~~~~~~~~~~~

To update an assistant, you have to supply assistant id, an attributes list and corresponding values. Then, using
this look-up table, corresponding entry in the database gets updated.

.. code-block:: python
	
    def update_assistant(self, as_id, attrs, values):
        attrs_lookup_table = {
            "person": "AS_PERSON",
            "lab": "LAB",
            "degree": "DEGREE",
            "department": "DEPARTMENT",
            "faculty": "FACULTY",
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE ASSISTANTS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE AS_ID = %s"
                values.append(as_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update assistant Error: ", err)
		
Deleting
~~~~~~~~~~~~~~~~~~~~

To delete an assistant, you have to supply assistant id.

.. code-block:: python

    def delete_assistant(self, as_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM ASSISTANTS WHERE AS_ID = %s"
                values = [as_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete assistant Error: ", err)
	

Buildings
------------------------------

SQL Table Creation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS BUILDINGS (
        BU_ID SERIAL PRIMARY KEY,
        BU_NAME VARCHAR(100),
        BU_CODE VARCHAR(5),
        CAMPUS VARCHAR(20)
    )

Building Class
~~~~~~~~~~~~~~~~~~~~~~~~

Since it makes it easier to create, we have defined a building class for creating an entry into our database.
Therefore, before adding a new building an object of class Building must be initialized. Here is the definition of
the Building class:

.. code-block:: python

    class Building:
        def __init__(self, name, code, campus):
            self.name = name
            self.code = code
            self.campus = campus


Adding 
~~~~~~~~~~~~~~~~~~~~~~~~

Adding a building into the database is pretty straigthforward. You have to pass the object you have initialized
into add_building() function.

.. code-block:: python

   def add_building(self, building):
        """

        :param building: A building object
        :return:
        """
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [building.name, building.code, building.campus]
                statement = "INSERT INTO BUILDINGS (BU_NAME, BU_CODE, CAMPUS) VALUES (%s, %s, %s)"
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add Building Error: ", err)


Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

There are two functions. One returns a specific entry for the given entry and the other one returns entries for all of the
buildings in the database.

**get_building()**

This returns the corresponding query result of the given building id as a list.

.. code-block:: python

    def get_building(self, bu_id):
        """

        :param bu_id: ID of the building in the database
        :return:
        """
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT bu_id, bu_name, bu_code, campus FROM BUILDINGS WHERE BU_ID = %s"
                data = [bu_id]
                cursor.execute(statement, data)
                data = cursor.fetchall()
                cursor.close()
                return data
        except Exception as err:
            print("Get building DB Error: ", err)

        return None

**get_buildings**

This returns multiple queries as a list of dictionaries.

.. code-block:: python

    def get_buildings(self):
        """

        :return: Information as dictionary.
        """
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM buildings"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                retval = []
                for datum in data:
                    val = {
                        "ID": datum[0],
                        "Name": datum[1],
                        "Code": datum[2],
                        "Campus": datum[3]
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Buildings DB Error: ", err)


Updating 
~~~~~~~~~~~~~~~~~~~~~~~~

To update a building, you have to supply building id, an attributes list and corresponding values. Then, using
this look-up table, corresponding entry in the database gets updated.

.. code-block:: python
	
    def update_building(self, bu_id, attrs, values):
        attrs_lookup_table = {
            "name": "BU_NAME",
            "code": "BU_CODE",
            "campus": "CAMPUS"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE BUILDINGS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE BU_ID = %s"
                values.append(bu_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update Building Error: ", err)
		
Deleting
~~~~~~~~~~~~~~~~~~~~

To delete a building, you have to supply building id.

.. code-block:: python

    def delete_building(self, bu_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM BUILDINGS WHERE BU_ID = %s"
                values = [bu_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete building error: ", err)
	
Clubs
------------------------------

SQL Table Creation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS CLUBS (
        CLUB_ID SERIAL PRIMARY KEY,
        NAME VARCHAR(100) NOT NULL,
        FACULTY INTEGER,
        ADVISOR INTEGER,
        CHAIRMAN INTEGER,
        V_CHAIRMAN_1 INTEGER,
        V_CHAIRMAN_2 INTEGER,
        FOREIGN KEY (FACULTY) REFERENCES FACULTIES(FAC_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (ADVISOR) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (CHAIRMAN) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (V_CHAIRMAN_1) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (V_CHAIRMAN_2) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT
    )

Club Class
~~~~~~~~~~~~~~~~~~~~~~~~

Since it makes it easier to create, we have defined a club class for creating an entry into our database.
Therefore, before adding a new class, an object of class Club must be initialized. Here is the definition of
the Club class:

.. code-block:: python

    class Club:
        def __init__(self, name, faculty, advisor, chairman, vice_1, vice_2):
            self.name = name
            self.faculty = faculty
            self.advisor = advisor
            self.chairman = chairman
            self.vice_1 = vice_1
            self.vice_2 = vice_2


Adding 
~~~~~~~~~~~~~~~~~~~~~~~~

Adding a club into the database is pretty straigthforward. You have to pass the object you have initialized
into add_club() function.

.. code-block:: python

   def add_club(self, club):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [club.name, club.faculty, club.advisor, club.chairman, club.vice_1, club.vice_2]
                statement = "INSERT INTO CLUBS (NAME, FACULTY, ADVISOR, CHAIRMAN, V_CHAIRMAN_1, V_CHAIRMAN_2) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add Club Error: ", err)

Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

There are 3 options to read information from clubs page.

**get_club()**

This function takes club id as input and returns the corresponding entry as a list.

.. code-block:: python

    def get_club(self, club_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM CLUBS WHERE CLUB_ID = %s"
                data = [club_id]
                print(data)
                cursor.execute(statement, data)
                datas = cursor.fetchall()
                cursor.close()
                return datas
        except Exception as err:
            print("Get club DB Error: ", err)

        return None

**get_all_clubs()**

This function returns all the entries as a list of lists.

.. code-block:: python

    def get_all_clubs(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM CLUBS"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                return data

        except Exception as err:
            print("Get Clubs Error: ", err)        

        return None

**get_clubs_info_astext()**

This function returns all the clubs as a list of dictionaries. Also, since entries include different numbers that corresponds to a key
in a different table, we are using joins in the query so we can return all the related information in a human readable format.

.. code-block:: python

     def get_clubs_info_astext(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT (c.club_id, c.name, f.fac_name, p1.name, p2.name, p3.name, p4.name) FROM clubs c JOIN faculties f ON c.faculty=f.fac_id JOIN people p1 ON c.advisor=p1.p_id JOIN people p2 ON c.chairman=p2.p_id JOIN people p3 ON c.v_chairman_1=p3.p_id JOIN people p4 ON c.v_chairman_2=p4.p_id"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                retval = []
                for datum in data:
                    datum = datum[0].lstrip("(").rstrip(")").split(",")
                    val = {
                        "ID": datum[0],
                        "Name": datum[1].strip('"'),
                        "Faculty": datum[2].strip('"'),
                        "Advisor": datum[3].strip('"'),
                        "Chair": datum[4].strip('"'),
                        "VChair1": datum[5].strip('"'),
                        "VChair2": datum[6].strip('"')
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Clubs(All Text) DB Error: ", err)

Updating 
~~~~~~~~~~~~~~~~~~~~~~~~

To update a club, you have to supply club id, an attributes list and corresponding values. Then, using
this look-up table, corresponding entry in the database gets updated.

.. code-block:: python
	
    def update_club(self, club_id, attrs, values):
        attrs_lookup_table = {
            "name": "NAME",
            "faculty": "FACULTY",
            "advisor": "ADVISOR",
            "chairman": "CHAIRMAN",
            "vice_1": "V_CHAIRMAN_1",
            "vice_2": "V_CHAIRMAN_2"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE CLUBS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE CLUB_ID = %s"
                values.append(club_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update Club Error: ", err)
		
Deleting
~~~~~~~~~~~~~~~~~~~~

To delete a club, you have to supply club id.

.. code-block:: python

    def delete_club(self, club_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM CLUBS WHERE CLUB_ID = %s"
                values = [club_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete club error: ", err)

Departments
------------------------------

SQL Table Creation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS DEPARTMENTS (
        DEP_ID SERIAL PRIMARY KEY,
        DEP_NAME VARCHAR(100),
        FACULTY INTEGER,
        BUILDING INTEGER,
        DEAN INTEGER,
        FOREIGN KEY (BUILDING) REFERENCES BUILDINGS(BU_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (FACULTY) REFERENCES FACULTIES(FAC_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (DEAN) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT
    )

Department Class
~~~~~~~~~~~~~~~~~~~~~~~~

Since it makes it easier to create, we have defined a department class for creating an entry into our database.
Therefore, before adding a new department, an object of class Department must be initialized. Here is the definition of
the Department class:

.. code-block:: python

    class Department:
        def __init__(self, name, faculty, building, dean):
            self.name = name
            self.faculty = faculty
            self.building = building
            self.dean = dean

Adding 
~~~~~~~~~~~~~~~~~~~~~~~~

Adding a department into the database is pretty straigthforward. You have to pass the object you have initialized
into add_department() function.

.. code-block:: python

    def add_department(self, department):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [department.name, department.faculty, department.building, department.dean]
                statement = "INSERT INTO DEPARTMENTS (DEP_NAME, FACULTY, BUILDING, DEAN) VALUES (%s, %s, %s, %s)"
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print(" Add department Error: ", err)


Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

There are 3 functions to read an entry or multiple entries from the database.

**get_department()**

This function takes department id as an argument and returns the corresponding entry as a list.

.. code-block:: python

    def get_department(self, dep_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM DEPARTMENTS WHERE DEP_ID = %s"
                data = [dep_id]
                cursor.execute(statement, data)
                datas = cursor.fetchall()
                cursor.close()
                return datas
        except Exception as err:
            print("Get department DB Error: ", err)

        return None

**get_all_departments()**

This function returns all the entries of departments table as a list of lists.

.. code-block:: python

    def get_all_departments(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM DEPARTMENTS"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                return data
        except Exception as err:
            print("Fetching Departments Error: ", err)

        return None

**get_departments_text**

This function returns all the entries of departments as a list of dictionaries. To get a human readable result, multiple
joins are used.

.. code-block:: python

    def get_departments_text(self):
        """

        :return: Information as dictionary.
        """
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM departments INNER JOIN faculties ON departments.faculty = faculties.fac_id INNER JOIN buildings ON departments.building = buildings.bu_id INNER JOIN people ON departments.dean = people.p_id"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                retval = []
                for datum in data:
                    val = {
                        "ID": datum[0],
                        "Name": datum[1],
                        "Faculty": datum[6],
                        "Building": datum[12],
                        "Chair": datum[16]
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Departments(All Text) DB Error: ", err)

Updating 
~~~~~~~~~~~~~~~~~~~~~~~~

To update a deparment, you have to supply department id, an attributes list and corresponding values. Then, using
this look-up table, corresponding entry in the database gets updated.

.. code-block:: python
	
    def update_department(self, dep_id, attrs, values):
        attrs_lookup_table = {
            "name": "dep_name",
            "faculty": "faculty",
            "building": "building",
            "dean": "dean"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE DEPARTMENTS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE DEP_ID = %s"
                values.append(dep_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update Department Error: ", err)
		
Deleting
~~~~~~~~~~~~~~~~~~~~

To delete a department, you have to supply department id.

.. code-block:: python

    def delete_department(self, dep_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM DEPARTMENTS WHERE DEP_ID = %s"
                values = [dep_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Department Error: ", err)

Faculties
------------------------------

SQL Table Creation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS FACULTIES (
        FAC_ID SERIAL PRIMARY KEY,
        FAC_NAME VARCHAR(100) NOT NULL,
        FAC_BUILDING INTEGER,
        DEAN INTEGER NOT NULL,
        DEAN_ASST_1 INTEGER NOT NULL,
        DEAN_ASST_2 INTEGER,
        FOREIGN KEY (FAC_BUILDING) REFERENCES BUILDINGS(BU_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (DEAN) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (DEAN_ASST_1) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (DEAN_ASST_2) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT
    )

Faculty Class
~~~~~~~~~~~~~~~~~~~~~~~~

Since it makes it easier to create, we have defined a faculty class for creating an entry into our database.
Therefore, before adding a new faculty, an object of class Faculty must be initialized. Here is the definition of
the Faculty class:

.. code-block:: python

    class Faculty:

        def __init__(self, name, building, dean, assistant_dean_1, assistant_dean_2):
            self.name = name
            self.building = building
            self.dean = dean
            self.assistant_dean_1 = assistant_dean_1
            self.assistant_dean_2 = assistant_dean_2


Adding 
~~~~~~~~~~~~~~~~~~~~~~~~

Adding a faculty into the database is pretty straigthforward. You have to pass the object you have initialized
into add_faculty() function.

.. code-block:: python

    def add_faculty(self, faculty):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [faculty.name, faculty.building, faculty.dean, faculty.assistant_dean_1]
                if faculty.assistant_dean_2 is not None:
                    data.append(faculty.assistant_dean_2)
                    statement = "INSERT INTO FACULTIES (FAC_NAME, FAC_BUILDING, DEAN, DEAN_ASST_1, DEAN_ASST_2) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(statement, data)
                else:
                    statement = "INSERT INTO FACULTIES (FAC_NAME, FAC_BUILDING, DEAN, DEAN_ASST_1) VALUES (%s, %s, %s, %s)"
                    cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add faculty Error: ", err)

Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

There are 4 different functions for reading an entry or multiple entries from the database.


**get_faculty**

This function takes faculty id as an argument and returns the corresponding entry as a list.

.. code-block:: python

     def get_faculty(self, fac_id):
        """
        Gets faculty id as an input, returns query results.
        By: Uğur Ali Kaplan"""
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM FACULTIES WHERE FAC_ID = %s"
                data = [fac_id]
                print(data)
                cursor.execute(statement, data)
                datas = cursor.fetchall()
                cursor.close()
                return datas
        except Exception as err:
            print("Get Faculty DB Error: ", err)

        return None

**get_faculties**

This function returns ids, names, buildings the faculties belong to and codes of those buildings
as a list of dictionaries. Joins are used to ensure a human readable form in the return values.

.. code-block:: python

    def get_faculties(self):
        """
        Joins faculty and buildings table, returns relevant columns as a dictionary.
        :return: 
        
        By: Uğur Ali Kaplan
        """
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM faculties INNER JOIN buildings ON faculties.fac_id = bu_id"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                retval = []
                for datum in data:
                    val = {
                        "ID": datum[0],
                        "Name": datum[1],
                        "Building Name": datum[4],
                        "Building Code": datum[5]
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Faculties DB Error: ", err)

**get_all_faculties**

This function returns all the rows of the faculty table as a list of lists.

.. code-block:: python

        def get_all_faculties(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM FACULTIES"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                return data

        except Exception as err:
            print("Fetch Faculties Error: ", err)

        return None

**get_faculty_as_text**

This function returns the information of all the faculties in a human readable form with a list of dictionaries. Each element
of the returned list is a dictionary corresponding to one row of the faculties table.

.. code-block:: python

        def get_faculty_as_text(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT (f.fac_id, f.fac_name, b.bu_name, p1.name, p2.name, p3.name) FROM faculties f JOIN buildings b ON f.fac_building = b.bu_id JOIN people p1 ON f.dean = p1.p_id JOIN people p2 ON f.dean_asst_1 = p2.p_id LEFT JOIN people p3 ON f.dean_asst_2 = p3.p_id"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                retval = []
                for datum in data:
                    datum = datum[0].lstrip("(").rstrip(")").split(",")
                    val = {
                        "ID": datum[0],
                        "Name": datum[1].strip('"'),
                        "Building": datum[2].strip('"'),
                        "Dean": datum[3].strip('"'),
                        "VDean1": datum[4].strip('"'),
                        "VDean2": datum[5].strip('"')
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Faculty Info(The one with the string parsing) DB Error: ", err)

Updating 
~~~~~~~~~~~~~~~~~~~~~~~~

To update a faculty, you have to supply faculty id, an attributes list and corresponding values. Then, using
this look-up table, corresponding entry in the database gets updated.

.. code-block:: python
	
    def update_faculty(self, fac_id, attrs, values):
        attrs_lookup_table = {
            "name": "FAC_NAME",
            "building": "FAC_BUILDING",
            "dean": "DEAN",
            "vdean_1": "DEAN_ASST_1",
            "vdean_2": "DEAN_ASST_2",
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE FACULTIES SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE FAC_ID = %s"
                values.append(fac_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update Faculty Error: ", err)
		
Deleting
~~~~~~~~~~~~~~~~~~~~

To delete a faculty, you have to supply faculty id.

.. code-block:: python

    def delete_faculty(self, fac_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM FACULTIES WHERE FAC_ID = %s"
                values = [fac_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Faculty Error: ", err)

Labs
------------------------------

SQL Table Creation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS LABS (
        LAB_ID SERIAL PRIMARY KEY,
        LAB_NAME VARCHAR(100) UNIQUE,
        DEPARTMENT INTEGER,
        FACULTY INTEGER,
        BUILDING  INTEGER,
        ROOM INTEGER,
        INVESTIGATOR INTEGER NOT NULL,
        FOREIGN KEY (BUILDING) REFERENCES BUILDINGS(BU_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (FACULTY) REFERENCES FACULTIES(FAC_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (DEPARTMENT) REFERENCES DEPARTMENTS(DEP_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (ROOM) REFERENCES ROOMS(ROOM_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (INVESTIGATOR) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT
    )

Lab Class
~~~~~~~~~~~~~~~~~~~~~~~~

Since it makes it easier to create, we have defined a lab class for creating an entry into our database.
Therefore, before adding a new lab, an object of class Lab must be initialized. Here is the definition of
the Lab class:

.. code-block:: python

    class Lab:
        def __init__(self, name, department, faculty, room, investigator, building):
            self.name = name
            self.department = department
            self.faculty = faculty
            self.room = room
            self.investigator = investigator
            self.building = building



Adding 
~~~~~~~~~~~~~~~~~~~~~~~~

Adding a lab into the database is pretty straigthforward. You have to pass the object you have initialized
into add_lab() function.

.. code-block:: python

     def add_lab(self, lab):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [lab.name, lab.department, lab.faculty, lab.building, lab.room, lab.investigator]
                statement = "INSERT INTO LABS (LAB_NAME, DEPARTMENT, FACULTY, BUILDING, ROOM, INVESTIGATOR) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add lab Error: ", err)


Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

There are 3 different functions that reads from the labs table.

**get_lab**

This function returns the row corresponding to given lab id as a list.

.. code-block:: python

    def get_lab(self, lab_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM LABS WHERE LAB_ID = %s"
                data = [lab_id]
                cursor.execute(statement, data)
                datas = cursor.fetchall()
                cursor.close()
                return datas
        except Exception as err:
            print("Get Lab DB Error: ", err)

        return None


**get_all_labs**

This function returns all the labs as a list of lists.

.. code-block:: python

    def get_all_labs(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM LABS"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                return data
        except Exception as err:
            print("Delete lab Error: ", err)

        return None


**get_lab_info**

This function returns all the rows of labs table as a list of dictionaries. To achieve a human readable form in the returned dictionaries,
multiple joins are used in the select statement.

.. code-block:: python

    def get_lab_info(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT (l.lab_id, l.lab_name, d.dep_name, f.fac_name, b.bu_name, r.room_name, p.name) FROM labs l JOIN departments d ON l.department=d.dep_id JOIN faculties f ON l.faculty = f.fac_id JOIN buildings b ON l.building=b.bu_id JOIN rooms r ON l.room = r.room_id JOIN people p ON l.investigator=p.p_id"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                retval = []
                for datum in data:
                    datum = datum[0].lstrip("(").rstrip(")").split(",")
                    val = {
                        "ID": datum[0],
                        "Name": datum[1].strip('"'),
                        "Department": datum[2].strip('"'),
                        "Faculty": datum[3].strip('"'),
                        "Building": datum[4].strip('"'),
                        "Room": datum[5].strip('"'),
                        "Investigator": datum[6].strip('"')
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Lab Info(The one with the string parsing) DB Error: ", err)



Updating 
~~~~~~~~~~~~~~~~~~~~~~~~

To update a lab, you have to supply lab id, an attributes list and corresponding values. Then, using
this look-up table, corresponding entry in the database gets updated.

.. code-block:: python
	
    def update_lab(self, lab_id, attrs, values):
        attrs_lookup_table = {
            "name": "LAB_NAME",
            "department": "DEPARTMENT",
            "faculty": "FACULTY",
            "building": "BUILDING",
            "room": "ROOM",
            "investigator": "INVESTIGATOR"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE LABS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE LAB_ID = %s"
                values.append(lab_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update lab Error: ", err)
		
Deleting
~~~~~~~~~~~~~~~~~~~~

To delete a lab, you have to supply lab id.

.. code-block:: python

    def delete_lab(self, lab_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM LABS WHERE LAB_ID = %s"
                values = [lab_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete lab Error: ", err)

****************
Papers
****************

SQL Table Creation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS PAPERS (
        PAPER_ID SERIAL PRIMARY KEY,
        TITLE VARCHAR (100),
        PLAT VARCHAR(100),
        CITATION_COUNT INTEGER DEFAULT 0,
        AUTHOR INTEGER,
        CONFERENCE BOOLEAN NOT NULL,
        FOREIGN KEY (AUTHOR) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT
    )

Paper Class
~~~~~~~~~~~~~~~~~~~~~~~~

Since it makes it easier to create, we have defined a paper class for creating an entry into our database.
Therefore, before adding a new paper an object of class Paper must be initialized. Here is the definition of
the Paper class:

.. code-block:: python

    class Paper:
        def __init__(self, title, platform, citation, author, isConference):
            self.title = title
            self.platform = platform
            self.citation = citation
            self.author = author
            self.isConference = isConference



Adding 
~~~~~~~~~~~~~~~~~~~~~~~~

Adding a paper into the database is pretty straigthforward. You have to pass the object you have initialized
into add_paper() function.

.. code-block:: python

    def add_paper(self, paper):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [paper.title, paper.platform, paper.citation, paper.author, paper.isConference]
                statement = "INSERT INTO PAPERS (TITLE, PLAT, CITATION_COUNT, AUTHOR, CONFERENCE) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add Paper Error: ", err)


Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

There are different methods for reading entries from the database.

**get_authors**

This function returns all the people in the database that has a written paper in the database as a list
of dictionaries.

.. code-block:: python

    def get_authors(self):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = "SELECT DISTINCT author, name from papers join people on author=p_id;"
            cursor.execute(statement)
            data = cursor.fetchall()
            cursor.close()
            retval = []
            for datum in data:
                val = {
                    "ID": datum[0],
                    "Name": datum[1]
                }
                retval.append(val)
            return retval

**get_paper**

This function returns the relevant entry from the papers table according to given paper id as a list.

.. code-block:: python

    def get_paper(self, paper_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM PAPERS WHERE PAPER_ID = %s"
                data = [paper_id]
                cursor.execute(statement, data)
                data = cursor.fetchall()
                cursor.close()
                return data
        except Exception as err:
            print("Get paper DB Error: ", err)

        return None

**get_paper_by_author**

This function returns all the papers written by a given author as a list of dictionaries. You have to supply person id
to this function. First, it fetches all the papers written by this author. Then, it gets the papers with the same title from the
database and determines if there are other authors and adds them to the authors list. Since we use inner join for this, if there
is a single author, author list stays empty. Therefore, we check the length of the authors list and add the name of the given person.

.. code-block:: python

    def get_paper_by_author(self, person):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT (paper_id, title, plat, citation_count, conference) FROM papers WHERE papers.author = %s"
                data = [person]
                cursor.execute(statement, data)
                data = cursor.fetchall()
                cursor.close()
                retval = []
                for datum in data:
                    datum = datum[0].lstrip("(").rstrip(")").split(",")
                    val = {
                        "ID": datum[0],
                        "Title": datum[1].strip('"'),
                        "Platform": datum[2].strip('"'),
                        "Citation": datum[3],
                        "Conference": datum[4],
                        "Authors": []
                    }

                    if val["Conference"] == "t":
                        val["Conference"] = True
                    else:
                        val["Conference"] = False

                    retval.append(val)

                for val in retval:
                    cursor = connection.cursor()
                    statement = "SELECT name FROM papers p1 JOIN papers p2 ON p1.title = p2.title JOIN people p3 ON p3.p_id = p1.author WHERE p1.author <> p2.author AND p1.title = %s"
                    data = [val["Title"]]
                    cursor.execute(statement, data)
                    data = cursor.fetchall()
                    for datum in data:
                        val["Authors"].append(datum[0])
                    val["Authors"] = list(set(val["Authors"]))
                    if len(val["Authors"]) == 0:
                        statement = "SELECT name FROM papers p1 JOIN people p2 ON p1.author=p2.p_id WHERE title = %s"
                        data = [val["Title"]]
                        cursor.execute(statement, data)
                        data = cursor.fetchall()
                        val["Authors"].append(data[0][0])
                    cursor.close()

                return retval
        except Exception as err:
            print("Get Paper by Author DB Error: ", err)


Updating 
~~~~~~~~~~~~~~~~~~~~~~~~

To update a paper, you have to supply paper id, an attributes list and corresponding values. Then, using
this look-up table, corresponding entry in the database gets updated.

.. code-block:: python
	
    def update_paper(self, paper_id, attrs, values):
        attrs_lookup_table = {
            "title": "TITLE",
            "platform": "PLAT",
            "citation": "CITATION_COUNT",
            "author": "AUTHOR",
            "isConference": "CONFERENCE"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE PAPERS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE PAPER_ID = %s"
                values.append(paper_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update Paper Error: ", err)
		
Deleting
~~~~~~~~~~~~~~~~~~~~

To delete a paper, you have to supply paper id.

.. code-block:: python

    def delete_paper(self, paper_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM PAPERS WHERE PAPER_ID = %s"
                values = [paper_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete paper error: ", err)
