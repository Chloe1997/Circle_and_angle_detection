import numpy as np
import math
import label1020
import matplotlib.image as mpimg # mpimg 用於讀取圖片
import matplotlib.pyplot as plt # plt 用於顯示圖片


#image_org = mpimg.imread('C:/Users/user/Desktop/test/circle.jpg')
image_org = mpimg.imread('C:/Users/user/Desktop/test/clp5.jpg')
#image_org = mpimg.imread('C:/Users/user/Desktop/test/image1.jpg')

#print(image_org.shape)
F = open('boundary.txt',mode='w')
B = open('boundary_show.txt',mode='w')

def neighbor(label,row,column,mode=4):
    if mode == 4 :
        neighbor_array = [label[row,column-1],label[row-1,column],label[row,column+1],label[row+1,column]]
    elif mode == 8:
        neighbor_array = [label[row-1,column-1],label[row-1,column],label[row-1,column+1],label[row,column-1],
                          label[row,column+1],label[row+1,column-1],label[row+1,column],label[row+1,column+1]]
    return neighbor_array

# labeling
label,image,num_obj = label1020.labeling(image_org)
#print(num_obj)
size = label.shape
m = size[0] #rows
n = size[1] #columns
#print(num_obj)
num = np.zeros(num_obj)

# calculate object perimeter
for row in range(m):
    for column in range(n):
        if label[row,column] != 0 :
            if row != 0 and row != m-1 and column != 0 and column != n-1 :
                for x in range(num_obj):
                    if label[row,column] == x+ 1 :
                        neighbor_array = neighbor(label,row,column,mode=8)
                        if min(neighbor_array) !=0 :
                            #label[row,column] = 0
                            F.write(str(int(label[row,column])))
                        elif min(neighbor_array) == 0 : #只有符合才是邊緣
                            F.write(str(int(label[row,column])))
                            num[x] = num[x] +1
        F.write(str(int(label[row,column])))
    F.write('\n')

# object perimeter == num

# calculate object area
area = np.zeros(num_obj)

for row in range(m):
    for column in range(n):
        if label[row,column] != 0 :
            for x in range(num_obj):
                if label[row,column] == x+1 :
                    area[x] = area[x] +1

#print(area)
Boundary = np.ones([m,n])

circle = 0
track = np.zeros(num_obj)

for id in range(num_obj):
    perimeter = num[id]
    obj_area = area[id]
    #print(area[id])
    #print(perimeter,area)
    if perimeter!=0 and obj_area!=0 :
        cal = math.pow(perimeter,2)/obj_area
        test = cal/(4* math.pi)
        #print(test)
        if 0.6<=test<=1.6 :
            #print(id+1)
            track[id] = id+1
            circle = circle+1
            #print(id)
print('Number of Circle : ',circle)
#print(track)

# mark the label of circle
k=0
track_circle = np.zeros(circle)
track_area = np.zeros(circle)
for id in range(num_obj) :
        if track[id] != 0 :
            track_circle[k] = track[id]
            track_area [k] = area[id]
            k = k + 1
            #print(track[id])

#print(track_circle,track_area)

# Geometry center
x_tot = np.zeros(circle)
y_tot = np.zeros(circle)
for row in range(m):
    for column in range(n):
        for c in range(circle):
            if label[row,column] == track_circle[c] :
                x_tot[c] = x_tot[c] + (row+1)*1
                y_tot[c] = y_tot[c] + (column+1)*1
x_mean = np.zeros(circle)
y_mean = np.zeros(circle)
for c in range(circle):
    # x_mean[c] = int(x_tot[c]/track_area[c])
    # y_mean[c] = int(y_tot[c]/track_area[c])
    x_mean[c] = round(x_tot[c]/track_area[c])
    y_mean[c] = round(y_tot[c]/track_area[c])
#print(x_mean,y_mean)

# tilt angle
angle = 0
for n in range(circle) :
    line = abs(x_mean[n]-x_mean[n-1])/abs(y_mean[n]-y_mean[n-1])
    # print(math.atan(line)* (180 / math.pi))
    angle = math.atan(line)/circle + angle

print("tilt angle :",angle* (180 / math.pi))

# show the boundary
for row in range(m):
    for column in range(n):
        Boundary[row,column] = label[row,column]
        if Boundary[row,column] != 0 :
            if row != 0 and row != m-1 and column != 0 and column != n-1 :
                for x in range(num_obj):
                    neighbor_array = neighbor(label, row, column, mode=4)
                    if min(neighbor_array) == 0:
                        Boundary[row, column] = label[row,column] + num_obj
                        B.write(str(int(Boundary[row, column])))
        if Boundary[row,column] <= num_obj :
            Boundary[row,column] = 0
            B.write(str(int(Boundary[row, column])))
    B.write('\n')

# plt.figure(figsize=(30,10))
# plt.imshow(Boundary)
# plt.axis('off') # 不顯示座標軸
# plt.show()





