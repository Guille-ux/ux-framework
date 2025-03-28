from playsound import playsound
from pydub.playback import play
import pydub


arpabet_to = {
    'AA': 'a_colon',
    'AE': 'æ',
    'AH': 'ʌ',
    'AO': 'ɔ_colon',
    'AW': 'aʊ',
    'AY': 'aɪ',
    'EH': 'e',
    'ER': 'ɜ_colon',
    'EY': 'eɪ',
    'IH': 'i',
    'IY': 'i_colon',
    'OW': 'əʊ',
    'OY': 'ɔɪ',
    'UH': 'ʊ',
    'UW': 'u_colon',
    'R': 'r',
    'L': 'l',
    'M': 'm',
    'N': 'n',
    'NG': 'ŋ',
    'CH': 'ʈʃ',
    'JH': 'dʒ',
    'F': 'f',
    'V': 'v',
    'TH': 'θ',
    'DH': 'ð',
    'S': 's',
    'Z': 'z',
    'SH': 'ʃ',
    'ZH': 'ʒ',
    'HH': 'h',
    'W': 'w',
    'Y': 'j',
    'P': 'p',
    'B': 'b',
    'T': 't',
    'D': 'd',
    'K': 'k',
    'G': 'g',
    'UX': 'ʊ',
    'IX': 'i',
    'AX': 'ə',
    'AXR': 'ɚ',
    'EH0': 'e',
    'EH1': 'e',
    'EH2': 'e',
    'IH0': 'i',
    'IH1': 'i',
    'IH2': 'i',
    'AH0': 'ə',
    'AH1': 'ʌ',
    'AH2': 'ʌ',
    'UW0': 'u_colon',
    'UW1': 'u_colon',
    'UW2': 'u_colon',
    'IY0': 'i_colon',
    'IY1': 'i_colon',
    'IY2': 'i_colon',
    'AO0': 'ɔ_colon',
    'AO1': 'ɔ_colon',
    'AO2': 'ɔ_colon',
    'UH0': 'ʊ',
    'UH1': 'ʊ',
    'UH2': 'ʊ',
    'ER0': 'ɜ_colon',
    'ER1': 'ɜ_colon',
    'ER2': 'ɜ_colon',
    'EL': 'l',
    'EM': 'm',
    'EN': 'n',
    'NX': 'n',
    'DX': 'd',
    'WH': 'w',
    'Q': 'k',
    'PCL': 'p',
    'TCL': 't',
    'KCL': 'k',
    'BCL': 'b',
    'DCL': 'd',
    'GCL': 'g',
    'HCL': 'h',
    'PAU': 'pause'
}

def arpabet_to_phoneme(arpabet):
	base_phoneme = arpabet.rstrip("012")
	if base_phoneme in arpabet_to:
		return arpabet_to[base_phoneme]
	else:
		print(f"[!] Not in Arpabet to {base_phoneme} [!]")
		return None

class EncodeTranslator:
	def __init__(self, set_a, set_b):
		self.set_a = set_a
		self.set_b = set_b
	def translate(self, char, ab):
		if ab == "a":
			return self.set_b[self.set_a.index(char)]
		elif ab=="b":
			return self.set_a[self.set_b.index(char)]
		else:
			return None

class VoiceMixer:
	def __init__(self, voice_dir="voice", prefix="mp3", exports="exports", crossfade=350):
		self.voice = voice_dir
		self.prefix = prefix
		self.crossfade = crossfade
		self.exports = exports
	def get_sound(self, sound):
		if sound is None:
			print("[!] None Sound Received [!]")
			return None
		
		ruta = self.voice + "/" + sound + "." + self.prefix
		try:
			return pydub.AudioSegment.from_file(ruta, self.prefix)
		except Exception as e:
			print(f"[!] Error: {e} [!]")
		return False
	def mix_sound(self, sound_list):
		output = None
		for sound in sound_list:
			audio = self.get_sound(sound)
			if audio:
				if output is None:
					output = audio
				else:
					output = output.append(audio, self.crossfade)
		return output
	def play_mix(self, sound_list):
		play_sound = self.mix_sound(sound_list)
		play(play_sound)
	def save_audio(self, sound):
		sound.export(sound, format=self.prefix)
	def save_mix(self, sound_list, name):
		sound = self.mix_sound(sound_list)
		sound.export(self.exports + "/" + name + "." + self.prefix, format=self.prefix)
	def play_sound(self, sound):
		play(sound)
	def save_sound(self, sound, name):
		sound.export(self.exports+"/"+name+"."+self.prefix, format=self.prefix)
	def join_sounds(self, sounds, space_sound):
		output = None
		for audio in sounds:
			if output is None:
				output = audio
			else:
				output = output.append(audio, 0)
				output = output.append(space_sound, 0)
		return output

class VoiceSynth:
	def __init__(self, voice_dir="voice", prefix="mp3"):
		self.voice = voice_dir
		self.prefix = prefix
	def play(self, sound):
		playsound(self.voice + "/" + sound + "." + self.prefix)

