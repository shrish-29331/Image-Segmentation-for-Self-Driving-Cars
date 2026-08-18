import subprocess
import sys, os, math
from difflib import SequenceMatcher


def python_analyser(code):
    
    with open("test.py", "w") as file:
        file.write(code)
        
        
    cmd = "pylint test.py"  # Replace "your_command_here" with your actual command
    
    # Run the command
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Capture the output
    stdout, stderr = process.communicate()

    s = stdout.decode()
    print("#########################################")
    print(s)
   
    index1 = s.find("(pre")

    

    return [s,2.5*float(s[index1-8:index1- 4])]

def upd_code(code_inp):

    source_lines = []
    code_block = False

    lines1 = code_inp.splitlines()

    for source_line in lines1:
      if '/*' in source_line:
        code_block = True
        continue
      if '*/' in source_line:
        code_block = False
        continue
      if not code_block:
        source_lines.append(source_line.split('//')[0].strip()) # if not in code block, insert line with comments removed

    return source_lines

# com+=(source_lines)



def check_commenting(code_inp):

    source_lines = code_inp.splitlines()

    # setup
    lines = 1
    codes = 0
    comments = 0
    in_block = False
    
    com=""

    # read line-by-line
    for line in source_lines:
      lines += 1

      # count block comments
      if '/*' in line:
        in_block = True # open block

      if '*/' in line:
        in_block = False
        comments += 1 # blocks count as one

      # count standard comments
      if '//' in line and not in_block:
        comments += 1 # can have comment, whether on code line or not, but not in block

      # count code lines
      if not in_block and line.strip().find('//') != 0 and not line.strip() == '':
        codes += 1 # count line as code if not in block code or starting with commment

    # com+= final report
    # com+=("Total Lines: " + str(lines))
    # com+=("Code Lines: " + str(codes))
    # com+=("Comments: " + str(comments))
        
    com+=("Total Lines: " + str(lines) + "\n")
    com+=("Code Lines: " + str(codes) + "\n")
    com+=("Comments: " + str(comments) + "\n")

    ratio = comments*100/codes

    if ratio < 6:
      feedback = "There are very few to no comments present; you should comment your code more thoroughly"
      score = 25
    elif ratio < 12:
      feedback = "There are a few comments, but you should comment your code more completely for full credit"
      score = 50
    elif ratio < 18:
      feedback = "There are some comments, but you should comment your code more completely for full credit"
      score = 75
    elif ratio < 50:
      feedback = "There are a reasonable number of comments"
      score = 100
    else:
      feedback = "Best practice is around 30% comments, so this is a bit more heavily commented than necessary. Comments can start to impede readability at a certain level."
      score = 75

    # com+=("")
    score=(score/100)*5
    com+=("Comment-to-Code Ratio: " + str(ratio) + "%" + "\n")
    com+=("Feedback: " + feedback + "\n")
    com+=("Commenting score: "+str(score)+"/5"+"\n")
    com+="\n"
    
    return [com,score]
    # com+=("Comment-to-Code Ratio: " + str(ratio) + "%")
    # com+=("Feedback: " + feedback)
    # com+=(score)


