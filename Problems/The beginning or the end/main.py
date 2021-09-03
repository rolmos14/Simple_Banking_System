sentence = input()
old_first = sentence.find("old")
old_last = sentence.rfind("old", old_first)
print(max(old_first, old_last))
