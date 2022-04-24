class Student:
    instance_list = []

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.student_grades = {}
        Student.instance_list.append(self)

    def average_grade(self):
        """Сalculate the student's average grade for all courses."""
        s = sum([v for v in self.student_grades.values()], [])
        return round(sum(s) / len(s), 2)

    def rate_lecturer(self, lecturer, course, grade):
        """Rate a lecturer from a student for a certain course."""
        check_list = ['- отсуствие такого лектора', '- курс не закреплен за данным лектором',
                      '- курс не проходится сейчас студентом', '- оценка не в диапазоне от 1 до 10']
        check_bool = [isinstance(lecturer, Lecturer), course in lecturer.courses_attached,
                      course in self.courses_in_progress, grade in range(1, 11)]
        if sum(check_bool) == 4:
            print(f'<Оценка {grade} лектору {lecturer.name} {lecturer.surname} за курс "{course}" добавлена>')
            if course in lecturer.grades_from_students:
                lecturer.grades_from_students[course] += [grade]
            else:
                lecturer.grades_from_students[course] = [grade]
        else:
            print(f'<Ошибка добавления оценки лектору {lecturer.name} {lecturer.surname} '
                  f'от студента {self.name} {self.surname} за курс "{course}">')
            print('Причина:' if sum(check_bool) == 3 else 'Причины:')
            print(*[mist for i, mist in enumerate(check_list) if not check_bool[i]], sep=';\n')

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}\n' \
               f'Средняя оценка за домашние задания: {self.average_grade()}\n' \
               f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n' \
               f'Завершенные курсы: {", ".join(self.finished_courses)}'

    def __lt__(self, other):
        if not isinstance(other, Student):
            print(f'<Ошибка: {other} - не студент>')
        else:

            return self.average_grade() < other.average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


class Lecturer(Mentor):
    instance_list = []

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades_from_students = {}
        Lecturer.instance_list.append(self)

    def average_grade(self):
        """Сalculate the lecturer's average grade for all courses."""
        s = sum([v for v in self.grades_from_students.values()], [])
        return round(sum(s) / len(s), 2)

    def __str__(self):
        return f'{super().__str__()}\nСредняя оценка за лекции: {self.average_grade()}'

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print(f'<Ошибка: {other} - не лектор>')
        else:
            return self.average_grade() < other.average_grade()


class Reviewer(Mentor):
    def rate_student(self, student, course, grade):
        """Rate a student from a reviewer for a certain course."""
        check_list = ['- отсуствие такого студента', '- курс не закреплен за данным ревьюером',
                      '- курс не проходится сейчас студентом', '- оценка не в диапазоне от 1 до 10']
        check_bool = [isinstance(student, Student), course in self.courses_attached,
                      course in student.courses_in_progress, grade in range(1, 11)]
        if sum(check_bool) == 4:
            print(f'<Оценка {grade} студенту {student.name} {student.surname} за курс "{course}" добавлена>')
            if course in student.student_grades:
                student.student_grades[course] += [grade]
            else:
                student.student_grades[course] = [grade]
        else:
            print(f'<Ошибка добавления оценки студенту {student.name} {student.surname} '
                  f'от ревьюера {self.name} {self.surname} за курс "{course}">')
            print('Причина:' if sum(check_bool) == 3 else 'Причины:')
            print(*[mist for i, mist in enumerate(check_list) if not check_bool[i]], sep=';\n')


def students_average_course(course):
    """Сalculate the average grade of students for the selected course."""
    av_list = []
    for student in Student.instance_list:
        if course in student.student_grades:
            av_list.append(round(sum(student.student_grades[course]) / len(student.student_grades[course]), 2))
    return round(sum(av_list) / len(av_list), 2)


def lecturers_average_course(course):
    """Сalculate the average grade of lecturers for the selected course."""
    av_list = []
    for lecturer in Lecturer.instance_list:
        if course in lecturer.grades_from_students:
            av_list.append(round(sum(lecturer.grades_from_students[course])
                                 / len(lecturer.grades_from_students[course]), 2))
    return round(sum(av_list) / len(av_list), 2)


# Create instances of classes and assign attributes.
# Students:
st_01 = Student('Laurel', 'Hubbard', 'transgender')
st_01.courses_in_progress += ['Macrame', 'Oratory']
st_01.finished_courses += ['Nuclear Physics']
st_01.student_grades['Macrame'] = [10, 10, 10, 9, 10]
st_01.student_grades['Oratory'] = [8, 7, 9, 8, 8, 6, 7]
st_01.student_grades['Nuclear Physics'] = [10, 8, 7, 4, 4, 10, 8, 6, 9, 3]

st_02 = Student('Greta', 'Thunberg', 'woman')
st_02.courses_in_progress += ['Macrame', 'Oratory']
st_02.finished_courses += ['Nuclear Physics']
st_02.student_grades['Macrame'] = [8, 7, 5, 9, 3]
st_02.student_grades['Oratory'] = [10, 9, 10, 8, 9, 10, 10]
st_02.student_grades['Nuclear Physics'] = [3, 5, 7, 6, 4, 8, 7, 6, 5, 4]

st_03 = Student('Bart', 'Simpson', 'man')
st_03.courses_in_progress += ['Macrame', 'Nuclear Physics']
st_03.finished_courses += ['Oratory']
st_03.student_grades['Macrame'] = [8, 7, 5, 9, 3]
st_03.student_grades['Oratory'] = [7, 8, 6, 8, 7, 9, 5, 6, 6, 4]
st_03.student_grades['Nuclear Physics'] = [3, 5, 7, 6, 4, 8, 5, 4]

st_04 = Student('Veselin', 'Lazarev', 'man')
st_04.courses_in_progress += ['Oratory', 'Nuclear Physics']
st_04.student_grades['Nuclear Physics'] = [10, 9, 10, 8, 10, 10, 9, 10]

# Lecturers:
lec_01 = Lecturer('Gianfranco', 'Ferdyshchenko')
lec_01.courses_attached += ['Macrame', 'Oratory']
lec_01.grades_from_students['Oratory'] = [5, 9, 8, 7, 7, 8, 7, 8, 7, 8]
lec_01.grades_from_students['Macrame'] = [5, 5, 5, 6, 6, 7, 8, 5, 4, 2]

lec_02 = Lecturer('Octavian', 'Augustus')
lec_02.courses_attached += ['Macrame', 'Oratory']
lec_02.grades_from_students['Macrame'] = [8, 9, 5, 4, 10, 9, 7, 8, 7, 6]
lec_02.grades_from_students['Oratory'] = [9, 8, 7, 3, 10, 8, 8, 6, 3, 6]

lec_03 = Lecturer('Olga', 'Buzova-Tarasova')
lec_03.courses_attached += ['Nuclear Physics']
lec_03.grades_from_students['Nuclear Physics'] = [1, 6, 4, 9, 8, 7, 3, 9, 3, 2, 4, 9, 5, 4, 5]

# Reviewers:
rev_01 = Reviewer('Slava', 'Zaitsev')
rev_01.courses_attached += ['Macrame', 'Oratory']

rev_02 = Reviewer('Vanga', 'Surcheva')
rev_02.courses_attached += ['Oratory', 'Nuclear Physics']
