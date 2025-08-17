# -*- encoding: utf-8 -*-
# ---------https://www.cnblogs.com/Forever77/p/11135124.html
import xlrd
"""
使用xlrd模块之前需要先导入import xlrd，xlrd模块可读取xls文件。

获取工作簿对象：book = xlrd.open_workbook('excel文件名称')

获取所有工作表名称：names = book.sheet_names()，结果为列表

根据索引获取工作表对象：sheet = book.sheet_by_index(i)

根据名称获取工作表对象：sheet = book.sheet_by_name('工作表名称')

获取工作表行数：rows = sheet.nrows

获取工作表列数：cols = sheet.ncols

获取工作表某一行的内容：row = sheet.row_values(i) ，结果为列表   【sheet.row(i)，列表】

获取工作表某一列的内容：col = sheet.col_values(i)  结果为列表   【sheet.col(i)，列表】

获取工作表某一单元格的内容：cell = sheet.cell_value(m,n)、 
                        sheet.cell(m,n).value、sheet.row(m)[n].value，
                        sheet.col(n)[m].value，
                        结果为字符串或数值    
                        【sheet.cell(0,0)，xlrd.sheet.Cell对象】
"""
# -------------------------- 读 --------------------


# 根据指定的表名，读取指定工作表数据
# 逐行读取， 逐列读取
def read_excel_once(excel_name, sheet_name):
    """
        根据指定的表名，读取指定工作表数据
    :param excel_name: excel表名（注意带后缀名）
    :param sheet_name: 需要读取的工作表名称
    :return: 逐行读取， 逐列读取
    """
    # 获取工作簿对象
    book = xlrd.open_workbook(excel_name)

    # 根据名称获取工作表对象
    sheet = book.sheet_by_name(sheet_name)

    # 逐行读取数据
    row_data = [sheet.row_values(i) for i in range(sheet.nrows)]

    # 逐列读取数据
    columns_data = [sheet.col_values(i) for i in range(sheet.ncols)]

    return row_data, columns_data


# 指定读取表或多去所有工作表, 逐行读取或者逐列读取
# num: 1：读取所有    2，指定读取
# row_or_columns: 1：逐行读取    2，逐列读取
def read_excel_all(excel_name, num=1, row_or_columns=1):
    """
         指定读取表或多去所有工作表, 逐行读取或者逐列读取
    :param excel_name: excel表名
    :param num: 1：读取所有    2，指定读取
    :param row_or_columns: 1：逐行读取    2，逐列读取
    :return:
    """
    # 获取工作簿对象
    book = xlrd.open_workbook(excel_name)
    # 获取所有工作表名称
    names = book.sheet_names()
    # 逐行读取
    row_datas = lambda sheet: [sheet.row_values(i) for i in range(sheet.nrows)]
    # 逐列读取
    columns_datas = lambda sheet: [sheet.col_values(i) for i in range(sheet.ncols)]

    if num == 1:
        # 读取所有表
        data = []
        for sheet_name in names:
            # 根据名称获取工作表对象
            sheet = book.sheet_by_name(sheet_name)

            if row_or_columns == 1:
                data.append(row_datas(sheet))
            else:
                data.append(columns_datas(sheet))
    else:
        # 指定sheet表读取
        name_list = []  # 缓存选择数据
        data = []
        try:
            while True:
                [print(f'{i}----{names[i]}') for i in range(len(names))]

                # 输入选择
                num = input('请输入相应序号选择表（一次输入一个， 输入"stop"结束选择）：')

                if num == 'stop':
                    break
                elif num.split():
                    numbers = num.split()[0]

                else:
                    print('请选择!!!')
                    continue
                name_list.append(names[int(numbers)])
            for sheet_name in name_list:
                # 根据名称获取工作表对象
                sheet = book.sheet_by_name(sheet_name)
                if row_or_columns == 1:
                    data.append(row_datas(sheet))
                else:
                    data.append(columns_datas(sheet))


        except Exception as e:
            print('重新启动程序，请规范操作：', e)
    return data


if __name__ == '__main__':
    # data = read_excel_all('房天下房源数据.xls', num=2)
    # print(data)
    # read_excel_once('房天下房源数据.xls', '房源详情')
    pass





