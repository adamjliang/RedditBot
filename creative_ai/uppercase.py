ifstream = open('allHeadlines.txt')
lines = ifstream.readlines()
ifstream.close()
i = 0
for line in lines:
    print(line.capitalize())
