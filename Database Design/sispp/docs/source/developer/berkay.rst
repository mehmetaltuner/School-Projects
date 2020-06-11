Parts Implemented by Berkay Olgun
=================================

*****************
Instructors
*****************

.. note:: All table creations exist in db_init.py file.
.. note:: All SQL operations in python files are wrapped with try-except statements in order to avoid errors

1. Creation
~~~~~~~~~~~~~~~~~~~~~~~~

Detailed informations about instructors are kept in tables that it refers.

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS INSTRUCTORS(
        INS_ID INTEGER PRIMARY KEY,
        BACHELORS VARCHAR(90),
        MASTERS VARCHAR(90),
        DOCTORATES VARCHAR(90),
        DEPARTMENT INTEGER,
        ROOM INTEGER UNIQUE,
        LAB INTEGER,
        FOREIGN KEY (DEPARTMENT) REFERENCES DEPARTMENTS(DEP_ID) ON UPDATE CASCADE ON DELETE SET NULL,
        FOREIGN KEY (ROOM) REFERENCES ROOMS(ROOM_ID) ON DELETE SET NULL,
        FOREIGN KEY (LAB) REFERENCES LABS(LAB_ID) ON DELETE SET NULL,
        FOREIGN KEY (INS_ID) REFERENCES PEOPLE ON DELETE CASCADE
    )

2. Adding 
~~~~~~~~~~~~~~~~~~~~~~~~

Before adding an instructor if that person is not in table People he/she will be added to people before adding as instructor.
Instructor id references the private key in the People table.

.. warning:: The room of an instructor should be added before it's instructor.

.. code-block:: python

    def add_instructor(self, instructor):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO INSTRUCTORS (INS_ID, BACHELORS, MASTERS, DOCTORATES,
                 DEPARTMENT, ROOM, LAB) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                data = [instructor.instructor_id, instructor.bachelors, instructor.masters, instructor.doctorates,
                        instructor.department, instructor.room, instructor.lab]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add Instructor Error: ", err)
        return instructor



3. Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

In order to get room name lab name and instructor name join operations must be performed since the tables are in normal form.

