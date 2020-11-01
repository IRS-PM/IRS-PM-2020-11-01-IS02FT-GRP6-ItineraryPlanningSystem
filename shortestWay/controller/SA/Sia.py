#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 18:41:02 2020

@author: andrew
"""
import base64
import io

import pandas as pd
import math
import random
import matplotlib.pyplot as plt
import sys
# from matplotlib.mlab import dist
import copy
import time

#初始温度 结束温度
T0 = 30
Tend = 1e-8
#循环控制常数
L = 50
#温度衰减系数
a = 0.98

save_path = "D:\\shortestWay1029\\shortestWay\\static\\assets\\plots\\"

map = {
        0: [1.25494, 103.82258],    # Universal Studios
        1: [1.2852, 103.8555],         # Merlion Park
        2: [1.2803799, 103.8642310],    # Gardens by the Bay
        3: [1.4043539, 103.7908343],    # Singapore Zoo
        4: [1.3108427, 103.8150717],    # Singapore Botanic Gardens
        5: [1.2893042, 103.8609481],    # Singapore Flyer
        6: [1.2489856, 103.8188008],    # Sentosa Island
        7: [1.4021926, 103.7858719],     # Night Safari
        8: [1.2899547, 103.849361],     # National Gallery Singapore
        9: [1.2966201, 103.8463208]      # National Museum of Singapore
    }

map1 = {
    0: "Universal Studios",
    1: "Merlion Park",
    2: "Gardens by the Bay",
    3: "Singapore Zoo",
    4: "Singapore Botanic Gardens",
    5: "Singapore Flyer",
    6: "Sentosa Island",
    7: "Night Safari",
    8: "National Gallery Singapore",
    9: "National Museum of Singapore"
}

time_consumption = {
    0: 5,
    1: 1,
    2: 3,
    3: 5,
    4: 3,
    5: 1,
    6: 10,
    7: 3,
    8: 2,
    9: 4
}

def init_dis_matrix(length):
    distance_matrix = [[0 for col in range(length)] for raw in range(length)]
    return distance_matrix
    
    
def load_position(file_name):
    data = pd.read_csv(file_name,names=['index','lat','lon'])
    city_x = data['lat'].tolist()
    city_y = data['lon'].tolist()
    return city_x,city_y
#构建初始参考距离矩阵
def getdistance(city_x,city_y,n_len,distance):
    for i in range(n_len):
        for j in range(n_len):
            x = pow(city_x[i] - city_x[j], 2)
            y = pow(city_y[i] - city_y[j], 2)
            distance[i][j] = pow(x + y, 0.5)
    for i in range(n_len):
        for j in range(n_len):
            if distance[i][j] == 0:
                distance[i][j] = sys.maxsize

#计算总距离
def cacl_best(rou,n_len,distence):
    sumdis = 0.0
    for i in range(n_len-1):
        sumdis += distence[rou[i]][rou[i+1]]
    sumdis += distence[rou[n_len-1]][rou[0]]     
    return sumdis

#得到新解
def getnewroute(route, time,n_len):
    #如果是偶数次，二变换法
    current = copy.copy(route)
    
    if time % 2 == 0:
        u = random.randint(0, n_len-1)
        v = random.randint(0, n_len-1)
        temp = current[u]
        current[u] = current[v]
        current[v] = temp
    #如果是奇数次，三变换法 
    else:
        temp2 = random.sample(range(0, n_len), 3)
        temp2.sort()
        u = temp2[0]
        v = temp2[1]
        w = temp2[2]
        w1 = w + 1
        temp3 = [0 for col in range(v - u + 1)]
        j =0
        for i in range(u, v + 1):
            temp3[j] = current[i]
            j += 1
        
        for i2 in range(v + 1, w + 1):
            current[i2 - (v-u+1)] = current[i2]
        w = w - (v-u+1)
        j = 0
        for i3 in range(w+1, w1):
            current[i3] = temp3[j]
            j += 1
    
    return current
    
def draw(best,city_x,city_y,n_len,start_time, best_maping):
    result_x = [0 for col in range(n_len+1)]
    result_y = [0 for col in range(n_len+1)]
    
    for i in range(n_len):
        result_x[i] = city_x[int(best[i])]/1000
        result_y[i] = city_y[int(best[i])]/1000
    result_x[n_len] = result_x[0]
    result_y[n_len] = result_y[0]
    plt.xlim(1.24, 1.41)  # 限定横轴的范围
    plt.ylim(103.78, 103.87)  # 限定纵轴的范围
    plt.plot(result_x, result_y, marker='>', mec='r', mfc='w', label=u'Route')

    for i in range(0, n_len):
        print(i)
        print(best[i])
        print(map1[int(best[i])])
        print(result_x[i], result_y[i])
        print(best_maping[int(best[i])])

        plt.annotate(map1[best_maping[int(best[i])]], xy=(result_x[i], result_y[i]))  # xy散点坐标，xytext标注坐标，xy，xytext也可不写，只需坐标信息
    plt.legend()  # 让图例生效
    plt.margins(0)
    plt.subplots_adjust(bottom=0.15)
    plt.xlabel(u"x") #X轴标签
    plt.ylabel(u"y") #Y轴标签
    plt.title("shortestPath") #标题

    plt.savefig(save_path + start_time + ".png")  # 保存图片

    plt.show()
    plt.close(0)

def solve(form,start_time):
    # city_x,city_y = load_position(file_name)
    print(form)
    mid_cities = []
    city_x = []
    city_y = []

    for index in form.values():
        if int(index) >= 0:
            mid_cities.append(index)

            city_x.append(map[int(index)][0])
            city_y.append(map[int(index)][1])

    n_len = len(city_x)
    city_x = [x*1000 for x in city_x]
    city_y = [x*1000 for x in city_y]

    distence = init_dis_matrix(n_len)
    #得到距离矩阵
    getdistance(city_x,city_y,n_len,distence)
    #得到初始解以及初始距离
    route = random.sample(range(0, n_len), n_len) 
    total_dis = cacl_best(route,n_len,distence)
    route_real = []
    for city in route:
        route_real.append(mid_cities[city])
    print("初始路线：", route_real)
    print("初始距离：", total_dis)
    #新解
    newroute = []
    new_total_dis = 0.0
    best = route
    best_total_dis = total_dis
    t = T0
    
    while True:
        if t <= Tend:
            break
        #令温度为初始温度
        for rt2 in range(L):
            newroute = getnewroute(route, rt2,n_len)
            new_total_dis = cacl_best(newroute,n_len,distence)
            delt = new_total_dis - total_dis
            if delt <= 0:
                route = newroute
                total_dis = new_total_dis
                if best_total_dis > new_total_dis:
                    best = newroute
                    best_total_dis = new_total_dis
            elif delt > 0:
                p = math.exp(-delt / t)
                ranp = random.uniform(0, 1)
                if ranp < p:
                    route = newroute
                    total_dis = new_total_dis
        t = t * a
    
    print("现在温度为：", t)
    best_real = []
    for city in best:
        best_real.append(mid_cities[city])
    print("最佳路线：", best_real)
    print("最佳路线2：", best)
    print("最佳距离：", best_total_dis)
    best_maping = {}
    for i in range(0, len(best)):
        best_maping[best[i]] = int(best_real[i])

    print(best_maping)
    draw(best, city_x, city_y, n_len, start_time, best_maping)
    return best_real

def get_schedule(best, real_path_name,types):
    days = 0
    typesH = [6, 8, 10]

    one_day_play = typesH[int(types)]
    perday = {0: []}

    perday_consumption = 0
    index = 0
    for i in best:
        if perday_consumption + time_consumption[int(i)] <= one_day_play:  # 未超过
            perday_consumption += time_consumption[int(i)]
            # perday.append({days: real_path_name[index] + ":" + str(time_consumption[int(i)]) + "h"})
            perday[days].append(real_path_name[index] + ":" + str(time_consumption[int(i)]) + "h")
            index += 1
        else:  # 超过
            days += 1
            perday_consumption = time_consumption[int(i)]
            # perday.append({days: real_path_name[index] + ":" + str(time_consumption[int(i)]) + "h"})
            perday[days] = []
            perday[days].append(real_path_name[index] + ":" + str(time_consumption[int(i)]) + "h")
            index += 1
    return perday

def get_res(form):
    start = time.time()
    start_time = str(start).replace(".", "")
    print(start_time)
    best = solve(form, start_time)
    end = time.time()
    print('time : ', end-start)
    print(best)
    ty = form['types']
    real_path_name = []
    for i in best:
        real_path_name.append(map1[int(i)])
    perdays = get_schedule(best, real_path_name, ty)
    return real_path_name, start_time, perdays
