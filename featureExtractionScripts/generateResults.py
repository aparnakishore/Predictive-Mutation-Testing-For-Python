import csv
import re
import pandas as pd
import collections
import json
import ast

mutationFileName = "/Users/manasikancherla/College/CS 6888 Software Analysis/Project/working/data/calculator_diff/calculator_diff_mut.txt"
sourceFileName = "/Users/manasikancherla/College/CS 6888 Software Analysis/Project/working/data/calculator_diff/calculator_diff.py"
profilerFileName = "/Users/manasikancherla/College/CS 6888 Software Analysis/Project/working/data/calculator_diff/calculator_diff_profile.txt"
methodAssertPath = "/Users/manasikancherla/College/CS 6888 Software Analysis/Project/working/data/calculator_diff/calculator_diff_method_assert.txt"
coveragePath = "/Users/manasikancherla/College/CS 6888 Software Analysis/Project/working/data/calculator_diff/coverage.json"
complexityFileName = "/Users/manasikancherla/College/CS 6888 Software Analysis/Project/working/data/calculator_diff/calculator_diff_complexity.txt"
locFileName = "/Users/manasikancherla/College/CS 6888 Software Analysis/Project/working/data/calculator_diff/calculator_diff_LOC.txt"

file = "calculator_diff.py"

outputFile = "results/calculator_diff_finalResults.csv"

f = open(sourceFileName,'r')
lenSource = len(list(f))
f.close

def remove_items(list, item):
    result = [i for i in list if i != item]
    return result
    
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#mutation
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------


seperator = '--------------------------------------------------------------------------------\n'

mutants = {}

f = open(mutationFileName,'r')
flag = 0
countMutant = 1
#lists out mutation output lines
Lines = list(f)

operator = ""
label = ""
totalDuration = ""

#source code in the mutants

for i in range(len(Lines)):

    #For each mutant
    if Lines[i] == seperator and flag == 0:
        mutants[countMutant] = {}
        mutants[countMutant]["source"] = []
        i += 1

        while(Lines[i] != seperator):
            mutants[countMutant]["source"].append(Lines[i])
            i += 1
       
        countMutant += 1
        flag = 1
           
    elif Lines[i] == seperator and flag == 1:
        flag = 0
        
    if Lines[i] != seperator and ('[# ' in Lines[i]):
        if countMutant> 1:
            mutants[countMutant-1]["operator"] = operator
        
        newLine=Lines[i].strip('').strip(':').split(']')
        new = newLine[1].strip().split(' ')
        operator = new[0]

    
    if Lines[i] != seperator and Lines[i][0] == '[' and Lines[i][1].isdigit():
        newLine = Lines[i].strip('').split(']')
        new = newLine[1].strip('').split('by')
        label = new[0]
        mutants[countMutant-1]["label"] = label.rstrip("\n")
    
    if '[*] Mutation score' in Lines[i]:
        newLine = Lines[i].strip('').split('[')
        new = newLine[2].split(' ')
        totalDuration = new[0]
        
mutants[countMutant-1]["operator"] = operator



#extract mutant line number, mutated statement, type
for countMutant in mutants:
    changes = 0
    mutants[countMutant]["valid"] = 0
    for statement in mutants[countMutant]["source"]:
        if statement[0] == '-':
            changes += 1
    
    if changes < 2:
        mutants[countMutant]["valid"] = 1
        for statement in mutants[countMutant]["source"]:
            if statement[0] == '-':
                newLine = statement.strip('- ').split(':')
                mutants[countMutant]["mutantLineNumber"] = newLine[0].lstrip(' -')
                #mutants[countMutant]["mutatedStatement"] = newLine[1]
                
                try:
                    if newLine[2] != " ":
                        newLine[1]=newLine[1]+":"+newLine[2]
                        mutants[countMutant]["mutatedStatement"] = newLine[1].strip()
                                        
                except:
                    mutants[countMutant]["mutatedStatement"] = newLine[1].strip()
                
                new = newLine[1].strip()
                if new.startswith('return'):
                    mutants[countMutant]["type"] = 'return'
                elif new.startswith('@'):
                    mutants[countMutant]["type"] = 'decorator'
                elif 'import' in new:
                    mutants[countMutant]["type"] = 'import'
                elif new.startswith('def '):
                    mutants[countMutant]["type"] = 'method'
                elif (new.startswith('if ') or new.startswith('else ') or new.startswith('elif ')):
                    mutants[countMutant]["type"] = 'condition'
                elif (new.startswith('while ') or new.startswith('for ') or ('range' in new)):
                    mutants[countMutant]["type"] ='loop'
                elif ((' eval(') in new) or ((' eval (') in new):
                    mutants[countMutant]["type"] ='dynamic'
                else:
                    mutants[countMutant]["type"] = 'expression'
    
    if mutants[countMutant]["label"] == 'incompetent':
        mutants[countMutant]["valid"] = 0
