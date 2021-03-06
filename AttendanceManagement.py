from enum import Enum

database = {}
attendance = {}
staff_members = []

next_student_id = 0
next_user_id = 0


def print_staff_members():
    for member in staff_members:
        member.print()


def get_staff_member(id: int):
    for member in staff_members:
        if member.id == id:
            return member


def printGrades():
    print("Grades: ")
    for grade in database.keys():
        print(grade, " \t", end=" ")
    print()


def printSections(grade: int):
    print("The sections in grade %d are:" % grade)
    for g in database.keys():
        if g == grade:
            for section in database[g].keys():
                print(section, end=", ")
    print()


def getNextStudentID():
    global next_student_id
    next_student_id += 1
    return next_student_id


def getNextUserID():
    global next_user_id
    next_user_id += 1
    return next_user_id


def printDatabase():
    for grade in database.keys():
        print("----------------------GRADE:", grade, "----------------------")
        for section in database[grade]:
            print(section + ": ", end=" ")
            for students in database[grade][section]:
                print(students, end=" ")
            print("\n", end="")
        print()


class UserType(Enum):
    ADMIN = 1
    STAFF = 2


class TimeSpan(Enum):
    WEEK = 5
    MONTH = 4 * 5
    YEAR = 52 * 5


class User:
    def __init__(self, name: str, type: UserType):
        self.id = getNextUserID()
        self.name = name
        self.type = type
        staff_members.append(self)
        print("New staff member added successfully")
        self.print()
        print()

    def print(self):
        print("Name: %s \tID: %d \tType: %s" % (self.name, self.id, self.type.name))


class Staff(User):
    __allocated_section = [0, ""]

    def __init__(self, name: str, type: UserType):
        super().__init__(name, type)

    def get_allocation(self):
        return self.__allocated_section

    def set_allocation(self, grade: int, section_name: str):
        self.__allocated_section[0] = grade
        self.__allocated_section[1] = section_name

    def set_missing_students(self, missing_students: []):
        for missing_student in missing_students:
            if missing_student not in database[self.__allocated_section[0]][self.__allocated_section[1]]:
                print("ID %d is not allocated to your section" % missing_student)
                print("Your section student IDs are: ")
                for student_ID in database[self.__allocated_section[0]][self.__allocated_section[1]]:
                    print(student_ID, end=", ")
                print()
                return
        else:
            attendance[self.__allocated_section[0]][self.__allocated_section[1]].insert(0, missing_students)

    def showAttendance(self, student_id: int, time_span: TimeSpan):
        missing_attendance = 0
        _time_span = 1
        if student_id not in database[self.__allocated_section[0]][self.__allocated_section[1]]:
            print("ID %d is not allocated to your section" % student_id)
            print("Your section student IDs are: ")
            for student_ID in database[self.__allocated_section[0]][self.__allocated_section[1]]:
                print(student_ID, end=", ")
            print()
            return

        for day in attendance[self.__allocated_section[0]][self.__allocated_section[1]]:
            for missing in day:
                if missing == student_id:
                    missing_attendance += 1
                    break
            if _time_span == time_span.value:
                print("Student with ID: ", student_id, " was missing ", missing_attendance, " times this ",
                      time_span.name.lower())
                return
            _time_span += 1
        else:
            print("Student with ID: ", student_id, " was missing ", missing_attendance, " times this ",
                  time_span.name.lower())


class Admin(User):
    def __int__(self, name: str, type: UserType):
        super().__init__(name, type)

    def add_grade(self, grade: int):
        database[grade] = {}
        attendance[grade] = {}

    def add_section(self, grade, sectionName):
        database[grade][sectionName] = []
        attendance[grade][sectionName] = []

    def add_student(self, grade: int, sectionName: str):
        if len(database[grade][sectionName]) >= 20:
            print("This section is full\nChose other or create new section")
        else:
            database[grade][sectionName].append(getNextStudentID())

    def add_staff_member(self, name: str, user_type: UserType):
        if user_type == UserType.ADMIN:
            return Admin(name, user_type)
        else:
            return Staff(name, user_type)

    def allocate_staff(self, staff: Staff, grade: int, section_name: str):
        if staff.type == UserType.STAFF:
            staff.set_allocation(grade, section_name)
        else:
            print("Only general staff members can be allocated")

admin_1 = Admin("Admin1", UserType.ADMIN)
staff_1 = admin_1.add_staff_member("User1", UserType.STAFF)

admin_1.allocate_staff(staff_1, 1, "a")


# print_staff_members()


def populateDatabase(admin: Admin):
    sections = 97  # a
    group = 1
    # id = 1
    students_per_section = [80, 90, 36, 39]
    for grade in range(1, 5):
        admin.add_grade(grade)
        admin.add_section(grade, chr(sections))
        for students in range(students_per_section[grade - 1]):
            if group > 20:
                sections += 1
                admin.add_section(grade, chr(sections))
                group = 1

            admin.add_student(grade, chr(sections))
            group += 1
        sections = 97
        group = 1


