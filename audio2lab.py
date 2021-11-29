import sys
import shutil
import pysinsy
import librosa
import xml.etree.ElementTree as ET
import soundfile as sf
import subprocess

sinsy = pysinsy.Sinsy()
input_audio = "./in/" + sys.argv[1] + ".wav"
input_xml = "./in/" + sys.argv[1] + ".musicxml"
temp_Slab = "./temp/S" + sys.argv[2] + ".lab"
temp_Jlab = "./temp/J" + sys.argv[2] + ".lab"
temp_JlabC = "./temp/convert/J" + sys.argv[2] + "C.lab"
raw_Jlab = "./Julius/wav/" + sys.argv[2] + ".lab"
temp_audio = "./Julius/wav/" + sys.argv[2] + ".wav"
temp_text = "./Julius/wav/" + sys.argv[2] + ".txt"
output_filename = "./out/" + sys.argv[2] + ".lab"
mode = sys.argv[3]


class make_labels:
    def make(self):
        self.check_input()
        self.sinsy_make_lab()
        self.julius_make_lab()

    def check_input(self):
        if len(sys.argv) != 4:
            sys.exit("xml2lab.py [input_filename] [output_filename] [mode]")

        assert sinsy.setLanguages("j", pysinsy.get_default_dic_dir())
        assert sinsy.loadScoreFromMusicXML(input_xml)

    def sinsy_make_lab(self):
        if mode == "mono":
            print("Make mono labels for train")
            is_mono = True
            labels = sinsy.createLabelData(is_mono, 1, 1).getData()

            with open(temp_Slab, "w") as f:
                for l in labels:
                    f.write(str(l) + "\n")

    def julius_make_lab(self):
        y, sr = librosa.core.load(input_audio, sr=16000, mono=True)
        sf.write(temp_audio, y, sr, subtype="PCM_16")
        self.read_XML()

        subprocess.run(["perl", "./segment_julius.pl"], cwd="./Julius")
        shutil.move(raw_Jlab, temp_Jlab)

    def read_XML(self):
        tree = ET.parse(input_xml)  # 入力楽譜ファイル
        root = tree.getroot()
        measure_count = 0
        lyrics = []

        for _ in root.iter("measure"):  # 小節数カウント
            measure_count = measure_count + 1

        for i in range(0, measure_count, 1):
            measure = root[3][i]  # 小節区切り
            for child in measure:
                if child.find('lyric') is not None:
                    lyrics.append(child.find('lyric').find('text').text)

        print('Lyrics : ' + ','.join(lyrics))
        with open(temp_text, "w", encoding='utf-8') as f:
            f.write("".join(lyrics))


class merge_labels:
    def merge(self):
        self.julius2sinsy()
        self.merge2sinsy()

    def julius2sinsy(self):
        Jstart_time = []
        Jend_time = []
        phoneme = []

        with open(temp_Jlab, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                split = line.split(' ')
                Jstart_time.append(float(split[0]))
                Jend_time.append(float(split[1]))
                phoneme.append(split[2])

            Sstart_time = Jstart_time * 10000000
            Send_time = Jend_time * 10000000

        with open(temp_JlabC, 'w', encoding='utf-8') as f:
            for i in range(0, len(Jstart_time)):
                start = int(Sstart_time[i] * 10000000)
                end = int(Send_time[i] * 10000000)
                f.write(str(start) + " " + str(end) + " " + phoneme[i])

    def merge2sinsy(self):
        Sstart_time = []
        Send_time = []
        Sphoneme = []

        Jstart_time = []
        Jend_time = []
        Jphoneme = []
        j = 0

        final = []

        with open(temp_Slab, 'r', encoding='utf-8') as f:  # ファイルを開く
            for line in f.readlines():  # 行をすべて読み込んで1行ずつfor文で回す
                split = line.split(' ')  # 行を半角スペースで分割する
                Sstart_time.append(split[0])
                Send_time.append(split[1])
                Sphoneme.append(split[2])

        with open(temp_JlabC, 'r', encoding='utf-8') as f:  # ファイルを開く
            for line in f.readlines():  # 行をすべて読み込んで1行ずつfor文で回す
                split = line.split(' ')  # 行を半角スペースで分割する
                Jstart_time.append(split[0])
                Jend_time.append(split[1])
                Jphoneme.append(split[2])

        for i in range(0, len(Sphoneme)):
            print(Sphoneme[i] + Jphoneme[j])
            if Sphoneme[i] == Jphoneme[j]:
                final.append(str(Jstart_time[j]) + " " + str(Jend_time[j]) + " " + Sphoneme[i])
                j = j + 1
            elif Sphoneme[i] == "a\n" and Jphoneme[j] == "a:\n":
                final.append(str(Jstart_time[j]) + " " + str(Jend_time[j]) + " " + Sphoneme[i])
                j = j + 1
            elif Sphoneme[i] == "i\n" and Jphoneme[j] == "i:\n":
                final.append(str(Jstart_time[j]) + " " + str(Jend_time[j]) + " " + Sphoneme[i])
                j = j + 1
            elif Sphoneme[i] == "u\n" and Jphoneme[j] == "u:\n":
                final.append(str(Jstart_time[j]) + " " + str(Jend_time[j]) + " " + Sphoneme[i])
                j = j + 1
            elif Sphoneme[i] == "e\n" and Jphoneme[j] == "e:\n":
                final.append(str(Jstart_time[j]) + " " + str(Jend_time[j]) + " " + Sphoneme[i])
                j = j + 1
            elif Sphoneme[i] == "o\n" and Jphoneme[j] == "o:\n":
                final.append(str(Jstart_time[j]) + " " + str(Jend_time[j]) + " " + Sphoneme[i])
                j = j + 1

            elif Sphoneme[i] == "pau\n" and Jphoneme[j] == "silB\n" or Jphoneme == "silE\n":
                final.append(str(Jstart_time[j]) + " " + str(Jend_time[j]) + " " + Sphoneme[i])
                j = j + 1
            elif Sphoneme[i] == "pau\n" and Jphoneme[j] != "silB\n" or Jphoneme != "silE\n":
                sec = int(Send_time[i]) - int(Sstart_time[i])
                start = int(Jend_time[j - 1]) - sec
                end = Jstart_time[j]
                final[i - 1] = Jstart_time[j - 1] + " " + str(start) + " " + Sphoneme[i - 1]
                final.append(str(start) + " " + end + " " + Sphoneme[i])
                print("pau skip")

        with open(output_filename, 'w', encoding='utf-8') as f:
            for i in range(0, len(Sphoneme)):
                f.write(final[i])


make = make_labels()
make.make()

merge = merge_labels()
merge.merge()
