def parse_var(var_def):
	code = []
	if not var_def.startswith("var "):
		raise Exception("Not a variable def → " + var_def)
	else:
		parts = var_def[4:].split(" ")
		name = parts[0]
		try:
			num = int(parts[1])
			code.append(f"var_num {name} {parts[1]}\n")
		except Exception:
			code.append(f"var_var {name} {parts[1]}\n")
		i = 2
		while i < len(parts):		
			if parts[i] == "*":
				if var(parts[i+1]):
					code.append(f"{name} *= {parts[i+1]}\n")
				else:
					code.append(f"var_num tmp {parts[i+1]}\n")
					code.append(f"{name} *= tmp\n")
					code.append(f"remove tmp\n")
			elif parts[i] == "-":
				if var(parts[i+1]):
					code.append(f"{name} -= {parts[i+1]}\n")
				else:
					code.append(f"var_num tmp {parts[i+1]}\n")
					code.append(f"{name} -= tmp\n")
					code.append(f"remove tmp\n")
			elif parts[i] == "/":
				if var(parts[i+1]):
					code.append(f"{name} /= {parts[i+1]}\n")
				else:
					code.append(f"var_num tmp {parts[i+1]}\n")
					code.append(f"{name} /= tmp\n")
					code.append(f"remove tmp\n")
			elif parts[i] == "+":
				if var(parts[i+1]):
					code.append(f"{name} += {parts[i+1]}\n")
				else:
					code.append(f"var_num tmp {parts[i+1]}\n")
					code.append(f"{name} += tmp\n")
					code.append(f"remove tmp\n")
			i += 2
		return "".join(code)
			 
def var(part):
	try:
		num = int(part)
	except Exception:
		return True
	return False
