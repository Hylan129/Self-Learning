
while(True):
    try:
        number = int(input("请输入大于1的正整数字："))
        if number ==0|number ==1|number <0:
            print("输入数字为0或者负数，不符合要求，请重新输入")
        else:
            break
    except:
        print("输入非数字，请重新输入")
    
#层数计算

##开方，并取整
number_sqrt = int(number**0.5)

##判断奇偶
if number_sqrt%2==0:
    stored_cirles = number_sqrt/2
else:
    stored_cirles = (number_sqrt+1)/2

print("内部完整层数：%s"%str(stored_cirles))

#外层距离计算
stored_max_number = (stored_cirles *2-1)**2

yushu_side = (number - stored_max_number)%(stored_cirles * 2)

distance_side = abs(stored_cirles - yushu_side)

print("外层边距：%s"%distance_side)

#最短距离计算

the_shortest_distant_from_grid_1 = stored_cirles  + distance_side 

print("\n最短距离数：%d " % the_shortest_distant_from_grid_1)

input("Press Enter to Exit!")





    



