from School import Student, Teacher, Lesson, Parent, Meeting, LazyTeacher

if __name__ == '__main__':
    parent1 = Parent([], True)
    student = Student('Alex', parent1, [5, 4, 5], )
    print(student.is_excellent)
    teacher = Teacher(True)
    teacher2 = LazyTeacher()
    lesson = Lesson(teacher, [student])
    lesson.learning()
    meeting = Meeting([teacher, teacher2], [], [lesson])
    print(meeting.meeting())
    print(lesson.rating_log)