def check_expressions(code_inp):
    
    com=""


    source_lines=upd_code(code_inp)
    # GLOBALS
    # Weights of each type of error
    WEIGHT_LEN = 0.6 # weight of long expressions

    # Thresholds for line length counted as complex expression
    LEN_THRESH = 50 # line character length threshold in order to be considered as a long expression
    # Step 2: Count operators and long expressions
    compounds = 0
    constructs = 0
    long_lines = 0
    for line in source_lines:
      # Count compound operations on the line
      compounds += line.count('&&')
      compounds += line.count('||')
      # Count if line is a for, while, if construct
      if 'else if' in line or 'else' in line or 'while' in line or 'for' in line:
        constructs += 1
        compounds += 1 # add 1 compound for the statement itself (e.g. if (this || that) should count both sides)
        # if line was a construct, check if it was a lengthy expression
        if len(line) > LEN_THRESH:
          long_lines += 1

    # Step 3: com+= final report
    com+=("Total Conditional Constructs: " + str(constructs) + "\n")
    com+=("Total Compound Expressions: " + str(compounds) + "\n")
    com+=("Total Lengthy Constructs: " + str(long_lines) + "\n")
    if compounds!=0 and constructs!=0:
        
        constructs_to_compounds_ratio = constructs/float(compounds) # constructs per compound, ideally 1-to-1, but gets smaller as expression complexity goes up (e.g. 2 compound per "if" would be 0.5 and 3 about 0.3)
    
        long_lines_to_constructs_ratio = (WEIGHT_LEN*long_lines)/float(constructs) # number of constructs that are over length threshold, scaled by cost of long expressions

        ratio = 100 * (.5*long_lines_to_constructs_ratio + .5*(1 - constructs_to_compounds_ratio)) # Final rating
    
        if ratio < 15:
          feedback = "There may be some complex or long expressions, but likely not enough to impact readability or suggest a need for better code design"
          score = 100
        elif ratio < 30:
          feedback = "There are some unnecessary complex or long expressions; readability may be impeded and there may be a need for better code design to reduce complexity"
          score = 75
        elif ratio < 50:
          feedback = "There are many unnecessary complex or long expressions; readability is likely impaired and there is probably better code design to reduce complexity"
          score = 50
        else:
          feedback = "There are too many unnecessary complex or long expressions; readability will be impaired and there should be better code design to reduce complexity"
          score = 25
    
        # com+=("")
        score=score/20
        com+=("Complex Expression Rate: {0:.2f}%".format(ratio)+"\n")
        com+=("Feedback: " + feedback + "\n")
        
    else:
        score=5
        
    com+=("Expressions score: "+str(score)+"/5"+"\n")
    com+="\n"
    
    return [com,score]


def list_to_ranged_string(l):
    # build up string, combining consecutive line ranges
    result = ''
    prev_e = -1 # start is line -1, which will never happen since starts at 1
    in_range = False
    for e in l: # go through all line numbers in the list
        if e != prev_e + 1: # if not continuing in range
            if in_range: # must handle com+=ing previous range
                result += "-" + str(prev_e)
                in_range = False
            if prev_e == -1:  # then com+= current line number, only with comma when not on first one (-1 for prev_e)
                result += str(e)
            else:
                result += ", " + str(e)
        else: # else, continuing a range
            in_range = True
        prev_e = e
    if in_range:
        result += "-" + str(prev_e) # must com+= last one if finished list in a range
    return result


