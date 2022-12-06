

foo = "https://idoc.jd:.@:com@/sites/SXHT"

index = foo.find("://")
protocal = foo[:index]
print protocal
tmp = foo[index+ 3:]
print tmp
index = tmp.rfind("@")
userPart = tmp[:index]
print userPart
index = userPart.find(":")
print userPart[: index]
print userPart[index + 1:]




