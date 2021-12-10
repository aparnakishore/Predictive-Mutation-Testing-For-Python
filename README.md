# Predictive-Mutation-Testing-For-Python

1. Use feature extraction scripts in feature Extraction to input txt and json file paths of your tool outputs to generate CSV file
2. Perform data cleansing on consolidated CSV files
3. Run classification learning model to generate predicted outputs.

Detailed Implementation:

Create a seperate conda environment or venv to install dependencies of source projects used to avoid conflicting dependencies among projects.
 
1. Coverage:
Copy .coveragerc file in preceeding directory (common for all projects)
In source directory run: 
    coverage run -m --rcfile=../.coveragerc pytest 
    coverage report -m --rcfile=../.coveragerc 
    coverage json --rcfile=../.coveragerc 
Output is stored in coverage.json

2. Line Profiler:
Create a new file called <nameOfSourceFile_profiler>.py
Add the line: from line_profiler import LineProfiler
Include all import statements from the source file and corresponding test file to <nameOfSourceFile_profiler>.py
Copy all source code from the source file and include the @profile decorator infront of each defined function in the source code
Copy all test methods from corresponding test file at the end.
In source directory run:
    kernprof -l -v pytest <nameOfSourceFile_profiler>.py

3. Mutation:
Only runs on Ubuntu/ other Linux platforms. Returns erroneous output on MacOS
mut.py --target <source_file>.py --unit-test <path_to_test_file/test_file_name>.py -m --runner pytest


6. Generate Results:
Give specified filePaths for all required files described in featureExtractionScripts/generateResults.py and run
    python3 generateResults.py

4. methodAssert:
Specify file path for corresponding test file in featureExtractionScripts/methodAsserts.py and run
    python3 methodAssert.py

5. classAssert:
Specify file path test file and source file in featureExtractionScripts/classAsserts.py and run
    python3 classAssert.py

5. Ca, Ce, Instability:
Specify source directory path in featureExtractionScripts/instability.py and run
    python3 instability.py
    
6. Run the classification model script