def populateAttendance():
    for days in range(TimeSpan.MONTH.value):
        missing_students = [13, 15, 18]
        staff_1.set_missing_students(missing_students)
        missing_students = [13, 15]
        staff_1.set_missing_students(missing_students)
        missing_students = [13]
        staff_1.set_missing_students(missing_students)
        missing_students = []
        staff_1.set_missing_students(missing_students)


populateDatabase(admin_1)
# printDatabase()
populateAttendance()


# print(attendance)
# staff_1.showAttendance(13, TimeSpan.MONTH)


def menu():
    choice = 0
    while choice != 9:
        choice = int(input("1) Admin 2) Staff 9) exit "))
        if choice == 1:
            admin_menu()
        if choice == 2:
            staff_menu()


def admin_menu():
    choice = 0
    while choice != 9:
        print("")
        print("1) To add grade\n2) To print grades\n3) To add section\n"
              "4) To print sections\n5) To print the database \n6) To add students \n7) To allocate staff \n8) To add "
              "new user \n9) To exit ")
        choice = int(input("What admin command would you like to perform? "))
        if choice == 9:
            return
        elif choice == 1:
            printGrades()
            grade_to_add = int(input("What grade would you like to add? "))
            admin_1.add_grade(grade_to_add)
        elif choice == 2:
            printGrades()
        elif choice == 3:
            printGrades()
            grade_to_add_to = int(input("Which grade would you like to add the section to? "))
            printSections(grade_to_add_to)
            section_to_add = input("What is the name of the section you would like to add? ")
            try:
                admin_1.add_section(grade_to_add_to, section_to_add)
            except KeyError as k:
                print("This grade does not exist, please try again")
        elif choice == 4:
            section_to_add = int(input("Which grade's sections: "))
            printSections(section_to_add)
        elif choice == 5:
            printDatabase()
        elif choice == 6:
            printGrades()
            grade_to_add_to = int(input("Which grade would you like to add the student to? "))
            printSections(grade_to_add_to)
            section_to_add_to = input("Which section would you like to add the student to?")
            try:
                admin_1.add_student(grade_to_add_to, section_to_add_to)
            except KeyError:
                print("There was an error in the grade or section, please try again")
        elif choice == 7:
            print("Staff member id's:")
            print_staff_members()
            staff_to_add = int((input("What is the staff id of the staff member would you like to allocate? ")))
            staff_to_add = get_staff_member(staff_to_add)
            if isinstance(staff_to_add,int):
                print("Staff ID not found")
                return

            printGrades()
            grade_to_add_to = int(input("What is the grade you would like to allocate them to? "))
            printSections(grade_to_add_to)
            section_to_add_to = input("Which section would you like to allocate them to? ")
            try:
                admin_1.allocate_staff(staff_to_add, grade_to_add_to, section_to_add_to)
            except Exception as e:
                print("There has been an error, please try again" + e)
        elif choice == 8:
            print_staff_members()
            user_type = input("Type 1 for adding admin user\nType 2 for adding general staff member\n")
            username = input("Type the new user name:")
            if user_type == 1:
                user_type = UserType.ADMIN
            else:
                user_type = UserType.STAFF
            try:
                admin_1.add_staff_member(username, user_type)
            except Exception as e:
                print("This attempt was not successful")


def staff_menu():
    successful_login = False
    while successful_login == False:
        try:
            print("Please enter your staff ID: ")
            staff_id = int(input("Type -1 to exit: "))
            if staff_id == -1:
                break
            staff_using = get_staff_member(staff_id)
        except Exception as e:
            print("There has been an error in your staff ID, please try again.")
        else:
            successful_login = True
    choice = 0
    while choice != 9:
        print("1) To mark students as absent 2) To show attendance 9) To exit")
        choice = int(input("What staff command would you like to do? "))

        if choice == 1:
            successful_absent_mark = False
            while successful_absent_mark == False:
                absent_students = []
                print("Please type the IDs of the absent students. Type -1 when done")
                absent_student_id = -200
                absent_student_id = int(input("ID:"))
                while absent_student_id != -1:
                    # if absent_student_id == -2:
                    #     break
                    absent_students.append(absent_student_id)
                    absent_student_id = int(input("ID:"))
                try:
                    staff_using.set_missing_students(absent_students)
                except Exception as e:
                    print("There has been an error, please try again. " + e)
                else:
                    print("Students successfully marked absent.")
                    successful_absent_mark = True
        elif choice == 2:
            print("Please enter the student ID of the student whose attendance you would like to see: ")
            student_id = int(input("Type -1 to exit: "))
            if student_id == -1:
                break
            time_period = int(input("What is the time period you would like to see?\n1) week\n2)month\n3)year"))
            if time_period == 1:
                time_period = TimeSpan.WEEK
            elif time_period == 2:
                time_period = TimeSpan.MONTH
            else:
                time_period = TimeSpan.YEAR
            try:
                staff_using.showAttendance(student_id, time_period)
            except Exception as e:
                print("There has been an error. Please try again. " + e)


menu()
