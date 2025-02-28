from bs4 import BeautifulSoup
from requests import get
import time
from datetime import datetime
from tabulate import tabulate


DATE_TIME_FORMAT = "%d/%m/%Y %H:%M"


def read_courses():
    with open("courses.txt", encoding="utf-8") as file:
        return file.readlines()


def find_rows_with_course(tag):
    courses = [course.strip() for course in read_courses()]
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
        date_and_time = remove_whitespace(cells_row[4].text)
        course["Ultimo Update"] = (
            datetime.strptime(date_and_time, DATE_TIME_FORMAT)
            if date_and_time != ""
            else datetime(2000, 1, 1, 12, 0)
        )
        data_courses.append(course)
    data_courses = sorted(data_courses, key=lambda c: c["Ultimo Update"], reverse=True)
    return data_courses


def make_markdown_table(data_courses):
    headers = data_courses[0].keys()
    rows = [list(course.values()) for course in data_courses]
    markdown_table = tabulate(rows, headers=headers, tablefmt="pipe")
    with open("courses.md", "w", encoding="utf-8") as file:
        file.write(markdown_table)


def main():
    SECONDS = 8
    while True:
        courses_html = get(
            "https://gestiondocente.info.unlp.edu.ar/cursadas/", verify=False
        )

        soup = BeautifulSoup(courses_html.text, "html.parser")
        course_rows = soup.find_all(find_rows_with_course)
        data_courses = get_data_courses(course_rows)
        make_markdown_table(data_courses)
        time.sleep(SECONDS)


if __name__ == "__main__":
    main()
