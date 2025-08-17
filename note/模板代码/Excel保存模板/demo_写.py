# -*- encoding: utf-8 -*-
import os

import xlwt
"""
使用xlwt模块之前需要先导入import xlwt，xlwt模块只能写xls文件

创建工作簿：book = xlwt.Workbook()，如果写入中文为乱码，可添加参数encoding = 'utf-8'

创建工作表：sheet = book.add_sheet('Sheet1')

向单元格写入内容：sheet.write(m,n,'内容1')、sheet.write(x,y,'内容2')

保存工作簿：book.save('excel文件名称')，
          默认保存在py文件相同路径下，如果该路径下有相同文件，会被新创建的文件覆盖，即xlwt不能修改文件。

"""


# 逐行写入
# 一组数据为一行的数据
def write_row(data, file_name, sheet_name='Sheet1', dir_path='数据'):
    """
        逐行写入
    :param data: 数据
    :param file_name: 保存excel名
    :param sheet_name: 工作子表名
    :param dir_path: 保存路径
    :return: 成功：successfully
    """
    #
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # 保存路径重构
    file_path = os.path.join(dir_path, file_name)

    # 创建工作簿：
    book = xlwt.Workbook()

    # 创建工作表：
    sheet = book.add_sheet(sheet_name)

    for row in range(len(data)):  # 行
        for columns in range(len(data[row])):  # 列
            sheet.write(row, columns, data[row][columns])

    book.save(file_path)

    return 'successful'


#  逐列写入
#  遗嘱数据为一列的数据
def write_col(data, file_name, sheet_name='Sheet1', dir_path='数据'):
    """
        逐列写入
    :param data: 数据
    :param file_name: 保存excel名
    :param sheet_name: 工作子表名
    :param dir_path: 保存路径
    :return: 成功：successfully
    """
    #
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # 保存路径重构
    file_path = os.path.join(dir_path, file_name)

    # 创建工作簿：
    book = xlwt.Workbook()

    # 创建工作表：
    sheet = book.add_sheet(sheet_name)

    # 逐列数据
    for columns in range(len(data)):  # 列
        for row in range(len(data[columns])):  # 行
            sheet.write(row, columns, data[columns][row])

    book.save(file_path)

    return 'successful'


if __name__ == '__main__':
    data = [['名称', '单价/元', '库存/kg'],
            ['苹果', '梨', '香蕉', '橘子']]

    # write_row(data, '测试.xls')
    write_col(data, '测试.xls')


