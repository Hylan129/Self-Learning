
while(True):
    try:
        number = int(input("请输入大于0的正整数字："))
        if number ==0|number <0:
            print("输入数字为0或者负数，不符合要求，请重新输入")
        else:
            break
    except:
        print("输入非数字，请重新输入")
    
arr = []
while(True):
    if number%2==0:
        number=number/2
        arr.append(2)
    elif (number%2==1) & (number==1):
        break
    elif number !=1:
        while(True):
            if number%3 ==0:
                number=number/3
                arr.append(3)
            elif (number%3==1) & (number==1):
                break
            elif number !=1:
                while(True):
                    if number%5 ==0:
                        number=number/5
                        arr.append(5)
                    elif (abs(number%5)==1) & (abs(number)==1):
                        break
                    else:
                        arr =[]
                        break
                break
        break
    
                
if arr ==[]:
    print("您输入的数字为非Simple Number,%s" % arr)
else:
    print("\n您输入的数字为Simple Number,%s " % arr)

input("Press Enter to Exit!")
