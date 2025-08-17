import pandas as pd
import matplotlib.pyplot as plt
# 设置绘图风格
plt.style.use('ggplot')
# 设置中文编码和负号的正常显示
plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False
df=pd.read_csv("E:\difan_demo\中国大学综合排名数据分析\gdp.csv")
# 导入模块
import matplotlib as mpl
# 设置图框的大小
fig = plt.figure(figsize=(10,6))
df1=df.date
df2=[df1]
print(df1)
# 绘图
plt.plot(df.date, # x轴数据
         df.total_expenditures, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = 'steelblue', # 折线颜色
         marker = 'o', # 点的形状
         markersize = 6, # 点的大小
         markeredgecolor='black', # 点的边框色
         markerfacecolor='steelblue') # 点的填充色
plt.plot(df.date, # x轴数据
         df.labor_force_pr, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = '#ff9999', # 折线颜色
         marker = 'o', # 点的形状
         markersize = 6, # 点的大小
         markeredgecolor='black', # 点的边框色
         markerfacecolor='#ff9999', # 点的填充色
         label = 'labor') # 添加标签
plt.plot(df.date, # x轴数据
         df.producer_price_index, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = '#ff9999', # 折线颜色
         marker = 'o', # 点的形状
         markersize = 6, # 点的大小
         markeredgecolor='black', # 点的边框色
         markerfacecolor='#ffff99', # 点的填充色
         label = 'producer') # 添加标签
plt.plot(df.date, # x轴数据
         df.gross_domestic_product, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = '#ff9999', # 折线颜色
         marker = 'o', # 点的形状
         markersize = 6, # 点的大小
         markeredgecolor='black', # 点的边框色
         markerfacecolor='#9999ff', # 点的填充色
         label = 'gross') # 添加标签
# 添加标题和坐标轴标签
plt.title('gdp')
plt.xlabel('日期')
plt.ylabel('数量')
# 剔除图框上边界和右边界的刻度
plt.tick_params(top = 'off', right = 'off')
# 获取图的坐标信息
ax = plt.gca()
# 设置x轴显示多少个日期刻度
xlocator = mpl.ticker.LinearLocator(23)
# 设置x轴每个刻度的间隔天数
ax.xaxis.set_major_locator(xlocator)
# 为了避免x轴日期刻度标签的重叠，设置x轴刻度自动展现，并且45度倾斜
fig.autofmt_xdate(rotation = 45)
# 显示图形
plt.show()