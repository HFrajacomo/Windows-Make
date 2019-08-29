from subprocess import check_output
import sys

def better_replace(text, chars=[" ", "\t", "\n"]):
	aux = ""
	for element in text:
		if(not element in chars):
			aux += element
	return aux

try:
	file = open("Makefile", "r")
except:
	print("MAKE: Couldn't find Makefile. Do 'make create' to generate a Makefile")

RESERVED_RULES = ["create"]

make_data = file.readlines()
file.close()

current_rule = None
executions = []
hashing = {}

# Parse Makefile
for line in make_data:
	if(line == ""):
		continue
	elif(":" in line):
		if(current_rule != None):
			hashing[current_rule] = executions
		current_rule = better_replace(line.split(":")[0])
		if(current_rule in RESERVED_RULES):
			print("MAKE: Ignored rule '" + current_rule + "' because it's a reserved rule")
			current_rule = None
			executions = []
			continue
		executions = []
	elif(line[0] == "\t" and current_rule != None):
		executions.append(line[1:].replace("\n", ""))
if(executions != []):
	hashing[current_rule] = executions


# Check rule
try:
	query = sys.argv[1]
except IndexError:
	query = "all"

if(query not in hashing.keys()):
	print("MAKE: Rule '" + query + "' not found")
	exit()
else:
	for element in hashing[query]:
		print(check_output(["powershell", element], universal_newlines=True))