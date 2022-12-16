# -*- coding:utf-8 -*-

pins = ""
with open("C:\\Users\\yangpan3\\Desktop\\append.txt") as f:
    for line in f:
        if len(line.strip()) == 0:
            continue

        pins += "'" + line.strip() + "',"

print(pins[0: len(pins) - 1])

