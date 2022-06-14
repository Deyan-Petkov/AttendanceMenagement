from enum import Enum

database = {}
attendance = {}
staff_members = []


def print_staff_members():
    for member in staff_members:
        member.print()


def get_staff_member(id: int):
    for member in staff_members:
        if member.id == id:
            return member


class UserType(Enum):
    ADMIN = 1
    STAFF = 2


class TimeSpan(Enum):
    WEEK = 7
    MONTH = 30
    YEAR = 365


class User:
    def __init__(self, id: int, name: str, type: UserType):
        self.id = id
        self.name = name
        self.type = type

    def print(self):
        print("Name: %s \tID: %d \tType: %s" % (self.name, self.id, self.type.name))


class Staff(User):
    __allocated_section = [0, ""]

    def __init__(self, id: int, name: str, type: UserType):
        super().__init__(id, name, type)

    def get_allocation(self):
        return self.__allocated_section

    def set_allocation(self, grade: int, section_name: str):
        self.__allocated_section[0] = grade
        self.__allocated_section[1] = section_name

    def set_missing_students(self, grade: int, section: str, missing_students: []):
        if self.__allocated_section != "":
            if grade != self.__allocated_section[0] or section != self.__allocated_section[1]:
                print("This staff member is allocated to ", self.__allocated_section)
                return
            else:
                attendance[grade][section].append(missing_students)

    def show_weekly_attendance(self, student_id: int, time_span: int):
        missing_attendance = 0
        _time_span = 1
        for r in attendance[self.__allocated_section[0]][self.__allocated_section[1]]:
            for missing in r:
                if missing == student_id:
                    missing_attendance += 1
                    break
            if _time_span == time_span:
                print("Student with ID: ", student_id, " was missing ", missing_attendance, " times")
                return
            _time_span += 1
        else:
            print("Student with ID: ", student_id, " was missing ", missing_attendance, " times")


class Admin(User):
    def __int__(self, id: int, name: str, type: UserType):
        super().__init__(id, name, type)

    def add_grade(self, grade: int):
        database[grade] = {}
        attendance[grade] = {}

    def add_section(self, grade, sectionName):
        database[grade][sectionName] = []
        attendance[grade][sectionName] = []

    def add_student(self, grade: int, sectionName: str, id: int):
        database[grade][sectionName].append(id)

    def add_staff_member(self, id: int):
        staff_members.append(id)

    def allocate_staff(self, staff: Staff, grade: int, section_name: str):
        staff.set_allocation(grade, section_name)


admin_1 = Admin(1, "Admin1", UserType.ADMIN)
staff_1 = Staff(2, "User1", UserType.STAFF)
staff_members.append(admin_1)
staff_members.append(staff_1)

admin_1.allocate_staff(staff_1, 2, "b")

admin_1.add_grade(1)
admin_1.add_section(1, "a")
admin_1.add_student(1, "a", 1)
admin_1.add_student(1, "a", 2)
admin_1.add_student(1, "a", 3)
admin_1.add_student(1, "a", 4)
admin_1.add_student(1, "a", 5)
admin_1.add_student(1, "a", 6)

admin_1.add_section(1, "b")
admin_1.add_student(1, "b", 7)
admin_1.add_student(1, "b", 8)
admin_1.add_student(1, "b", 9)
admin_1.add_student(1, "b", 10)
admin_1.add_student(1, "b", 11)
admin_1.add_student(1, "b", 12)

admin_1.add_grade(2)
admin_1.add_section(2, "b")
admin_1.add_student(2, "b", 13)
admin_1.add_student(2, "b", 14)
admin_1.add_student(2, "b", 15)
admin_1.add_student(2, "b", 16)
admin_1.add_student(2, "b", 17)
admin_1.add_student(2, "b", 18)

print(database)

missing_students = [13, 15, 18]
staff_1.set_missing_students(2, "b", missing_students)
missing_students = [13, 15]
staff_1.set_missing_students(2, "b", missing_students)
print(attendance)

staff_1.show_weekly_attendance(13, 3)


def menu():
    choice = 0
    while choice != 9:
        choice = int(input("1) Admin 2) Staff 9) exit "))
        if choice == 1:
            admin_menu()


def admin_menu():
    choice = 0
    while choice != 9:
        print("")
        print(database)
        print("")
        print("1) To add grade 2) To add section 3) To add students 4) To allocate staff 9) To exit ")
        choice = int(input("What admin command would you like to perform? "))
        if choice == 9:
            return
        elif choice == 1:
            grade_to_add = int(input("What grade would you like to add? "))
            admin_1.add_grade(grade_to_add)
        elif choice == 2:
            grade_to_add_to = int(input("Which grade would you like to add the section to? "))
            section_to_add = input("What is the name of the section you would like to add? ")
            try:
                admin_1.add_section(grade_to_add_to, section_to_add)
            except KeyError as k:
                print("This grade does not exist, please try again")
        elif choice == 3:
            grade_to_add_to = int(input("Which grade would you like to add the student to? "))
            section_to_add_to = input("Which section would you like to add the student to?")
            student_id = int(input("Please enter the student ID: "))
            try:
                admin_1.add_student(grade_to_add_to, section_to_add_to, student_id)
            except KeyError:
                print("There was an error in the grade or section, please try again")
        elif choice == 4:
            print("Staff member id's:")
            print_staff_members()
            staff_to_add = int((input("What is the staff id of the staff member would you like to allocate? ")))
            staff_to_add = get_staff_member(staff_to_add)

            grade_to_add_to = int(input("What is the grade you would like to allocate them to? "))
            section_to_add_to = input("Which section would you like to allocate them to? ")
            try:
                admin_1.allocate_staff(staff_to_add, grade_to_add_to, section_to_add_to)
            except Exception as e:
                print("There has been an error, please try again" + e)


