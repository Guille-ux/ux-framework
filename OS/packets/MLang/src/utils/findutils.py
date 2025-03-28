ENTRY_SYMBOL = "_entry:"
END_ENTRY_SYMBOL = ":end_"

def find_entry(text):
	tokens = text.split("\n")
	code = []
	set = False
	for i in tokens:
		if set == True:
			code.append(i)
		if i == END_ENTRY_SYMBOL:
			break
		if i == ENTRY_SYMBOL:
			set = True
	return code

def find_funcs(text):
	funcs = []
	lines = text.split("\n")
	i = 0
	while i < len(lines):
		if lines[i].startswith("func "):
			parts = lines[i][5:]
			name = parts.split(":")[0].strip()
			code = []
			b = i + 1
			while b < len(lines):
				if lines[b] == "}":
					break
				code.append(lines[b])
				b += 1
			funcs.append({"name":name, "code":code})
		i += 1
	return funcs
