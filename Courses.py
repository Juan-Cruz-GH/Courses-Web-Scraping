from bs4 import BeautifulSoup
from requests import get
from json import dumps
import os
import time
from datetime import datetime

COURSES_2023_1ST_SEMESTER = [
    "Ingeniería de Software 2",
    "Aspectos Legales y Profesionales de Informática",
]

ELECTIVES_2023_1ST_SEMESTER = [
    "Aspectos Éticos, Sociales y Profesionales Avanzados de Informática",
    "Desarrollo Seguro de Aplicaciones",
    "Internet de las Cosas",
    "Introducción a Blockchain, Criptomonedas y Smart Contracts",
    "Java y Aplicaciones Avanzadas sobre Internet",
    "Minería de Datos Utilizando Sistemas Inteligentes",
    "Web Semántica y Grafos de Conocimiento",
]

ALL_COURSES_2023 = COURSES_2023_1ST_SEMESTER + ELECTIVES_2023_1ST_SEMESTER


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

        print("Fecha límite de inscripciones a asignaturas: 5/3")
        print("Fecha límite de inscripciones a redictados: 28/2")
        print_data_courses(data_courses_2023)

        time.sleep(SECONDS)


main()
