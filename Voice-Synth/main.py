from synth import VoiceMixer
from synth import arpabet_to_phoneme
import cmudict
import sys

synthethizer = VoiceMixer(voice_dir="dataset", prefix="wav", crossfade=300)
pronounciation = cmudict.dict()

to_delete = ".,;:-+*|1234567890'¡!¨[]<>_ç{}´`¿?$%#@·'!=ºª"

filename = sys.argv[1]
spaces_time = int(sys.argv[2])
out_file = sys.argv[3]
with open(filename, "r") as f:
	text = f.read()
for char in to_delete:
	text.strip(char)
text = text.strip('"')
text = text.lower()
words = text.split()
words_sounds = []
for word in words:
	if word in pronounciation:
		pronounce = pronounciation[word]
		phonems = [arpabet_to_phoneme(pho) for pho in pronounce[0]]
		synthethized = synthethizer.mix_sound(phonems)
		words_sounds.append(synthethized)
space_sound = synthethizer.get_sound("pause")
space = space_sound * spaces_time
main_sound = synthethizer.join_sounds(words_sounds, space)
synthethizer.save_sound(main_sound, out_file)
synthethizer.play_sound(main_sound)
print("[+] Audio Generated [+]")
try:
	pass
except Exception as e:
	print(f"[!] Error: {e} [!]")

