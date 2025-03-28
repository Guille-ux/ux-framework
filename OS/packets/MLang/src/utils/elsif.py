def coparse(code, n):
	txt = code.split("\n")
	final_txt = []
	counter = 0
	counter_list = []
	for i in txt:
		rtxt = []
		if i.startswith("if")
			counter_list.append(counter)
			splitted = i.split(" ")
			cof = splitted[1]
			tco = splitted[2]
			cos = splitted[3]
			the = splitted[4]
			if tco == "==":
				rtxt.append(f"var_var tmp {cos}\n")
				rtxt.append(f"tmp -= {cof}\n")
				rtxt.append(f"jeq tmp {the}\n")
				rtxt.append(f"remove tmp\n")
			if tco == ">":
				rtxt.append(f"var_var tmp {cos}\n")
				rtxt.append(f"tmp -= {cof}\n")
				rtxt.append(f"jlt tmp {the}\n")
				rtxt.append(f"remove tmp\n")
			if tco == "<":
				rtxt.append(f"var_var tmp {cos}\n")
				rtxt.append(f"tmp -= {cof}\n")
				rtxt.append(f"jgt tmp {the}\n")
				rtxt.append(f"remove tmp\n")
			if tco == "!=":
				rtxt.append(f"var_var tmp {cos}\n")
				rtxt.append(f"tmp -= {cof}\n")
				rtxt.append(f"jnq tmp {the}\n")
				rtxt.append(f"remove tmp\n")
			final_txt.append(rtxt)
		counter += 1
	try:
		return [final_txt[n], counter_list[n]]
	except Exception:
		raise Exception("Fatal ERROR")
