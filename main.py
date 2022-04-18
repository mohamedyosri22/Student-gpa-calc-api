from flask import Flask
from werkzeug.serving import WSGIRequestHandler
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)


def gpa_calc(grades):
    points = 0
    grade_c = {"A+": 4, "A": 3.67, "B+": 3.33, "B": 3.0, "B-": 2.67,
               "C+": 2.33, "C": 2.0, "C-": 1.67, "D+": 1.33, "D": 1.0, "F": 0}
    if grades != []:
        for grade in grades:
            points += grade_c[grade]
        gpa = points / len(grades)
        return gpa
    else:
        return None


def four_year_students(student_id, dep):
    try:
        if dep.lower() == 'cs':
            dataset = pd.read_csv(r"F:\Every_year_grades\4CS.csv")

        elif dep.lower() == 'is':
            dataset = pd.read_csv(r"F:\Every_year_grades\4IS.csv")

        elif dep.lower() == 'ai':
            dataset = pd.read_csv(r"F:\Every_year_grades\4AI.csv")

        elif dep.lower() == 'md':
            dataset = pd.read_csv(r"F:\Every_year_grades\4MD.csv")

        else:
            dataset = pd.read_csv(r"F:\Every_year_grades\4SC.csv")

        student_data = dataset[dataset.Id == student_id]
        student_data = student_data.iloc[:, 4:]

        student_grades = student_data.iloc[:, :]

        grades = []
        for grade in student_grades:
            grades.append(student_grades.loc[0, :][grade])

        gpa = gpa_calc(grades)

        return gpa

    except:

        return print("some thing went wrong with fourth year")


def third_year_students(student_id, dep):
    try:
        if dep.lower() == 'cs':
            dataset = pd.read_csv(r"F:\Every_year_grades\3CS.csv")

        elif dep.lower() == 'is':
            dataset = pd.read_csv(r"F:\Every_year_grades\3IS.csv")

        elif dep.lower() == 'ai':
            dataset = pd.read_csv(r"F:\Every_year_grades\3AI.csv")

        elif dep.lower() == 'md':
            dataset = pd.read_csv(r"F:\Every_year_grades\3MD.csv")

        elif dep.lower() == 'se':
            dataset = pd.read_csv(r"F:\Every_year_grades\3SE.csv")

        else:
            dataset = pd.read_csv(r"F:\Every_year_grades\3SC.csv")

        student_data = dataset[dataset.Id == student_id]
        student_data = student_data.iloc[:, 4:]

        student_grades = student_data.iloc[:, :]

        grades = []
        for grade in student_grades:
            grades.append(student_grades.loc[0, :][grade])

        gpa = gpa_calc(grades)

        return gpa

    except:

        return print("some thing went wrong third year")


def second_year_students(student_id, dep):
    try:
        if dep.lower() == 'gn':
            dataset = pd.read_csv(r"F:\Every_year_grades\2GN.csv")

        elif dep.lower() == 'md':
            dataset = pd.read_csv(r"F:\Every_year_grades\2MD.csv")

        elif dep.lower() == 'se':
            dataset = pd.read_csv(r"F:\Every_year_grades\2SE.csv")

        else:
            return print("something is wrong with the department in second year")

        student_data = dataset[dataset.Id == student_id]
        student_data = student_data.iloc[:, 4:]

        student_grades = student_data.iloc[:, :]

        grades = []
        for grade in student_grades:
            grades.append(student_grades.loc[0, :][grade])

        gpa = gpa_calc(grades)

        return gpa

    except:

        return print("some thing went wrong with second year")


def first_year_students(student_id, dep):
    try:
        if dep.lower() == 'gn':
            dataset = pd.read_csv(r"F:\Every_year_grades\1GN.csv")

        elif dep.lower() == 'md':
            dataset = pd.read_csv(r"F:\Every_year_grades\1MD.csv")

        elif dep.lower() == 'se':
            dataset = pd.read_csv(r"F:\Every_year_grades\1SE.csv")
        else:
            return print("something is wrong with the department in first year")

        student_data = dataset[dataset.Id == student_id]
        student_data = student_data.iloc[:, 4:]

        student_grades = student_data.iloc[:, :]

        grades = []
        for grade in student_grades:
            grades.append(student_grades.loc[0, :][grade])

        gpa = gpa_calc(grades)

        return gpa

    except:

        return print("some thing went wrong at first year")


# year filtering
def make_stats(student_id, year, dep):
    try:
        gpa = 0
        if year == 4:
            gpa = four_year_students(student_id, dep)

        elif year == 3:
            gpa = third_year_students(student_id, dep)

        elif year == 2:
            gpa = second_year_students(student_id, dep)

        else:
            gpa = first_year_students(student_id, dep)

        return gpa

    except:
        return print("something is wrong with the year")


# flask api
@app.route('/', methods=['POST'])
def ret_stats():

    userinp = request.json
    id = int(userinp['studentid'])
    year = int(userinp['year'])
    dep = userinp['dep']

    student_gpa = make_stats(id, year, dep)
    student_gpa = str(student_gpa)
    return jsonify({"GPA": "Student GPA = " + student_gpa})


@app.route('/')
def ind():
    return "<h1>Student stats api</h1>"


if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(port=4000, debug=True)
