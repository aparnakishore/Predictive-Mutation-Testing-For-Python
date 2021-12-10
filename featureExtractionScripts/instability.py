import os

Ca = {}
Ce = {}
instability = {}

listOfFiles = []



filepath = '/Users/manasikancherla/College/CS 6888 Software Analysis/Project/working/data/automated-testing'

for file in os.listdir(filepath):
    if '.py' in file:
        Ca[file.replace('.py','')] = 0
        Ce[file.replace('.py','')] = 0
        listOfFiles.append(file)

"""
Calculating Ca
Number of modules outside the module that depend on classes inside the module
"""


#Listing out classes in module
for file in listOfFiles:
    f = open(filepath+'/'+file,"r")
    
    for line in f:
        if line.startswith('import ') and ('as ' in line):
            imported = line[:line.index(' as')].strip('\n').replace('import','')
            if imported in Ca:
                Ca[imported] += 1
        
        elif line.startswith('import ') and ('as ' not in line):
            imported = line.strip('\n').replace('import ','')
            if imported in Ca:
                Ca[imported] += 1
        
        elif line.startswith('from '):
            imported = line[:line.rindex(' import')].strip('\n').replace('from ','')
            if '.' in imported:
                imported = imported[::-1]
                imported = imported[:imported.index('.')]
                imported = imported[::-1]
            if imported in Ca:
                Ca[imported] += 1
                        
    f.close()

print("Ca values: ")
for key,value in Ca.items():
    print(key+' '+str(value))

"""
Calculating Ce
Number of modules inside the module that depend on classes outside the module
"""

for file in listOfFiles:
    f = open(filepath+'/'+file,"r")
    imported = file.replace('.py','')
    
    for line in f:
        if 'import ' in line:
            Ce[imported] += 1
            
print("Ce values: ")
for key,value in Ce.items():
    print(key+' '+str(value))
    

"""
Calculating Instability
Ce/(Ce+Ca)
"""

for file in listOfFiles:
    
    if (Ce[file.replace('.py','')]+Ca[file.replace('.py','')]) != 0:
        instability[file.replace('.py','')] = Ce[file.replace('.py','')]/(Ce[file.replace('.py','')]+Ca[file.replace('.py','')])
    else:
        instability[file.replace('.py','')] = 0

print("Instability values: ")
for key,value in instability.items():
    print(key+' '+str(value))
    