f.close()
#source, operator, label, valid, mutantLineNumber, mutatedStatement, type, totalDuration

for countMutant in mutants:
    if mutants[countMutant]["valid"] == 1:
        mutants[countMutant]["totalDuration"] = totalDuration


#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#profiler
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

s = open(sourceFileName,'r')
p = open(profilerFileName,'r')

sourceFile = list(s)
profileFile = list(p)

s.close()
p.close()

source = {}
profile = {}

count = 1
for pline in profileFile:
    pline1 = pline.split('    ')
    pline1 = remove_items(pline1, '')
   

    if (len(pline1) == 2 and pline1[0].lstrip().rstrip().isnumeric()):
            profile[count] = {}
            profile[count]["statement"] = pline1[-1]
            profile[count]["hits"] = 0
            profile[count]["line"] = int(pline1[0].lstrip().rstrip())
            
            count += 1
        
    
    if len(pline1)>5:
        hits = pline1[1].lstrip().rstrip()
        statement = pline1[-1]
        
        if hits.isnumeric():
            profile[count] = {}
            profile[count]["statement"] = statement
            profile[count]["hits"] = int(hits)
            profile[count]["line"] = int(pline1[0].lstrip().rstrip())
            
            count += 1
        
count = 1
for line in sourceFile:
    source[count] = {}
    statement = line.lstrip().rstrip()
    source[count]["statement"] = statement
    source[count]["valid"] = 0
    source[count]["hitsList"] = []
    source[count]["hits"] = 0
    source[count]["multipleHits"] = 0
    count += 1
  


for src in source:
    statement = source[src]["statement"]
    for key,prof in profile.items():
    
        if ("if " in statement):
            new = statement.replace('(','').replace(')','')
            new2 = prof["statement"].replace('(','').replace(')','')

            if new in new2:
                source[src]["hitsList"].append(prof["hits"])
                source[src]["valid"] = 1
                
        elif statement in prof["statement"] and statement != "":
            source[src]["hitsList"].append(prof["hits"])
            source[src]["valid"] = 1
  

for src in (x for x in source if source[x]["valid"] == 1):
    
    for secondary in (y for y in source if source[y]["valid"] == 1):
        
        if (source[src]["statement"] == source[secondary]["statement"]) and (secondary<src):
            source[src]["multipleHits"] += 1
        
    index = source[src]["multipleHits"]-1
    try:
        if index == -1:
            source[src]["hits"] = source[src]["hitsList"][0]
        else:
            source[src]["hits"] = source[src]["hitsList"][-index]
    
    
    except:
        print(index)
        print(src,source[src])

    
            
for src in source:
    source[src]["lineNumber"] = src
    

