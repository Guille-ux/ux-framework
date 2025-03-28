import socket  # noqa: F401
import threading
import json
import time


class Tinrux:
	def __init__(self, hostname, port=6379, buffer_size=1024*1024, rdb_file="tdb.json", new=True):
		self.version = "1.0"
		self.host = hostname
		self.port = port
		self.buffer = buffer_size
		self.server_socket = socket.create_server((self.host, self.port), reuse_port=True)
		self.db = {}
		self.rdb_file = rdb_file
		if new:
			self.save_rdb()
	def save_rdb(self):
		try:
			with open(self.rdb_file, "w") as f:
				json.dump(self.db, f)
			return "+OK\r\n"
		except Exception as e:
			return f"-ERR Error saving RDB: {e}\r\n"
	def load_rdb(self):
		try:
			with open(self.rdb_file, "r") as f:
				self.db = json.load(f)
			return "+OK\r\n"
		except Exception as e:
			return f"-ERR Error loading RDB: {e}\r\n"
	def expire(self, key, stime):
		time.sleep(stime)
		try:
			del self.db[key]
		except Exception as e:
			print(f"[!] Error: {e} [!]")
	def parse_arg(self, arg): # devuelve tipo de argumento más valor, si es que hay
		if arg.startswith(b"*"):
			return {"type":"array", "data":int(arg[1:])}
		elif arg.startswith(b"$"):
			return {"type":"len", "data":int(arg[1:])}
		elif arg.startswith(b"-"):
			return {"type":"error", "data":int(arg[1:])}
		elif arg.startswith(b":"):
			return {"type":"int", "data":int(arg[1:])}
		else:
			return {"type":"command", "data":arg}
	def parse_command(self, data):
		lines = data.split(b"\r\n") # hago split con '\r\n' porque toda parte lo lleva, tengo la intención de devolver los argumentos y ya
		if not lines:
			return None
		first = self.parse_arg(lines[0])
		if first["type"] != "array":
			return None
		# Finnish this
		num_args = first["data"]
		i = 1
		args = []
		while i < len(lines):
			parsed = self.parse_arg(lines[i])
			if parsed["type"]!="len":
				args.append(parsed)
			i+=1
		return args
	def proccess_args(self, args):
		command = args[0]["data"]
		if command == b"PING" or command == b"ping":
			return PONG
		elif command == b"SET" or command == b"set":
			if len(args) != 4:
				return "-ERR wrong number of arguments for 'set' command \r\n"
			key = args[1]["data"].decode()
			value = args[2]["data"].decode()
			self.db[key] = value
			return "+OK\r\n"
		elif command == b"GET" or command == b"get":
			if len(args) != 3:
				return "-ERR wrong number of arguments for 'get' command\r\n"
			key = args[1]["data"].decode()
			if key in self.db:
				value = self.db[key]
				return f"${len(value)}\r\n{value}\r\n"
			else:
				return "$-1\r\n"
		elif command == b"DEL" or command == b"del":
			if len(args)!=3:
				return "-ERR wrong number of arguments for 'del' command\r\n"
			key = args[1]["data"].decode()
			if key in self.db:
				del self.db[key]
				return "+OK\r\n"
			else:
				return "-ERR key doesn't exists\r\n"
		elif command == b"SAVE" or command == b"save":
			return self.save_rdb()
		elif command == b"EXPIRE" or command == b"expire":
			if len(args)!=4:
				return "-ERR wrong number of arguments for 'expire' command\r\n"
			key = args[1]["data"].decode()
			stime = args[2]["data"].decode()
			try:
				tim = int(stime)
			except Exception as e:
				print(f"[!] Error: {e} [!]")
				return "-ERR the time need's to be a number\r\n"
			if key in self.db:
				expire = threading.Thread(target=self.expire, args=(key, tim), daemon=True)
				expire.start()
			else:
				return "-ERR the key doesn't exist\r\n"
			return "+OK\r\n"
		elif command == b"HELP" or command == b"help":
			help = "LIST OF COMMAND AVALIABLE:\r\n"
			help += "PING \r\n"
			help += "SET key value\r\n"
			help += "GET key\r\n"
			help += "DEL key\r\n"
			help += "EXPIRE key time\r\n"
			help += "SAVE\r\n"
			help += "HELP\r\n"
			return help
		else:
			return "-ERR unknow command\r\n"
	def auto_save(self, stime):
		while True:
			time.sleep(stime)
			self.save_rdb()
	def handle_client(self, client, address):
		print(f"[+] Connection from {address} [+]")
		try:
			while True:
				data = client.recv(self.buffer)
				if not data:
					break
				print(f"[+] Request from {address} : {data.decode().strip()} [+]")
				# Procesar comando
				response = self.proccess_args(self.parse_command(data))
				client.send(response.encode())
		except Exception as err:
			print(f"[!] Error : {err} [!]")
		
		finally:
			client.close()
			print(f"[*] Client : {client} has  Disconnected [*]")
	def main(self, auto_time=900):
		print(f"[+] Running redis-ux server {self.version} on {self.host} at {self.port} [+]")
		self.load_rdb()
		auto_saver = threading.Thread(target=self.auto_save, args=(auto_time), daemon=True)
		while True:
			conn, address = self.server_socket.accept()
			thread = threading.Thread(target=self.handle_client, args=(conn, address), daemon=True)
			thread.start()
			
