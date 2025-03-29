# The _Ux-framework_
a framework with a lot of things, and they work
## Things that this has
- A DataBase (Tinrux)
- A Voice Synthethizer using pydub and a folder with all phonems
- A simplified OpenGL (help using graphics on C) and it has a utility for loading BMP images
- My Kernel
- Some of my apps
- Librarys

### Prequisites

- **Voice Synthethizer**
	- *pydub* → ```pip install pydub```
	- *playsound* → ```pip install playsound```
	- *cmudict* → ```pip install cmudict```
- **gamec.h** (simplified OpenGL) ¡Extra this have a file to compile it easier (without puting all linkers)!
	- *libgl1-mesa-dev* ```sudo apt-get install libgl1-mesa-dev```
	- *freeglut3-dev* ```sudo apt-get install freeglut3-dev```


### Notes
- **Voice Synthethizer**
	- You need to put in a folder the 44 english phonemes.
	- link for the phonems: <a href="https://github.com/moh3n9595/phonemes-dataset">Phonemes</a>
	- I recommend edit the phonemes files because in some of them there is a large pause
