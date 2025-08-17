# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# # 设置绘图风格
# plt.style.use('ggplot')
# # 设置中文编码和负号的正常显示
# plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
# plt.rcParams['axes.unicode_minus'] = False
# df=pd.read_csv("E:\difan_demo\中国大学综合排名数据分析\gdp.csv")
# # 提取不同性别的年龄数据
# df_1=df.total_expenditures.min()
# df_2=df.labor_force_pr.min()
# df_3=df.producer_price_index.min()
# df_4=df.gross_domestic_product.min()
# date=[df_1,df_2,df_3,df_4]
# print(date)
# plt.bar(range(4),date, # 绘图数据
#          align = 'center',color='steelblue', alpha = 0.8)
# # 设置坐标轴标签和标题
# plt.title('gdp柱形图')
# plt.xticks(range(4),['total','labor','producer','gross'])
# plt.ylim([50,15000])
# plt.xlabel('gdp')
# plt.ylabel('累计频率')
# # 去除图形顶部边界和右边界的刻度
# plt.tick_params(top='off', right='off')
# # 显示图例
# plt.legend(loc = 'best')
# # 显示图形
# plt.show()