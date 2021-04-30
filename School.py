from __future__ import annotations

from random import randint


class Student:
    def __init__(self, name: str, parent: Parent, marks: list[int] = None):
        self.parent = parent
        self.parent.add_child(self)
        self.__name = name
        self.__marks = marks
        self.__average_score = sum(self.__marks) / len(self.__marks)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def is_excellent(self) -> bool:
        return self.__average_score >= 4.5

    def add_mark(self, mark: int) -> None:
        self.__marks.append(mark)
        self.__average_score = sum(self.__marks) / len(self.__marks)


class Teacher:
    def __init__(self, good_mood: bool):
        self.__good_mood = good_mood
        self.__count = 0

    def add_marks(self, student: Student) -> int:
        if self.__good_mood:
            if student.is_excellent:
                student.add_mark(5)
                mark = 5
            else:
                student.add_mark(4)
                mark = 4
        else:
            if student.is_excellent:
                mark = randint(4, 5)
                student.add_mark(mark)
            else:
                mark = randint(2, 3)
                student.add_mark(randint(2, 3))
        self.check_count()
        return mark

    def check_count(self, check_count: int = 5) -> None:
        self.__count += 1
        if self.__count == check_count:
            self.__good_mood = bool(randint(0, 1))
            self.__count = 0


class Lesson:
    def __init__(self, teacher: Teacher, students: list[Student]):
        self.__students = students
        self.__teacher = teacher
        self.rating_log = dict()

    @property
    def teacher(self) -> Teacher:
        return self.__teacher

    def learning(self) -> None:
        count = randint(0, 5)
        for i in range(count):
            index = randint(0, len(self.__students) - 1)
            self.rating_log[self.__students[index]] = self.__teacher.add_marks(self.__students[index])


class LazyTeacher(Teacher):
    def __init__(self, const_mark: int = 5, good_mood=True):
        super(LazyTeacher, self).__init__(good_mood)
        self.__const_mark = const_mark if 2 <= const_mark <= 5 else 5

    def add_marks(self, student: Student) -> int:
        student.add_mark(self.__const_mark)
        return self.__const_mark


class Parent:
    def __init__(self, student: list[Student], good_mood: bool):
        self.__childs = student
        self.__good_mood = good_mood

    def add_child(self, student: Student) -> None:
        if student not in self.__childs:
            self.__childs.append(student)

    def say_about_each(self) -> None:
        for student in self.__childs:
            self.say(student)

    def say_about_all(self) -> None:
        sum_ = sum((int(student.is_excellent) for student in self.__childs))
        print('Мои дети молодцы' if sum_ >= len(self.__childs) and self.__good_mood else f'Мои дети идиоты')

    def say_about_random_children(self) -> None:
        self.say(self.__childs[randint(0, len(self.__childs) - 1)])

    def say(self, student: Student) -> None:
        if student not in self.__childs:
            raise Exception('Этот ребенок не принадлежит этому родителю')
        print(f'Мой ребенок {student.name} молодец'
              if student.is_excellent and self.__good_mood else f'Мой ребенок {student.name} идиот')


class Grandmother(Parent):
    def __init__(self, student: list[Student], good_mood: bool):
        super(Grandmother, self).__init__(student, good_mood)

    def say(self, student: Student) -> None:
        print(f'Мой внучек по имени {student.name} молодец!')


class Meeting:
    def __init__(self, teachers: list[Teacher], parents: list[Parent], lessons: list[Lesson]):
        self.__lessons = lessons
        self.__parents = parents
        self.__teachers = teachers

    def meeting(self) -> list[Parent]:
        absent_parents = list()
        for lesson in self.__lessons:
            if lesson.teacher not in self.__teachers:
                continue
            for student in lesson.rating_log.keys():
                if student.parent not in self.__parents:
                    absent_parents.append(student.parent)
                    continue
                student.parent.say(student)
        return absent_parents