def check_indentation(code_inp):
    
    com=""


    WEIGHT_WRONG = 1 # each line with fully wrong indentation has weight of 1
    WEIGHT_PARTLY = 0.8 # each line of slightly wrong indentation only has weight of 0.8
    WEIGHT_TABSPACE = 0.4 # each line of mixed tab space only has weight of 0.3

    # Attempt to lessen impact of large blocks that are wrongly indented?
    BLOCK_LEVEL = True # true makes lines be weighted slightly by blocks (lowers penalty for wrong level in one region, using function specified in BLOCK_ADJUST)
    # Adjustment function for blocks, return new weight between 0 and 1; fewer blocks with more lines would be slightly less weight than many lines spread over many blocks
    BLOCK_ADJUST = lambda lines,blocks: 1.0 if lines == 0 else math.log(blocks/float(lines))/math.log(1000) + 1 # This is a log base 1000 function that slowly reduces cost of block-level errors

    # When calculating final result for many files, weight file by number lines or just average?
    FILE_WEIGHT = True # files will be weighted by number of lines; turn to False to just take raw average

    file_lines = []
    file_ratios = []

    # Step 1: First read-through to get all levels seen
    # setup
    indents = 0
    indents_probs = {}

    # read line-by-line
    # with open(sys.argv[f]) as source:
    for line in code_inp:
        # get line indentation
        indentation = line[:len(line)-len(line.lstrip())] # read from beginning until start of stripped string
        if '\n' not in indentation:
            if line.strip().find('}') == 0:
                indents -= 1
            if indents not in indents_probs:
                indents_probs[indents] = [indentation]
            else:
                indents_probs[indents].append(indentation)
            if '{' in line:
                indents += 1
            if '}' in line and not line.strip().find('}') == 0:
                indents -= 1

    # Step 2: Pick most likely for each level based on frequency
    # setup
    indents_final = {}

    for k,v in indents_probs.items():
        indents_final[k] =  max(set(v), key=v.count)

    # Step 3: Read line-by-line again and match against expectations
    # setup
    indents = 0
    current_line = 1 # line number counting starts at 1
    mixed_tabs_spaces_lines = []
    partly_wrong_lines = []
    wrong_lines = []

    # read line-by-line
    for line in code_inp:
        # get line indentation
        indentation = line[:len(line)-len(line.lstrip())] # read from beginning until start of stripped string
        if '\n' not in indentation: # must have been a newline if \n present after stripping, ignore

            # check for decrease indentation, only if non-code line with bracket is current line affected
            if line.strip().find('}') == 0: # decrease
                indents -= 1

            # check indentation against expectations and place error type
            if ('\t' in indentation and ' ' in indents_final[indents]) or (' ' in indentation and '\t' in indents_final[indents]):
                mixed_tabs_spaces_lines.append(current_line) # mixed tabs and spaces
            elif indentation != indents_final[indents]: # some other error
                for k,v in indents_final.items():
                    if indentation == v and k != indents and current_line not in wrong_lines:
                        wrong_lines.append(current_line) # fully wrong, at a different indent level
                if current_line not in wrong_lines: # most have only been partly wrong if didn't match any other level
                    partly_wrong_lines.append(current_line)

            # check for indentation changes, '{' always affects next line and '}' affects next line if with code this line
            if '{' in line: # increase
                indents += 1
            if '}' in line and not line.strip().find('}') == 0: # decrease
                indents -= 1

        # always increment line counter
        current_line += 1

    # com+= report for current file
    total_lines = current_line # last line read is total line number
    total_mixed_tabs_spaces_lines = len(mixed_tabs_spaces_lines)
    total_partly_wrong_lines = len(partly_wrong_lines)
    total_wrong_lines = len(wrong_lines)

    string_mixed_tabs_spaces_lines = list_to_ranged_string(mixed_tabs_spaces_lines)
    string_partly_wrong_lines = list_to_ranged_string(partly_wrong_lines)
    string_wrong_lines = list_to_ranged_string(wrong_lines)

    blocks_mixed_tabs_spaces_lines = 0 if string_mixed_tabs_spaces_lines == '' else len(string_mixed_tabs_spaces_lines.split(','))
    blocks_partly_wrong_lines = 0 if string_partly_wrong_lines == '' else len(string_partly_wrong_lines.split(','))
    blocks_wrong_lines = 0 if string_wrong_lines == '' else len(string_wrong_lines.split(','))

    ratio_raw = (total_mixed_tabs_spaces_lines + total_partly_wrong_lines + total_wrong_lines) / float(total_lines)
    ratio_weighted = (WEIGHT_TABSPACE*total_mixed_tabs_spaces_lines
        + WEIGHT_PARTLY*total_partly_wrong_lines
        + WEIGHT_WRONG*total_wrong_lines) / float(total_lines)
    ratio_adjusted = (WEIGHT_TABSPACE*BLOCK_ADJUST(total_mixed_tabs_spaces_lines,blocks_mixed_tabs_spaces_lines)*total_mixed_tabs_spaces_lines
        + WEIGHT_PARTLY*BLOCK_ADJUST(total_partly_wrong_lines,blocks_partly_wrong_lines)*total_partly_wrong_lines
        + WEIGHT_WRONG*BLOCK_ADJUST(total_wrong_lines,blocks_wrong_lines)*total_wrong_lines) / float(total_lines)

    # com+=("="*len(sys.argv[f]))
    # com+=(sys.argv[f].upper())
    # com+=("="*len(sys.argv[f]))
    com+=("Total Lines: " + str(total_lines)+"\n")
    com+=("Total As Expected: " + str(total_lines - total_mixed_tabs_spaces_lines - total_partly_wrong_lines - total_wrong_lines)+"\n")
    com+=("Total Unexpected: " + str(total_mixed_tabs_spaces_lines + total_partly_wrong_lines + total_wrong_lines)+"\n")

    com+=("\nMixed Tabs/Spaces: " + str(total_mixed_tabs_spaces_lines) + " lines over " + str(blocks_mixed_tabs_spaces_lines) + " blocks"+"\n")
    com+=("On Line Numbers: " + string_mixed_tabs_spaces_lines+"\n")

    com+=("\nIndentation Partly Wrong: " + str(total_partly_wrong_lines) + " lines over " + str(blocks_partly_wrong_lines) + " blocks"+"\n")
    com+=("On Line Numbers: " + string_partly_wrong_lines+"\n")

    com+=("\nIndentation at Wrong Level: " + str(total_wrong_lines) + " lines over " + str(blocks_wrong_lines) + " blocks"+"\n")
    com+=("On Line Numbers: " + string_wrong_lines+"\n")

    com+=("\nRatios (lower is preferred):"+"\n")
    com+=("Raw: {0:.2f}%".format(ratio_raw*100)+"\n")
    com+=("Weighted: {0:.2f}%".format(ratio_weighted*100)+"\n")
    com+=("Adjusted: {0:.2f}%".format(ratio_adjusted*100)+"\n")
    # com+=("")

    file_lines.append(total_lines)
    if BLOCK_LEVEL:
        file_ratios.append(ratio_adjusted)
    else:
        file_ratios.append(ratio_weighted)

    # Final report
    if FILE_WEIGHT:
        final_ratio = sum([x/float(sum(file_lines)) * y for x,y in zip(file_lines,file_ratios)])
    else:
        final_ratio = sum(file_ratios)/float(len(file_ratios))

    final_ratio = final_ratio * 100; # scale by 100 to get percentage from decimal score

    if final_ratio < 8:
        feedback = "There may be a few minor indentation errors (see notes above) but no major issues."
        score = 100
    elif final_ratio < 20:
        feedback = "There were a few major or several minor indentation errors (see notes above)"
        score = 75
    elif final_ratio < 35:
        feedback = "There were several major indentation errors (see notes above)"
        score = 50
    else:
        feedback = "There were many major indentation errors (see notes above)"
        score = 25

    score/=20

    # com+=("==================================")
    com+=("Overall Improper Indentation Rate: {0:.2f}%".format(final_ratio)+"\n")
    com+=("Feedback: " + feedback+"\n")
    com+=("Indentation score: "+str(score)+"/5"+"\n")
    com+="\n"

    return [com,score]


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def parse_line(x):
	  return x.split('//')[0].strip() # remove comments and whitespace


