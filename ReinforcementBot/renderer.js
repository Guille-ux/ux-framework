// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.
// Copyright (c) 2025 Guillermo Leira Temes
// 
const {ipcRenderer} = require("electron");

async function sendToAPI(responsesFile, stopwordsFile, action, data) {
	const args = {
		responses_file: responsesFile,
		stopwords_file: stopwordsFile,
		action: action,
		data: [data]
	};
	return await ipcRenderer.invoke("send-msg", args);
}

const history = [];

const settingsButton = document.getElementById("ajustes");
const modal = document.getElementById("settings");
const rfile = document.getElementById("responses_file");
const sfile = document.getElementById("stopwords_file");
const save_button = document.getElementById("save");
const filenames = ["responses.txt", "stopwords.txt"];
const goodButton = document.getElementById("y"); //y 
const badButton = document.getElementById("n"); // n
const askButton = document.getElementById("send"); //send
const response = document.getElementById("out_data");
const question = document.getElementById("question");
const save_chat = document.getElementById("save-chat");

settingsButton.addEventListener("click", ()=> {
	modal.classList.toggle("hided");
});

save_button.addEventListener("click", async () => {
	const refile = rfile.files[0];
	const safile = sfile.files[0];
	data = [await refile.text(), await safile.text()];
	ipcRenderer.send("save-file", filenames[0], data[0]);
	ipcRenderer.send("save-file", filenames[1], data[1]);
	sendToAPI(filenames[0], filenames[1], "new");
});

function scrollToBottom() {
	window.scrollTo({top: document.body.scrollHeight, behavior: "smooth"});
}

function readFileContent(file) {
	return new Promise((resolve, reject) => {
		let reader = new FileReader();
		reader.onload = (e) => {
			resolve(e.target.result);
		};
		reader.onerror = (e) => {
			reject(e.target.error);
		};
		reader.readAsText(file);
	});
}

askButton.addEventListener("click", () => {
	sendToAPI(filenames[0], filenames[1], "ask", question.value).then(answer => {
		response.innerHTML += "<div class='user-message'>" + question.value + "</div>";
		response.innerHTML += "<div class='message'> <img src='favicon.svg' alt='Logo' width='50' height='50'>" + answer + "</div>" ;
		let new_h = {"ques":question.value, "answer":answer};
		history.push(new_h);
		scrollToBottom();
	});
});

goodButton.addEventListener("click", () => {
	sendToAPI(filenames[0], filenames[1], "update-log", "y").then(answer => {
		response.innerHTML += answer + "\n";
		scrollToBottom();
	});
});
badButton.addEventListener("click", () => {
	sendToAPI(filenames[0], filenames[1], "update-log", "n").then(answer => {
		response.innerHTML += answer + "\n";
		scrollToBottom();
	});
});

save_chat.addEventListener("click", ()=> {
	let text = "Conversation History: \n";
	let a = "Question: ";
	let b = "Swelshiniano's Answer: ";
	for (let i=0; i<history.length; i++) {
		text += a + history[i].ques + "\n";
		text += b + history[i].answer + "\n";
		text += "\n";
	}
	ipcRenderer.send("save-f", "history.txt", text);
});
