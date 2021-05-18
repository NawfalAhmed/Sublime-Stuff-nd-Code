from random import seed
from random import randint as rand

data = [rand(0, 600) for i in range(200)]

data2 = [num for num in data if num not in data2 and len(data2) != 100]
data = data2
data = " ".join(map(str, data))
print(data)
filee = open("theseldata.txt", "w+")
filee.write(data)
filee.close()
# from bisect import bisect_left
# data1 = open("CreateTest-input.txt","r");
# data = data1.read().split()
# data = [int(x) for x in data]
# print(data[1:20])
# seed(1)
# def bifind(a, x):
#     i = bisect_left(a, x)
#     return i if i != len(a) and a[i] == x else -1

# for i in range(4000):
# 	val = bifind(data,rand(1,9500))
# 	if val != -1:
# 		del data[val];

# data = [str(x) for x in data]
# print(data[:120])
# data1.close()
# mystr = " "
# filee = open("thedata.txt","w+")
# filee.write(mystr.join(data))
# filee.close()