.. code-block:: python

    def get_instructors(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT P_ID, NAME, ROOMS.ROOM_NAME, LABS.LAB_NAME, BACHELORS, MASTERS,
                 DOCTORATES FROM INSTRUCTORS JOIN PEOPLE ON (INSTRUCTORS.INS_ID = PEOPLE.P_ID)
                  JOIN ROOMS ON (INSTRUCTORS.ROOM = ROOMS.ROOM_ID)
                   LEFT JOIN LABS ON (INSTRUCTORS.LAB = LABS.LAB_ID)"
                cursor.execute(statement)
                datas = cursor.fetchall()
                cursor.close()
                retval = []
                for data in datas:
                    val = {
                        "ID":data[0],
                        "Name": data[1],
                        "Room": data[2],
                        "Lab": data[3],
                        "Bachelors": data[4],
                        "Masters": data[5],
                        "Doctorates": data[6]
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Instructors Error: ", err)

        return None



4. Updating 
~~~~~~~~~~~~~~~~~~~~~~~~

In order to update instructors, characteristic attribute id is enough to filter any of them.
attrs_lookup_table is used with attrs and values list in order to restrict naming and ordering attribute confusions.

.. code-block:: python
	
	def update_instructor(self, ins_id, attrs, values):
        attrs_lookup_table = {
            "department": "DEPARTMENT",
            "room": "ROOM",
            "lab": "LAB",
            "bachelors": "BACHELORS",
            "masters": "MASTERS",
            "doctorates": "DOCTORATES"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE INSTRUCTORS SET "
                for i in range(len(attrs) - 1):
                    print(attrs_lookup_table[attrs[i]] + " = %s ,")
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE INS_ID = %s"
                values.append(ins_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update Instructors Error: ", err)
		
5. Deleting
~~~~~~~~~~~~~~~~~~~~

In order to delete an instructor, simple DELETE query is sufficient.

.. code-block:: python

	def delete_instructor(self, ins_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM INSTRUCTORS WHERE INS_ID = %s"
                values = [ins_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Instructor Error: ", err)
	

*****************
Rooms
*****************

1. Creation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS ROOMS (
        ROOM_ID SERIAL PRIMARY KEY,
        BUILDING INTEGER,
        ROOM_NAME VARCHAR(10) UNIQUE NOT NULL,
        AVAILABLE BOOL DEFAULT TRUE,
        CLASS BOOLEAN DEFAULT FALSE,
        LAB BOOLEAN DEFAULT FALSE,
        ROOM BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (BUILDING) REFERENCES BUILDINGS(BU_ID) ON UPDATE CASCADE ON DELETE CASCADE
    )
		
Building key references the building that room is in.

2. Adding 
~~~~~~~~~~~~~~~~~~~~~~~~

.. warning:: Before adding a room a building must exist to refer with a foreign key.

.. code-block:: python

	def add_room(self, room):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO ROOMS (BUILDING, ROOM_NAME, AVAILABLE, CLASS, LAB, ROOM) VALUES (%s, %s, %s, %s, %s, %s)"
                data = [room.building, room.name, room.availability, room.classroom, room.lab, room.room]
                cursor.execute(statement, data)
                statement = "SELECT ROOM_ID FROM ROOMS WHERE ROOM_NAME = %s"
                data = [room.name]
                cursor.execute(statement, data)
                value = cursor.fetchall()
                room.id = value[0]
                cursor.close()
        except Exception as err:
            print("Add Room Error: ", err)
        return room

After adding a room its id is taken to include it in return.

3. Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

In order to get the name of the room's building a join operation must be performed.

.. code-block:: python

    def get_rooms(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT ROOM_ID, BU_NAME, ROOM_NAME FROM ROOMS JOIN BUILDINGS ON(ROOMS.BUILDING = BUILDINGS.BU_ID)"
                cursor.execute(statement)
                datas = cursor.fetchall()
                cursor.close()
                retval = []
                for data in datas:
                    val = {
                        "ID": data[0],
                        "Name": data[2],
                        "Building": data[1]  
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Rooms Error: ", err)

Rooms are returned with a list of dictionaries
	
			
4. Updating 
~~~~~~~~~~~~~~~~~~~~~~~~

Attributes are taken from the lookup table values and names are compared with given parameters and new values are written on the instance.

.. code-block:: python
	
	def update_room(self, room_id, attrs, values):
        attrs_lookup_table = {
            "building": "BUILDING",
            "room_name": "ROOM_NAME",
            "class": "CLASS",
            "lab": "LAB",
            "room": "ROOM",
            "available": "AVAILABLE"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE ROOMS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE ROOM_ID = %s"
                values.append(room_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update Rooms Error: ", err)
		
		
5. Deleting
~~~~~~~~~~~~~~~~~~~~~~~~

Simple DELETE query with a room id is sufficient to delete any room from the application.

.. code-block:: python

	def delete_room(self, room_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM ROOMS WHERE room_id = %s"
                values = [room_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Room Error: ", err)
	
****************
Classrooms
****************

1. Creation
~~~~~~~~~~~~~~~~~~~~

Private and foreign key class id refers to the room id that the class in.
.. note:: In our structure every classroom is a (inside a) room.

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS CLASSES(
        CL_ID INTEGER PRIMARY KEY,
        CAP INTEGER NOT NULL,
        TYPE VARCHAR(15) DEFAULT 'Lecture',
        AIR_CONDITIONER BOOL,
        LAST_RESTORATION VARCHAR(4),
        BOARD_TYPE VARCHAR(5) DEFAULT 'Mixed',
        FOREIGN KEY (CL_ID) REFERENCES ROOMS(ROOM_ID) ON DELETE CASCADE
    )

2. Adding
~~~~~~~~~~~~~~~~~~~~
Before adding a classroom a room is added if not exists, with the proper values.

.. code-block:: python

    def add_classroom(self, classroom):
            try:
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    statement = "INSERT INTO CLASSES (CL_ID, TYPE, AIR_CONDITIONER, LAST_RESTORATION, BOARD_TYPE, CAP) VALUES (%s, %s, %s, %s, %s, %s)"
                    data = [classroom.id, classroom.type, classroom.conditioner, classroom.restoration_date, classroom.board_type, classroom.cap]
                    cursor.execute(statement, data)
                    cursor.close()
            except Exception as err:
                print("Add Classroom Error: ", err)
            return classroom

3. Reading
~~~~~~~~~~~~~~~~~~~~

Selecting all the values by the name in order to avoid ordering problems when giving them to attributes dictioanary.

.. code-block:: python

    def get_classrooms(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT CLASSES.CL_ID, ROOMS.ROOM_NAME, CLASSES.CAP, CLASSES.TYPE, BUILDINGS.BU_NAME FROM CLASSES JOIN ROOMS ON CL_ID = ROOM_ID JOIN BUILDINGS ON BUILDINGS.BU_ID = ROOMS.BUILDING"
                cursor.execute(statement)
                datas = cursor.fetchall()
                cursor.close()
                retval = []
                for data in datas:
                    val = {
                        "ID":data[0],
                        "Name": data[1],
                        "Capacity": data[2],
                        "Class Type": data[3],
                        "Building Name": data[4],
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Classrooms Error: ", err)

        return None
	
4. Updating
~~~~~~~~~~~~~~~~~~~~

Same update process is applied to classrooms. Attribute names and their values are given parameters from the form.

.. code-block:: python

	def update_classroom(self, class_id, attrs, values):
        attrs_lookup_table = {
            "type": "TYPE",
            "air_conditioner": "AIR_CONDITIONER",
            "last_restoration": "LAST_RESTORATION",
            "board_type": "BOARD_TYPE",
            "cap": "CAP"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE CLASSES SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE CL_ID = %s"
                print(statement, values)
                values.append(class_id)
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Update Classroom Error: ", err)

5. Deleting
~~~~~~~~~~~~~~~~~~~~

.. note:: By the cascade nature if referred room is deleted the classroom is deleted. 

.. code-block:: python

	def delete_classroom(self, cl_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM CLASSES WHERE CL_ID = %s"
                values = [cl_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Classroom Error: ", err)