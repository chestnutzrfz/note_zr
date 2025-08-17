# 导入第三方模块
import matplotlib.pyplot as plt

# 设置绘图的主题风格（不妨使用R中的ggplot分隔）
plt.style.use('ggplot')

# 构造数据
# str=['Kyoto', 'Japan', '江苏苏州', '上海', 'Wien', 'Austria', '北京', '北京', '江苏连云港', '湖北武汉', '北京', '上海', '福建泉州', '陕西西安', '北京', 'Singapore']
edu = [0.25,0.125,0.0625,0.0625,0.0625,0.0625,0.0625,0.0625,0.0625,0.0625,0.0625,0.0625]
""""
{'北京': 0.25, '上海': 0.125, '江苏连云港': 0.0625, '福建泉州': 0.0625, '湖北武汉': 0.0625, 'Japan': 0.0625, 'Wien': 0.0625, '江苏苏州': 0.0625, 'Austria': 0.0625,
 'Singapore': 0.0625, '陕西西安': 0.0625, 'Kyoto': 0.0625}



"""
labels = ['北京','上海','江苏连云港','福建泉州','湖北武汉','Japan','Wien','江苏苏州','Austria','Singapore','陕西西安','Kyoto']

explode = [0.1,0,0,0,0,0,0,0,0,0,0,0]  # 用于突出显示bj学历人群
colors=['#9999ff','#ff9999','#7777aa','#2442aa','#dd5555','#aa7777','#5555dd','#a8bb19','#7cb9e8','#ff7e00','#ff033e','#9966cc'] # 自定义颜色

# 中文乱码和坐标轴负号的处理
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 将横、纵坐标轴标准化处理，保证饼图是一个正圆，否则为椭圆
plt.axes(aspect='equal')

# 控制x轴和y轴的范围
plt.xlim(0,4)
plt.ylim(0,4)

# 绘制饼图
plt.pie(x = edu, # 绘图数据
        explode=explode, # 突出显示大专人群
        labels=labels, # 添加教育水平标签
        colors=colors, # 设置饼图的自定义填充色
        autopct='%.1f%%', # 设置百分比的格式，这里保留一位小数
        pctdistance=0.8,  # 设置百分比标签与圆心的距离
        labeldistance = 1.15, # 设置教育水平标签与圆心的距离
        startangle = 180, # 设置饼图的初始角度
        radius = 1.5, # 设置饼图的半径
        counterclock = False, # 是否逆时针，这里设置为顺时针方向
        wedgeprops = {'linewidth': 1.5, 'edgecolor':'green'},# 设置饼图内外边界的属性值
        textprops = {'fontsize':12, 'color':'k'}, # 设置文本标签的属性值
        center = (1.8,1.8), # 设置饼图的原点
        frame = 1 )# 是否显示饼图的图框，这里设置显示

# 删除x轴和y轴的刻度
plt.xticks(())
plt.yticks(())
# 添加图标题
plt.title('怒之火')

# 显示图形
plt.show()