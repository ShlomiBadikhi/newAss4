from persistence import repo

import os
import imp


def grade(assignments_dir, assignment_num):
    expected_output = repo.assignments.find(assignment_num).expected_output

    for assignment in os.listdir(assignments_dir):
        (student_id, ext) = os.path.splitext(assignment)

        code = imp.load_source('test', assignments_dir + '/' + assignment)

        student_grade = Grade(student_id, assignment_num, 0)
        if code.run_assignment() == expected_output:
            student_grade.grade = 100

        repo.grades.insert(student_grade)


def print_grades():
    print
    'grades:'
    for grade in repo.grades.find_all():
        student = repo.students.find(grade.student_id)

        print
        'grade of student {} on assignment {} is {}' \
            .format(student.name, grade.assignment_num, grade.grade)