def check_repetition(code_inp):
    
    com=""

    WEIGHT_DUP = 0.8 # exact duplicate lines weighting
    WEIGHT_SIM = 0.65 # similar lines weighting

    # Thresholds for similarity and line length
    SIM_THRESH = 0.9 # similarity threshold
    LEN_THRESH = 22 # line character length threshold in order to be considered as candidate

    source_lines=upd_code(code_inp)

    content = [parse_line(x) for x in source_lines if x.strip() != '' and len(parse_line(x)) > LEN_THRESH] # remove whitespace and comments for checking and sorting, no blank lines
    lines = len(content) # count original, non-new lines
    lines=max(lines,1)

    uniques = set(content)
    remainder = list(uniques) # get only uniques
    duplicates = lines - len(remainder) # count duplicates

    remainder.sort() # sort list of remainder


    # Step 2: Using difflib, determine how many in the remainder are similar above a threshold
    similar = 0
    i = 0
    j = 0
    while i < len(remainder) and j < len(remainder)-1:
      j += 1 # increment j at start
      if similarity(remainder[i],remainder[j]) > SIM_THRESH and len(remainder[i]) > 30: # 90% similar for long-ish lines of code
        similar += 1
        i -= 1 # keep i at start of group while j steps through to find end to similarities
      else:
        i = j - 1 # move i forward to end of current similarity group
      i += 1 # increment i at end


    # Step 3: com+= final report
    com+=("Total Candidate Lines (length threshold of " + str(LEN_THRESH) + "): " + str(lines)+"\n")
    com+=("Lines Fully Duplicated: " + str(duplicates)+"\n")
    com+=("Lines Over Similarity Threshold of " + str(SIM_THRESH*100) + "%: " + str(similar)+"\n")

    ratio = 100 * (WEIGHT_DUP*duplicates + WEIGHT_SIM*similar) / float(lines) # Final ratio

    if ratio < 20:
      feedback = "There is very little repetition in your code"
      score = 100
    elif ratio < 40:
      feedback = "There is some repetition in your code; consider simplifying logic or moving some common operations into their own functions"
      score = 75
    elif ratio < 65:
      feedback = "There is a fair amount of repetition in your code; simplify logic or move common operations into their own functions"
      score = 50
    else:
      feedback = "There is a lot of repetition in your code; simplify logic or move common operations into their own functions"
      score = 25

    score/=20
    com+=("Reptition Rate: {0:.2f}%".format(ratio)+"\n")
    com+=("Feedback: " + feedback+"\n")
    com+=("Non-Reptition score: "+str(score)+"/5"+"\n")
    com+="\n"
    
    return [com,score]

