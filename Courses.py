from bs4 import BeautifulSoup
from requests import get
from json import dumps
import os
import time
from datetime import datetime

COURSES_2023_2ND_SEMESTER = [
    "Redes y Comunicaciones",
    "Programación Concurrente",
    "Computabilidad y Complejidad",
    "Laboratorio de Software",
    "Lógica e Inteligencia Artificial",
    "Matemática 4",
]

ELECTIVES_2023_2ND_SEMESTER = [

]

ALL_COURSES_2023 = COURSES_2023_2ND_SEMESTER + ELECTIVES_2023_2ND_SEMESTER


def find_rows_with_course(tag):
    if tag.name == "tr":
        first_table_cell = tag.find("td")
        if (first_table_cell) and (first_table_cell.text in ALL_COURSES_2023):
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


def print_data_courses(data_courses):
    print("\n")
    print(datetime.now().strftime("%H:%M:%S"))
    for course in data_courses:
        print(dumps(course, indent=2, ensure_ascii=False))


def main():
    SECONDS = 1800
    while True:
        courses_html = get(
            "https://gestiondocente.info.unlp.edu.ar/cursadas/", verify=False
        )

        soup = BeautifulSoup(courses_html.text, "html.parser")
        course_rows = soup.find_all(find_rows_with_course)
        data_courses = get_data_courses(course_rows)
        data_courses_2023 = [
            dict for dict in data_courses if "2023" in dict["Ultimo Update"]
        ]
        os.system("cls" if os.name == "nt" else "clear")

        print("Fecha límite de inscripciones a asignaturas: 13/8")
        print("Fecha límite de inscripciones a redictados: 10/8")
        print_data_courses(data_courses_2023)

        time.sleep(SECONDS)


main()
