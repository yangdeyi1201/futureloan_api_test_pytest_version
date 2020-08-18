# author:CC
# email:yangdeyi1201@foxmail.com

import openpyxl


class ExcelHandler(object):
    def __init__(self, excel_path):
        self.workbook = openpyxl.load_workbook(filename=excel_path)
        self.excel_path = excel_path
        return

    def get_sheet(self, sheet_name):
        """获取表单"""
        sheet = self.workbook[sheet_name]
        return sheet

    def read_sheet(self, sheet_name):
        """读取表单"""
        sheet = self.get_sheet(sheet_name=sheet_name)
        rows = list(sheet.rows)

        headers = [header.value for header in rows[0]]

        cases = []
        for row in rows[1:]:
            case = {}
            for index, cell in enumerate(row):
                case[headers[index]] = cell.value
            cases.append(case)

        return cases

    def write(self, sheet_name, row, column, data):
        """向表单指定单元格写入数据"""
        sheet = self.get_sheet(sheet_name)
        sheet.cell(row=row, column=column).value = data
        self.save()

    def save(self):
        """保存 excel"""
        self.workbook.save(filename=self.excel_path)


if __name__ == '__main__':
    pass