def check_variables(code_inp):

    com=""
    # GLOBALS
    # Weights of each type of error
    WEIGHT_SHORT = 1 # short var names
    WEIGHT_SCOPE = 0.5 # for loop counters not tightly scoped

    # Thresholds
    THRESH_SHORT = 3 # minimum number of permitted characters before considered short



    source_lines = upd_code(code_inp)

    # Step 2: Count short variable names and look at loop scoping
    var_names = 0
    var_names_short = 0
    for_loops = 0
    for_loops_scoped = 0
    for line in source_lines:
      # Check variable naming
      temp = line.split(' ')
      if len(temp) > 1:
        if temp[0] == 'int' or temp[0] == 'double' or temp[0] == 'float' or temp[0] == 'bool' or temp[0] == 'char' or temp[0] == 'string':
          var_names += 1
          if len(temp[1]) < THRESH_SHORT:
            var_names_short += 1
      # Check scoping on loops
      if 'for' in line:
        for_loops += 1
        if 'int' in line or 'auto' in line or 'decltype' in line:
          for_loops_scoped += 1

    # Step 3: com+= final report
    com+=("Total Short Variable Names: " + str(var_names_short) + " out of " + str(var_names) + " considered"+"\n")
    com+=("Total Scoping Issues: " + str(for_loops - for_loops_scoped) + " out of " + str(for_loops) + " considered"+"\n")
    
    for_loops=max(1,for_loops)
    var_names=max(1,var_names)

    ratio = 100 * (.5*(WEIGHT_SCOPE*(for_loops-for_loops_scoped))/float(for_loops) + .5*(WEIGHT_SHORT*var_names_short)/float(var_names))

    if ratio < 15:
      feedback = "A few variable names may be short and minor scoping issues my be present but not enough to cause concern"
      score = 100
    elif ratio < 30:
      feedback = "Several variable naming or scoping issues are present; remember to use meaningful names and scope variables tightly"
      score = 75
    elif ratio < 50:
      feedback = "Multiple variable naming or scoping issues are present; make sure to use meaningful names and scope variables tightly"
      score = 50
    else:
      feedback = "Many variable naming or scoping issues are present; you should use meaningful names and scope variables tightly"
      score = 25

    score/=20
    com+=("Variable Naming or Scoping Issue Level: {0:.2f}%".format(ratio)+"\n")
    com+=("Feedback: " + feedback+"\n")
    com+=("Variable score: "+str(score)+"/5"+"\n")
    
    return [com,score]
    

