from bs4 import BeautifulSoup
from requests import get
import time
from tabulate import tabulate


def read_courses():
    courses = []
    with open('courses.txt', encoding="utf-8") as file:
        for line in file:
            courses.append(line.strip())
    return courses


def find_rows_with_course(tag):
    courses = read_courses()
    if tag.name == "tr":
        first_table_cell = tag.find("td")
        if (first_table_cell) and (first_table_cell.text in courses):
            return True
    return False


def remove_whitespace(string):
    return " ".join(string.split())


def get_data_courses(course_rows):
    data_courses = []
    for row in course_rows:
        course = {}
        cells_row = row.find_all("td")
        course["Nombre"] = remove_whitespace(cells_row[0].text)
        course["Inicio Cursada"] = remove_whitespace(cells_row[2].text)
        course["Horarios Cursada"] = remove_whitespace(cells_row[3].text)
        course["Ultimo Update"] = remove_whitespace(cells_row[4].text)
        data_courses.append(course)
    return data_courses


def make_markdown_table(data_courses):
    headers = data_courses[0].keys()
    rows = [list(course.values()) for course in data_courses]
    markdown_table = tabulate(rows, headers=headers, tablefmt="pipe")
    with open("table.md", "w", encoding="utf-8") as file:
        file.write(markdown_table)


def main():
    SECONDS = 1800
    while True:
        courses_html = get(
            "https://gestiondocente.info.unlp.edu.ar/cursadas/", verify=False
        )

        soup = BeautifulSoup(courses_html.text, "html.parser")
        course_rows = soup.find_all(find_rows_with_course)
        data_courses = get_data_courses(course_rows)
        make_markdown_table(data_courses)
        time.sleep(SECONDS)
        """
            Fecha límite de inscripciones a asignaturas: 13/8
            Fecha límite de inscripciones a redictados: 10/8
        """

main()
