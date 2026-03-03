file = open("../task6_read_me.txt", "r")
content = file.read()
file.close()

num_words = len(content.split())
print(num_words)
