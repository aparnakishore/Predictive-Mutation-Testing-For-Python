import os

path = os.path.abspath(".")
output = open("methodAssert/templite_methodAssert.txt", "w")

def isclass(line):
    return "class" in line and ":" in line and ".class" not in line
	
def ismethod(line):
    return "def " in line 
    
def analysis(file):
    input = open(file)
    currentclass = ''
    currentmethod = ''
    count = 0
    totalCount = 0
    output.write(file + "\n")
    for line in input:
        if(isclass(line)):
            line = line.split(" ")
            try:
                index = line.index("class")
            except:
                continue
			
            if currentclass != '' and currentmethod != '':
                output.write(currentclass + "," + currentmethod + ",_, " + str(count) + '\n')
            currentclass = line[index+1]
            currentmethod = ''
            count = 0
            continue
            
        elif(ismethod(line)):
            end = line.rfind(")") + 1
            middle = line.find("(")
            start = line.rfind(" ", 0, middle) + 1
            if currentclass != '' or currentmethod != '':
                output.write(currentclass + "," + currentmethod + ",_, " + str(count) + '\n')
            currentmethod = line[start:end]
            count = 0
            continue
        count += line.count("assert")

    if currentclass != '' or currentmethod != '':
        output.write(currentclass + "," + currentmethod + ",_, " + str(count) + '\n')

analysis("../test/test_templite.py")
		
output.close()