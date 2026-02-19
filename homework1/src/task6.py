file = open("../task6_read_me.txt", "r")
content = file.read()
print(content)

num_words = len(content.split())
print(num_words)

file.close()
