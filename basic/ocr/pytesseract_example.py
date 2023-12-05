import pytesseract

content = pytesseract.image_to_string("Snipaste_2023-11-30_11-42-45.png", "chi_sim")

# 输出： 使用 lang-'chi_sim+eng
print(content)
