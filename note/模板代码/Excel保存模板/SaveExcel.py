"""
工具库--保存excel表格使用
请仔细阅读其中的注释，理清其中的思路
在使用
"""

# pip install openpyxl
from openpyxl import workbook


class SaveExcel(object):

    def __init__(self, title_list):
        """
        创建表格
        :param title_list: 表的标头
        """
        """创建Excel对象"""
        self.wb = workbook.Workbook()
        """获取当前正在操作的表对象  激活"""
        self.ws = self.wb.active
        """设置表头"""
        self.ws.append(title_list)

    def parse_join_data(self, data):
        """
        添加数据
        :return:
        """
        self.ws.append(data)
        print('数据保存成功----logging！！！')
        # 爬虫采集数据，遍历执行保存---一条数据一条数据的写入到本地
        # 如果你的爬虫在执行数据存储到excel的过程中
        # 一条数据一条数据的写入到本地----出现了报错
        # 100w条----99w时候发生了报错
        # 只保存一次

    def save_excel(self):
        """
        数据插入完成，执行保存
        :return:
        """
        self.wb.save('test2.xlsx')


if __name__ == '__main__':
    """插入示例"""
    title_list = ['姓名', '年龄', '性别', '班级']
    s = SaveExcel(title_list)
    a1 = ['小明', '18', '男', 'python一班']
    a2 = ['小红', '18', '女', 'python一班']
    a3 = ['小黄', '20', '女', 'python一班']
    s.parse_join_data(a1)
    s.parse_join_data(a2)
    s.parse_join_data(a3)
    # 执行保存
    s.save_excel()


