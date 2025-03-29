# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# Copyright (c) 2025 Guillermo Leira Temes
# 
import rbot as bot
import sys
import json

responses_file = sys.argv[1]
stopwords_file = sys.argv[2]
maxis = 50000

apibot = bot.ReinforcementBot(responses_file, stopwords_file, maxis)


returned = ""
log_file = "logs.json"
if sys.argv[3]=="new":
	apibot.file_bot("save_file.json", "save")
	returned = "¡Bot Created Successful!"
elif sys.argv[3] == "ask":
	apibot.file_bot("save_file.json", "load")
	question = "".join(sys.argv[4:])
	returned = apibot.ask(question)
	with open(log_file, "w") as f:
		json.dump(apibot.last, f)
elif sys.argv[3] == "update-log":
	apibot.file_bot("save_file.json", "load")
	feed = sys.argv[4]
	with open(log_file, "r") as f:
		apibot.last = json.load(f)
	apibot.reforce(feed)
	returned = "¡Thanks!"
	apibot.file_bot("save_file.json", "save")
print(returned)
