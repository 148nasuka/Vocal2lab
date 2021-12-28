"""
一曲分だけラベル生成したい場合はこちらのスクリプトを動かして下さい。
※管理者権限でないと動かない場合があります

使い方 :
python ./Vocal2lab.py [入力ファイル名] [出力ファイル名] [モード(mono / full)]
※入力ファイル名は ./in フォルダ内から選んでください。
  また、入力ファイルの .wavと.musicxmlは同じ名前にしてください。
"""

import sys  # コマンド変数用
import os  # ファイル作成操作用
import shutil  # ファイル移動操作用
import pysinsy  # Sinsyラベル生成用
import librosa  # ダウンサンプリング用
import soundfile as sf  # ダウンサンプリング書き出し用
import xml.etree.ElementTree as ET  # musicXML読み込み用
import subprocess  # perlプログラム実行用

sinsy = pysinsy.Sinsy()
input_audio = "./in/" + sys.argv[1] + ".wav"
input_xml = "./in/" + sys.argv[1] + ".musicxml"
temp_Slab = "./temp/S" + sys.argv[2] + ".lab"
temp_SFlab = "./temp/SF" + sys.argv[2] + ".lab"
temp_Jlab = "./temp/J" + sys.argv[2] + ".lab"
temp_JlabC = "./temp/convert/J" + sys.argv[2] + "C.lab"
raw_Jlab = "./Julius/wav/" + sys.argv[2] + ".lab"
temp_audio = "./Julius/wav/" + sys.argv[2] + ".wav"
temp_text = "./Julius/wav/" + sys.argv[2] + ".txt"
error_lab = "./out/error/" + sys.argv[2] + ".lab"
output_filename = "./out/" + sys.argv[2] + ".lab"
log_file = "./Julius/wav/" + sys.argv[1] + ".log"
log_dir = "./Julius/log/" + sys.argv[2] + ".log"
mode = sys.argv[3]


# ラベル生成フェーズ
class make_labels:
    def make(self):  # クラス総合
        shutil.rmtree("./Julius/wav/")
        os.mkdir("./Julius/wav/")
        self.check_input()
        self.sinsy_make_lab()
        print("Reading score file...")
        self.julius_make_lab()

    def check_input(self):  # コマンド変数が正しいか、入力ファイル形式は正しいか確認
        if len(sys.argv) != 4:
            sys.exit("xml2lab.py [input_filename] [output_filename] [mode]")

        assert sinsy.setLanguages("j", pysinsy.get_default_dic_dir())
        assert sinsy.loadScoreFromMusicXML(input_xml)

    def sinsy_make_lab(self):  # Sinsyラベルを生成
        is_mono = True
        if mode == "mono":  # モノラベルデータの時
            print("Make mono labels for train")

        labels = sinsy.createLabelData(is_mono, 1, 1).getData()
        with open(temp_Slab, "w") as f:
            for l in labels:
                f.write(str(l) + "\n")

        if mode == "full":  # フルラベルデータの時
            is_mono = False
            print("Make full labels for train")
            labels = sinsy.createLabelData(is_mono, 1, 1).getData()
            with open(temp_SFlab, "w") as f:
                for l in labels:
                    f.write(str(l) + "\n")

    def julius_make_lab(self):  # Juliusラベルを生成
        y, sr = librosa.core.load(input_audio, sr=16000, mono=True)  # ダウンサンプリング
        sf.write(temp_audio, y, sr, subtype="PCM_16")  # ダウンサンプリングを保存
        self.read_XML()

        print("Making Julius label...")
        subprocess.run(["perl", "./segment_julius.pl"], cwd="./Julius")
        shutil.move(raw_Jlab, temp_Jlab)
        shutil.copy(log_file, log_dir)

    def read_XML(self):  # 楽譜ファイル読み込み&歌詞取り込み
        tree = ET.parse(input_xml)  # 入力楽譜ファイル
        root = tree.getroot()
        lyrics = []

        for _ in root.iter("note"):
            if _.find("lyric") is not None:
                lyrics.append(_.find('lyric').find('text').text)
            if _.find("rest") is not None:
                if _.find('type') is not None:
                    time = _.find('type').text
                else:
                    time = "None"
                if time == str("16th") or time == str("quarter") or time == str("eighth") or time == str("half"):
                    if len(lyrics) != 0:
                        lyrics.append(" sp ")
                if _.find("duration").text == str("16") and _.find('type') is None:
                    lyrics.append(" sps ")

        num = len(lyrics)

        count = 0

        while True:
            for i in range(0, num - 1):
                if i < len(lyrics) - 1:
                    if lyrics[i] == " sp " and lyrics[i + 1] == " sp " or \
                            lyrics[i] == " sps " and lyrics[i + 1] == " sps ":
                        lyrics.pop(i)
                        i += 1
                        count += 1
            if count == 0:
                break
            else:
                count = 0

        if lyrics[len(lyrics) - 1] == " sp ":
            lyrics.pop(-1)

        print('Lyrics : ' + ','.join(lyrics))
        if lyrics[0] == " sp " or lyrics[0] == " sps ":
            if lyrics[1] == " sps " or lyrics[1] != " sp ":
                lyrics.pop(0)
            elif lyrics[1] == " sp ":
                lyrics.pop(0)
                lyrics.pop(0)

        for i in range(0, len(lyrics)):
            if lyrics[i] == " sps ":
                print(" ")
                lyrics[i] = " sp "

        print('Lyrics : ' + ','.join(lyrics))
        with open(temp_text, "w", encoding='utf-8') as f:  # 歌詞データを保存
            f.write("".join(lyrics))


