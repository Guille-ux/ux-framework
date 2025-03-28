import os
import sys

if sys.argv[1] == "help":
	print("usage → python3 compile.py [input_file] [out_file]")
else:
	try:
		in_file = sys.argv[1]
		out_file = sys.argv[2]
		os.system(f"gcc -o {out_file} {in_file} -lglut -lGL -lGLU")
		print("[+] File Compiled! [+]")
	except Exception as e:
		print(f"[!] Error: {e} [!]")
