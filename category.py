#coding:gbk

file = open("d:\\experiment\\floor_category.txt")
result = list()
for line in file.readlines():
    # print(line)
    result.append(line)
#print(result)

ends = list();
file2 = open("d:\\experiment\\floor_text.txt")
for line in file2.readlines():
    print(line)
    # ends.append(line.replace("www.jd.com", "-"))
print(ends)