#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#calculate number of asserts and number of tests
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
def mergeMAandTests(nameOfFile, methodAssertPath, coveragePath):

    numTestCovered = {}
    numTests = {}
    
    methodAssertFile = open(methodAssertPath)
    coverageFile = open(coveragePath)
    
    
    methodAssert = list(methodAssertFile)
    coverage = json.load(coverageFile)

    methodAssertFile.close()
    coverageFile.close()

    asserts = {}
    classes = {}
    clsAssert = ""

    for me in methodAssert:
        
        if me[0] != ',':
            cls = me.split('(')
            cls1 = cls[0].split('/')
            clsAssert = cls1[-1].replace('.py','')
            
        if me[0] == ',':
            line = me.split(',_, ')
            if (line[1] != ''):
                function = line[0].split('(')
                try:
                    asserts[function[0].lstrip(',').rstrip()] = int(line[-1].strip('\n'))
                    classes[function[0].lstrip(',').rstrip()] = clsAssert.lstrip().rstrip().rstrip(':')
                except:
                    pass

        
    numTestCovered[nameOfFile] = {}
    numTests[nameOfFile] = {}
    
    for num in coverage["files"][nameOfFile]["contexts"]:
        testList = coverage["files"][nameOfFile]["contexts"][num]
        numTestCovered[nameOfFile][int(num)] = 0
        numTests[nameOfFile][int(num)] = 0
        
        testList = remove_items(testList,'')
                
        if testList == []:
            numTestCovered[nameOfFile][int(num)] += 0
            
        else:
            for test in testList:
                test1 = test.split('.')
                try:
                    t = test1[-1].lstrip().rstrip()
                    cls = test1[-2].lstrip().rstrip()
                    
                except:
                    pass
                    
                if t in asserts and t != '' and cls == classes[t]:
                    numTestCovered[nameOfFile][int(num)] += asserts[t]
                    numTests[nameOfFile][int(num)] += 1
    
    for line in range(1,lenSource+1):
        if line not in numTestCovered[nameOfFile]:
            numTestCovered[nameOfFile][line] = 0
            numTests[nameOfFile][line] = 0
        
    
    return([numTestCovered[nameOfFile],numTests[nameOfFile]])

    
assertsAndTests = mergeMAandTests(file,methodAssertPath,coveragePath)
numAsserts = assertsAndTests[0]
numTests = assertsAndTests[1]

#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#McCabe complexity
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

f = open(complexityFileName,'r')
complexityLines = list(f)
f.close()

comp = 0

complexities = {}
for line in complexityLines:
    x = line.split(':')
    try:
        lineNumber = int(x[0])
        complexity = int(x[-1].split(' ')[-1])
        complexities[lineNumber] = complexity
    except:
        pass

mcCabe = {}

for line in range(1,lenSource+1):
    if line in complexities:
        comp = complexities[line]
    mcCabe[line] = comp
    
    
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#LOC
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

def getLOC(locLines):
    for line in locLines:
        if line.lstrip().startswith('LOC: '):
            return(int(line.split(':')[-1].lstrip().rstrip()))
    return(0)

f = open(locFileName,'r')
locLines = list(f)
f.close()

LOC = getLOC(locLines)

#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#Depth of nested block
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------


def depthNode(root,children):
    depth = 0
    if isinstance(root, (ast.For, ast.While)):
        depth = 1
        for child in children:
            depth += depthNode(child, ast.iter_child_nodes(child))
            
            for grandchild in ast.iter_child_nodes(child):
                depth += depthNode(grandchild, ast.iter_child_nodes(grandchild))
            
            if isinstance(child, (ast.For, ast.While)):
                depth += 1

    return depth

def max_depth(tree):
    maxdepth = 0
    for node in [n for n in ast.walk(tree)]:
        depth = depthNode(node,ast.iter_child_nodes(node))
        maxdepth = max(maxdepth, depth)
    return maxdepth

expr = open(sourceFileName,"r")
tree = ast.parse(expr.read(), mode="exec")
expr.close()


depthOfNestedBlock = max_depth(tree)

#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#generate csv file
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

output = {}

#mutants.mutantLineNumber, mutants.mutatedStatement, source.hits ,mutants.operator, mutants.type, mutants.label, mutants.totalDuration
for mutant in (x for x in mutants if mutants[x]["valid"] == 1):
    ln = int(mutants[mutant]["mutantLineNumber"])
    
    output[mutant] = [mutant, ln, mutants[mutant]["mutatedStatement"] , source[ln]["hits"],  numTests[ln] ,numAsserts[ln], mutants[mutant]["operator"], mutants[mutant]["type"], mcCabe[ln] , LOC , depthOfNestedBlock , mutants[mutant]["totalDuration"] ,mutants[mutant]["label"] ]

headers = ["Mutant Number","Line Number", "Statement", "Hits", "Number of tests", "Number of Asserts", "Operator", "Type of Statement", "Complexity" , "LOC", "DepthofNestedLoops", "Total Duration" ,"Label"]

sortedOutput = collections.OrderedDict(sorted(output.items()))

with open(outputFile, "w") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for o in sortedOutput:
        try:
            #print(o,sortedOutput[o])
            writer.writerow(sortedOutput[o])
        except:
            print(sortedOutput[o])
            print("Couldn't write")
            
f.close()
