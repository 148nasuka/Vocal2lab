# coding: UTF-8
# v0.0.1 (2022/03/05)

import pysinsy
import sys

sinsy = pysinsy.Sinsy()

if len(sys.argv) != 3:
    sys.exit("music2lab.py [入力ファイル名] [出力ファイル名]")
input_filename = "./xml_in/" + sys.argv[1] + ".musicxml"
output_filename = "./lab_out/" + sys.argv[2] + ".lab"

assert sinsy.setLanguages("j", pysinsy.get_default_dic_dir())
assert sinsy.loadScoreFromMusicXML(input_filename)

is_mono = False

labels = sinsy.createLabelData(is_mono, 1, 1).getData()
for l in labels:
    print(l)

print("完了")

with open(output_filename, "w") as f:
    for l in labels:
        f.write(str(l) + "\n")
