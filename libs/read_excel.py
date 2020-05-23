import os

import xlsxwriter


def write_to_excel(projects_list):
    workbook = xlsxwriter.Workbook(os.getcwd() + "\\resources\\projects.xlsx")
    worksheet = workbook.add_worksheet()
    row = 0
    column = 0

    for pl in projects_list:
        worksheet.write(row, column, pl.text)
        row += 1
        worksheet.write(row, column, " ")
        row += 1

    workbook.close()
