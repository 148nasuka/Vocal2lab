import pysinsy
import sys

sinsy = pysinsy.Sinsy()

if len(sys.argv) != 4:
    sys.exit("music2lab.py [input_filename] [output_filename] [generate / train]")
input_filename = "./xml_in/" + sys.argv[1]
output_filename = "./lab_out/" + sys.argv[2]
mode = sys.argv[3]

assert sinsy.setLanguages("j", pysinsy.get_default_dic_dir())
assert sinsy.loadScoreFromMusicXML(input_filename)

if mode == "train":
    print("Make mono labels from musicxml")
    is_mono = True
elif mode == "generate":
    print("Make full labels from musicxml")
    is_mono = False
else:
    sys.exit("music2lab.py [input_filename] [output_filename] [generate / train]")

labels = sinsy.createLabelData(is_mono, 1, 1).getData()
for l in labels:
    print(l)

print("Compleate")

with open(output_filename, "w") as f:
    for l in labels:
        f.write(str(l) + "\n")
