#copy+paste the CSV data into the line below
#(you can just double-click the keyword and then Ctrl+V to ensure it's done correctly)
csv_data = '''PASTE_HERE'''

import re

def check_valid(calc, datestr):
	#we gave to check digits before substituting in the freebie power/root operators
	digits_used = ''.join(filter(str.isdigit,calc))
	if datestr != digits_used:
		return False #"Digit sequence " + digits_used + " does not match date string " + datestr

	calc = calc.replace("=","==") #convert equality test
	calc = calc.replace("^","**") #convert exponentiation
	calc = calc.replace(",","") #remove commas, since they may be used legitimately
	calc = calc.replace("x", "*").replace("×", "*") #convert incorrect multiply symbol
	calc = calc.replace("[","(").replace("]",")") #convert incorrect parentheses
	calc = calc.replace("{","(").replace("}",")") #convert incorrect parentheses
	
	#check for extra pluses
	if re.match("[*\/\+-]\+",calc) or re.match("\+[*\/\+-]", calc):
		return False #unnecessary pluses
	
	#print(calc) #DEBUG
	
	#return False for any strings that exhibit dodgy behaviour to cheat the system
	try:
		if "=" not in calc:
			return False #"No equality test found"
		elif "+-" in calc or "-+" in calc:
			return False #"Repeated negation"
		elif ">" in calc or "<" in calc or "!" in calc:
			return False #"Inequality operators
		elif "%" in calc or "--" in calc or "++" in calc:
			return False #"Use of banned operators"
		elif not eval(calc):
			return False #"Calculation incorrect"
		else:
			return True #"Correct!"
	except (SyntaxError, NameError, TypeError, ZeroDivisionError):
		print("WARNING: Expression",calc,"could not be executed")
		return False #"Error executing expression"

students = {}

lines = csv_data.split("\n")
for line in lines:
	if line == "PASTE_HERE":
		print("You didn't paste the forms data!")
		continue
	elif line == "":
		continue #skip empty lines
	
	data = line.split("\",\"")
	if data[0].strip("\"") == "Timestamp":
		continue #skip header row
	datestamp = data[0].split(" ")[0] #should always be of form 2024/11/22
	datestr = datestamp[9:11] + datestamp[6:8] + datestamp[3:5]
	
	student = data[1].strip("\"").upper()
	if student not in students:
		students[student] = {'right': 0, 'wrong': 0, 'submissions': set()}
	
	calc = data[2].strip("\"")
	
	#smart kid warning system
	if "#" in calc or "math" in calc or "def" in calc:
		print("WARNING: student",student,"attempting to use Python syntax.")
	#strip any whitespace before checking if this is a unique submission
	calc = calc.replace(" ","")
	#calc = calc.replace("(","").replace(")","")
	
	
	if calc in students[student]['submissions']:
		print("WARNING: Duplicate submission detected for",student+str("."),"It has not been counted.")
		continue
	students[student]['submissions'].add(calc)

	if check_valid(calc, datestr):
		students[student]['right'] += 1
	else:
		students[student]['wrong'] += 1

students_output = dict(sorted(students.items(), key=lambda x: x[1]['right'], reverse=True))

for student in students_output:
	right = students[student]['right']
	wrong = students[student]['wrong']
	print(student, "got", right, "right out of", right+wrong, "submissions.")