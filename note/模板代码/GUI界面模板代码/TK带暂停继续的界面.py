"""
该窗体界面拓展性高
具体更改流程如下：

1.将用户名可替换为爬虫检索用户输入的关键词输入

2.密码可替换为账号登录的cookie输入

3.Text富文本框该位置课选择输出爬虫效果print内容

4.对比事件绑定方法借鉴，即可创建程序执行关联函数
"""
import tkinter as tk
import tkinter.messagebox as msgbox
from threading import Thread
from requests_html import HTMLSession
from PIL import Image, ImageTk
session = HTMLSession()
import os, time, cv2

# def get_image(file_name, width, height):
#     im = Image.open(file_name).resize((width, height))
#     return ImageTk.PhotoImage(im)


class TKSpider(object):

    def __init__(self):
        """定义可视化窗口，并设置窗口和主题大小布局"""
        self.window = tk.Tk()
        self.window.title('爬虫数据采集')
        self.window.geometry('800x600')

        # """给GUI添加背景图"""
        # self.canvas = tk.Canvas(self.window, width=800, height=600)
        # self.im_root = get_image('hkdg.jpg', 800, 600)
        # self.canvas.create_image(400, 300, image=self.im_root)
        # self.canvas.pack()

        """创建label_user按钮，与说明书"""
        self.label_user = tk.Label(self.window, text='请输入检索词：', font=('Arial', 12), width=30, height=2)
        self.label_user.pack()
        """创建label_user关联输入"""
        self.entry_user = tk.Entry(self.window, show=None, font=('Arial', 14))
        self.entry_user.pack(after=self.label_user)

        self.label_cookie = tk.Label(self.window, text='请输入COOKIE', font=('Arial', 12), width=30, height=2)
        self.label_cookie.pack()
        """创建label_user关联输入"""
        self.entry_cookie = tk.Entry(self.window, show=None, font=('Arial', 14))
        self.entry_cookie.pack(after=self.label_cookie)

        """创建Text富文本框，用于按钮操作结果的展示"""
        # 定义富文本框滑动条
        scroll = tk.Scrollbar()
        # 放到窗口的右侧, 填充Y竖直方向
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text1 = tk.Text(self.window, font=('Arial', 12), width=85, height=20)
        self.text1.pack()
        # 两个控件关联
        scroll.config(command=self.text1.yview)
        self.text1.config(yscrollcommand=scroll.set)

        """定义按钮1，绑定触发事件方法"""
        """即点击运行，采集按钮，当点击时将执行parse_hit_click_1方法。在真实使用场景中"""
        """parse_hit_click_1中可替换为自己写的真正登录函数。这里仅为示例"""
        self.button_1 = tk.Button(self.window, text='运行，采集', font=('Arial', 12), width=10, height=1, command=self.parse_hit_click_1)
        self.button_1.pack(before=self.text1)

        """定义按钮2，绑定触发事件方法"""
        self.button_2 = tk.Button(self.window, text='清除', font=('Arial', 12), width=10, height=1, command=self.parse_hit_click_2)
        self.button_2.pack(anchor="e")

        """定义按钮3，绑定触发事件方法"""
        self.button_2 = tk.Button(self.window, text='暂停/继续', font=('Arial', 12), width=10, height=1,
                                  command=self.parse_hit_click_3)
        self.button_2.pack(anchor="e")
        # 判断循环计数
        self.num_if = 0
        # 全局判断条件
        self.is_running = True
        # 继续执行
        self.is_data = ''

    def parse_hit_click_1(self):
        """使用线程执行爬虫任务，线程关联"""
        Thread(target=self.parse_spider_run).start()

    def parse_hit_click_3(self):
        Thread(target=self.parse_if_data).start()

    def parse_if_data(self):
        """程序暂停逻辑"""
        self.num_if += 1
        if self.num_if % 2 == 0:
            self.is_running = True
            self.is_data = "pause"
        else:
            self.is_running = False
            self.is_data = ''

    def parse_spider_run(self):
        """
        定义触发事件1, 将执行结果显示在文本框中
        :return: 也可作为爬虫任务函数，添加爬虫逻辑
        """
        user_name = self.entry_user.get()
        cookie = self.entry_cookie.get()
        """爬虫任务函数"""
        for page in range(1, 101):
            time.sleep(1)
            if self.is_running:
                text = f"user_name: {user_name}\ncookie: {cookie}\n"
                # 界面：富文本框-信息显示
                self.text1.insert("insert", f'第{page}次' + text)
                # gui界面滑动条自动下拉
                self.text1.see('insert')
                # 报错提示
                # msgbox.showerror(title='错误', message='无效，请重新输入！')
                """调用爬虫任务函数"""
                self.parse_start_url(page)
            else:
                text = "----------暂停中----------\n"
                # 界面：富文本框-信息显示
                self.text1.insert("insert", f'第{page}次' + text)
                # gui界面滑动条自动下拉
                self.text1.see('insert')
                while True:
                    if len(self.is_data) > 0:
                        break
                    time.sleep(1.5)
                """调用爬虫任务函数"""
                self.parse_start_url(page)

    def parse_start_url(self, page):
        """
        爬虫任务函数，发送请求
        :param page: 地址拼接页码
        :return:
        """
        pass

    def parse_hit_click_2(self):
        """定义触发事件2，删除文本框中内容"""
        self.entry_user.delete(0, "end")
        self.entry_cookie.delete(0, "end")
        self.text1.delete("1.0", "end")

    def center(self):
        """创建窗口居中函数方法"""
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = int((ws / 2) - (800 / 2))
        y = int((hs / 2) - (600 / 2))
        self.window.geometry('{}x{}+{}+{}'.format(800, 600, x, y))

    def run_loop(self):
        """禁止修改窗体大小规格"""
        self.window.resizable(False, False)
        """窗口居中"""
        self.center()
        """窗口维持--持久化"""
        self.window.mainloop()


if __name__ == '__main__':
    t = TKSpider()
    t.run_loop()












