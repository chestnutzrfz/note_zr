# -*- coding: utf-8 -*-


import time
import string
import random
import pandas

# bit
def random_gender():
    return random.choice([0, 1])


# int
def random_age(a=18, b=48, gauss=True):
    x = min(a, b)
    y = max(a, b)
    mu = sum((x, y)) / 2
    sigma = abs(a - b) / 6
    age = random.gauss(mu, sigma) if gauss else random.uniform(x, y)
    return round(1 if age < 0 else age)


# decimal
def random_height(a=1.52, b=1.88, gender=1, gauss=True):
    x = min(a, b)
    y = max(a, b)
    mu = sum((x, y)) / 2
    sigma = abs(a - b) / 6
    height = random.gauss(mu + (sigma if gender else -sigma), sigma) if gauss else random.uniform(x, y)
    return round(1.2 if height < 1.2 else height, 2)


# char
def random_tel():
    pre_tel = random.choice(['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182',
                             '187', '188', '147', '130', '131', '132', '155', '156', '185', '186', '133', '153', '180',
                             '189'])
    next_tel = ''.join([random.choice(string.digits) for i in range(8)])
    return pre_tel + next_tel


# varchar
def random_name():
    name_list = [
        'Captain America',  # 美队
        'Iron Man',  # 钢铁侠
        'Thor Odinson',  # 雷神
        'Hulk',  # 浩克
        'Black Widow',  # 黑寡妇
        'Hawkeye',  # 鹰眼
        'Scarlet Witch',  # 绯红女巫
        'Quicksilver',  # 快银
        'Vision',  # 幻视
        'War Machine',  # 战争机器
        'Falcon',  # 猎鹰
        'Winter Soldier',  # 冬兵
        'Black Panther',  # 黑豹
        'Ant Man',  # 蚁人
        'Spider Man',  # 蜘蛛侠
        'Wasp',  # 黄蜂女
        'Doctor Strange',  # 奇异博士
        'Captain Marvel',  # 惊奇队长
    ]
    return random.choice(name_list)


# date
def random_birth(age):
    year = int(time.strftime('%Y', time.localtime())) - age
    month = random.randint(1, 12)
    day = random.randint(1, 31)

    birth = '{}-{}-{}'.format(year, month, day)
    try:
        time.strptime(birth, '%Y-%m-%d')
    except ValueError:
        birth = '{}-{}-{}'.format(year, month, day - 3)
    finally:
        return birth


def random_data():
    gender = random_gender()
    age = random_age()

    # varchar, bit, int, decimal, date, char
    return random_name(), random_gender(), random_birth(age=age), random_age(), random_height(
        gender=gender), random_tel()


if __name__ == '__main__':
    lis = []
    for i in range(20):
        print(random_data())
        lis.append(random_data())

    df = pandas.DataFrame(lis,columns=["name","gender",'birth',"age","height",'tel'])

    df.to_csv('mydata.csv',index=False)