def run_cpp_with_input(cpp_file, input_text):
    # Compile the C++ code
    compilation_process = subprocess.run(['g++', cpp_file, '-o', 'program'], capture_output=True, text=True)
    
    # Check if compilation was successful
    if compilation_process.returncode != 0:
        print("Compilation failed:")
        print(compilation_process.stderr)
        return
    
    # Run the compiled program with input text
    execution_process = subprocess.run(['./program'], input=input_text, capture_output=True, text=True)
    
    # Check if execution was successful
    if execution_process.returncode != 0:
        print("Execution failed:")
        print(execution_process.stderr)
        return
    
    # Return the output of the program
    return execution_process.stdout

def run_python_with_input(py_file, input_text):

    # Run the Python script with input text
    execution_process = subprocess.run(['python', py_file], input=input_text, capture_output=True, text=True)
    
    # Check if execution was successful
    if execution_process.returncode != 0:
        print("Execution failed:")
        print(execution_process.stderr)
        print("faaaaail")
        return
    
    # Return the output of the program
    return execution_process.stdout

def run_c_with_input(c_file, input_text):
    # Compile the C code
    compilation_process = subprocess.run(['gcc', c_file, '-o', 'program'], capture_output=True, text=True)
    
    # Check if compilation was successful
    if compilation_process.returncode != 0:
        print("Compilation failed:")
        print(compilation_process.stderr)
        return

    # Run the compiled program with input text
    execution_process = subprocess.run(['./program'], input=input_text, capture_output=True, text=True)
    
    # Check if execution was successful
    if execution_process.returncode != 0:
        print("Execution failed:")
        print(execution_process.stderr)
        return
    
    # Return the output of the program
    return execution_process.stdout

def convert_to_file(code_string, filename='code'):
    # Determine the file extension based on the code content
    file_extension = '.py'
    fe=0
    cpp_keywords = ['namespace', 'iostream', 'cin', 'cout']
    for keyword in cpp_keywords:
        if keyword in code_string:
            file_extension = '.cpp'
            fe=1
            
    c_keywords = ['stdio.h', 'stdlib.h', 'printf', 'scanf']
    for keyword in c_keywords:
        if keyword in code_string:
            file_extension = '.c'
            fe=2
            
    with open(filename + file_extension, 'w') as code_file:
        code_file.write(code_string)
        
    return fe

def tc_checker(l,l1,l2):
    fe=convert_to_file(l, filename='code')
    # print(fe)
    # print(1111111111111111111111111111111111111111111111111)
    passed=0
    com=[]
    tot_score=0
    
    if(fe!=0):
        
        com.append([check_commenting(l)[0]])
        tot_score+=check_commenting(l)[1]
        com.append([check_expressions(l)[0]])
        tot_score+=check_expressions(l)[1]
        com.append([check_repetition(l)[0]])
        tot_score+=check_repetition(l)[1]
        com.append([check_indentation(l)[0]])
        tot_score+=check_indentation(l)[1]
        com.append([check_variables(l)[0]])  
        tot_score+=check_variables(l)[1] 
        
    else:
        
        com.append([python_analyser(l)[0]])
        tot_score+=python_analyser(l)[1]
        
    for x in range(len(l1)):
        if(fe==0):
            out=run_python_with_input('code.py',l1[x])
            # print(out,"1111111111111111111111111111111111111111111111111111111111111")
        elif(fe==1):
            out=run_cpp_with_input('code.cpp',l1[x]) 
        else:
            # print("222222222222222222222222222222222",type(fe))
            out=run_c_with_input('code.c',l1[x])
            
        if(out.strip()==l2[x]):
            passed=passed+1
    tot_score+=(passed/len(l1))*75
    return ["{} out of {} test cases passed".format(passed, len(l1)),com,tot_score]

