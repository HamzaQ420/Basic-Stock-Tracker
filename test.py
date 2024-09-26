lst = ["Hamza:B,100"]
print(lst)
tempList = []; info = []
for x in lst:
    tempList = x.split(":")
    tempList.append((tempList[1].split(","))[0])
    tempList.append(tempList[1][tempList[1].index(","):].replace(",", ""))
    tempList.pop(1)

print(tempList)