# ラベル修正フェーズ
class merge_labels:
    def merge(self):  # クラス総合
        print("Merging labels...")
        self.julius2sinsy()
        self.merge2sinsy()

    def julius2sinsy(self):  # Juliusの時間単位をSinsyの時間単位に合わせる（10msから100nsへ）
        Jstart_time = []
        Jend_time = []
        phoneme = []

        with open(temp_Jlab, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                split = line.split(' ')
                Jstart_time.append(float(split[0]))
                Jend_time.append(float(split[1]))
                phoneme.append(split[2])

        with open(temp_JlabC, 'w', encoding='utf-8') as f:
            for i in range(0, len(Jstart_time)):
                start = int(Jstart_time[i] * 10000000)
                end = int(Jend_time[i] * 10000000)
                f.write(str(start) + " " + str(end) + " " + phoneme[i])

    def merge2sinsy(self):  # 変換後のJulius音素時間をSinsyの音素時間と置き換える（音素はSinsy基準）
        Sstart_time = []
        Send_time = []
        Sphoneme = []

        SFphoneme = []

        Jstart_time = []
        Jend_time = []
        Jphoneme = []

        Cstart_time = []
        Cend_time = []
        Cphoneme = []

        j = 0

        final = []

        with open(temp_Slab, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                split = line.split(' ')
                Sstart_time.append(split[0])
                Send_time.append(split[1])
                Sphoneme.append(split[2])

        if mode == "full":
            with open(temp_SFlab, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    split = line.split(' ')
                    SFphoneme.append(split[2])

        with open(temp_JlabC, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                split = line.split(' ')
                Jstart_time.append(split[0])
                Jend_time.append(split[1])
                Jphoneme.append(split[2])

        for i in range(0, len(Sphoneme)):  # JuliusとSinsyの音素ラベルの対応を取りながら置き換え
            # print(Sphoneme[i] + Jphoneme[j])

            if Sphoneme[i] == "sil\n" and Jphoneme[j] == "silB\n" or \
                    Sphoneme[i] == "sil\n" and Jphoneme[j] == "sp\n":  # 無音ラベル（開始）
                if mode == "full":
                    final.append(str(Sstart_time[i]) + " " + str(Send_time[i]) + " " + SFphoneme[i])
                elif mode == "mono":
                    final.append(str(Sstart_time[i]) + " " + str(Send_time[i]) + " " + Sphoneme[i])
                j = j + 1
            elif Sphoneme[i] == "pau\n" and Sphoneme[i - 1] == "sil\n" and Jphoneme == "silB\n" or \
                    Sphoneme[i] == "pau\n" and Sphoneme[i - 1] == "sil\n" and Jphoneme == "sp\n":  # 無音ラベル（開始連続）
                if mode == "full":
                    final.append(str(Send_time[i - 1]) + " " + str(Jend_time[j]) + " " + SFphoneme[i])
                elif mode == "mono":
                    final.append(str(Send_time[i - 1]) + " " + str(Jend_time[j]) + " " + Sphoneme[i])
                j = j + 1
            elif Sphoneme[i] == Jphoneme[j] or \
                    Sphoneme[i] == "a\n" and Jphoneme[j] == "a:\n" or \
                    Sphoneme[i] == "i\n" and Jphoneme[j] == "i:\n" or \
                    Sphoneme[i] == "u\n" and Jphoneme[j] == "u:\n" or \
                    Sphoneme[i] == "e\n" and Jphoneme[j] == "e:\n" or \
                    Sphoneme[i] == "o\n" and Jphoneme[j] == "o:\n" or \
                    Sphoneme[i] == "o\n" and Jphoneme[j] == "o:\n" or \
                    Sphoneme[i] == "cl\n" and Jphoneme[j] == "q\n" or \
                    Sphoneme[i] == "pau\n" and Jphoneme[j] == "sp\n" or \
                    Sphoneme[i] == "pau\n" and Jphoneme[j] == "silB\n" or \
                    Sphoneme[i] == "pau\n" and Jphoneme[j] == "silE\n":  # 単純置き換え
                if mode == "full":
                    final.append(str(Jstart_time[j]) + " " + str(Jend_time[j]) + " " + SFphoneme[i])
                elif mode == "mono":
                    final.append(str(Jstart_time[j]) + " " + str(Jend_time[j]) + " " + Sphoneme[i])
                j = j + 1
            elif Sphoneme[i] == "pau\n" and Jphoneme[j] != "silB\n" or \
                    Sphoneme[i] == "pau\n" and Jphoneme[j] != "silE\n" or \
                    Sphoneme[i] == "pau\n" and Jphoneme[j] != "sp\n" or \
                    Sphoneme[i] == "br\n":  # 無音ラベル（抜け）
                Ssec = int(Send_time[i]) - int(Sstart_time[i])
                Jsec = int(Jend_time[j - 1]) - int(Jstart_time[j - 1])
                start = int(Jend_time[j - 1]) - Ssec
                end = Jstart_time[j]
                if Ssec > Jsec:
                    if mode == "full":
                        final[i - 1] = Jstart_time[j - 1] + " " + Sstart_time[i] + " " + SFphoneme[i - 1]
                        final.append(Sstart_time[i] + " " + end + " " + SFphoneme[i])
                    elif mode == "mono":
                        final[i - 1] = Jstart_time[j - 1] + " " + Sstart_time[i] + " " + Sphoneme[i - 1]
                        final.append(Sstart_time[i] + " " + end + " " + Sphoneme[i])
                else:
                    if mode == "full":
                        final[i - 1] = Jstart_time[j - 1] + " " + str(start) + " " + SFphoneme[i - 1]
                        final.append(str(start) + " " + end + " " + SFphoneme[i])
                    elif mode == "mono":
                        final[i - 1] = Jstart_time[j - 1] + " " + str(start) + " " + Sphoneme[i - 1]
                        final.append(str(start) + " " + end + " " + Sphoneme[i])
            elif i != len(Sphoneme):
                if Sphoneme[i] == "sil\n" and Sphoneme[i + 1] == "sil\n":  # 1小節以上の無音
                    if mode == "full":
                        final.append(str(Sstart_time[i]) + " " + str(Send_time[i]) + " " + SFphoneme[i])
                    elif mode == "mono":
                        final.append(str(Sstart_time[i]) + " " + str(Send_time[i]) + " " + Sphoneme[i])
                elif Sphoneme[i] == "pau\n" and Sphoneme[i + 1] == "pau\n":  # 2拍以上の無音
                    if mode == "full":
                        final.append(str(Jend_time[i]) + " " + str(Send_time[i]) + " " + SFphoneme[i])
                    elif mode == "mono":
                        final.append(str(Jend_time[i]) + " " + str(Send_time[i]) + " " + Sphoneme[i])
                elif Sphoneme[i] == "pau\n" and Sphoneme[i + 1] != "pau\n":  # 1拍の無音
                    if mode == "full":
                        final.append(str(Send_time[i - 1]) + " " + str(Jstart_time[j]) + " " + SFphoneme[i])
                    elif mode == "mono":
                        final.append(str(Send_time[i - 1]) + " " + str(Jstart_time[j]) + " " + Sphoneme[i])
            elif i != 0:
                if Sphoneme[i] == "pau\n" and Sphoneme[i - 1] == "sil\n" and Jphoneme[j] == "silB\n":
                    if mode == "full":
                        final.append(str(Sstart_time[i]) + " " + str(Jend_time[i]) + " " + SFphoneme[i])
                    elif mode == "mono":
                        final.append(str(Sstart_time[i]) + " " + str(Jend_time[i]) + " " + Sphoneme[i])
                    j = j + 1

        with open(output_filename, 'w', encoding='utf-8') as f:  # 最終結果を保存
            for i in range(0, len(Sphoneme)):
                f.write(final[i])

        with open(output_filename, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                split = line.split(' ')
                Cstart_time.append(int(split[0]))
                Cend_time.append(int(split[1]))
                Cphoneme.append(split[2])

        for i in range(0, len(Cstart_time)):
            if Cstart_time[i] > Cend_time[i]:
                shutil.move(output_filename, error_lab)
            assert Cstart_time[i] < Cend_time[i], "ERROR：音素の開始時間が終了時間よりも未来に設定されています\n" \
                                                  "位置：[{0}]".format(i)
            if i != 0:
                if Cstart_time[i] != Cend_time[i - 1]:
                    shutil.move(output_filename, error_lab)
                assert Cstart_time[i] == Cend_time[i - 1], "ERROR：一つ前の音素の終了時間と現在の音素の開始時間が不一致です\n" \
                                                           "位置：[{0}]".format(i)

        print("Done")


make = make_labels()
make.make()

merge = merge_labels()
merge.merge()
