# coding: UTF-8
# v0.0.2 (2022/03/12)

import sys  # コマンド変数用
import os  # ファイル作成操作用
import shutil  # ファイル移動操作用
import pysinsy  # Sinsyラベル生成用
import librosa  # ダウンサンプリング用
import wave  # ダウンサンプリング用
import soundfile as sf  # ダウンサンプリング書き出し用
import xml.etree.ElementTree as ET  # musicXML読み込み用
import subprocess  # perlプログラム実行用

if len(sys.argv) == 1:  # チェック
    os.system("python help.py")
    sys.exit()

if sys.argv[1] == "--help":
    os.system("python help.py")
    sys.exit()

if sys.argv[1] == "--cash_clear":  # キャッシュクリアオプション
    print("デバッグ用ラベルデータ と ダウンサンプリング音声 を消去しますか？(y/n)")
    ans = input()
    if ans == "y":
        print("\n消去中...\n")
        shutil.rmtree("./bin/temp")
        os.mkdir("./bin/temp")
        os.mkdir("./bin/temp/convert")
        os.mkdir("./bin/temp/downscaling")
        sys.exit("完了\n")

if len(sys.argv) == 2:
    os.system("python help.py")
    sys.exit()

if sys.argv[1] == "--multi" and sys.argv[2] == "nnsvs":
    os.system("python MultiExecution.py nnsvs")
    sys.exit()

if sys.argv[1] == "--multi" and sys.argv[2] == "enunu":
    os.system("python MultiExecution.py enunu")
    sys.exit()

if len(sys.argv) == 3 and sys.argv[2] == "nnsvs" or \
        len(sys.argv) == 3 and sys.argv[2] == "enunu":
    input_sr_mode = sys.argv[2]

if len(sys.argv) == 4 and sys.argv[3] == "nnsvs" or \
        len(sys.argv) == 4 and sys.argv[3] == "enunu":
    input_sr_mode = sys.argv[3]

if len(sys.argv) != 4:
    sys.exit("ERROR : 使い方は以下のコマンドで確認できます\nVocal2lab.py -help")

sinsy = pysinsy.Sinsy()
if input_sr_mode == "nnsvs":
    if os.path.isfile("./Data_in/NNSVS/" + sys.argv[1] + ".musicxml"):
        input_xml = "./Data_in/NNSVS/" + sys.argv[1] + ".musicxml"
    else:
        input_xml = "./Data_in/NNSVS/" + sys.argv[1] + ".xml"
    input_audio = "./Data_in/NNSVS/" + sys.argv[1] + ".wav"
elif input_sr_mode == "enunu":
    input_xml = "./bin/Utau2sinsy/xml_out/" + sys.argv[1] + ".xml"
    input_audio = "./Data_in/ENUNU/" + sys.argv[1] + ".wav"
input_ust = "./Data_in/ENUNU/" + sys.argv[1] + ".ust"
temp_Slab = "./bin/temp/S" + sys.argv[2] + ".lab"
temp_SFlab = "./bin/temp/SF" + sys.argv[2] + ".lab"
temp_Jlab = "./bin/temp/J" + sys.argv[2] + ".lab"
temp_JlabC = "./bin/temp/convert/J" + sys.argv[2] + "C.lab"
raw_Jlab = "./bin/Julius/wav/" + sys.argv[2] + ".lab"
temp_audio = "./bin/Julius/wav/" + sys.argv[2] + ".wav"
down_audio = "./bin/temp/downscaling/" + sys.argv[2] + ".wav"
temp_text = "./bin/Julius/wav/" + sys.argv[2] + ".txt"
error_lab = "./Data_out/error/" + sys.argv[2] + ".lab"
output_filename = "./Data_out/" + sys.argv[2] + ".lab"
log_file = "./bin/Julius/wav/" + sys.argv[1] + ".log"
log_dir = "./bin/Julius/log/" + sys.argv[2] + ".log"

print("mode : " + input_sr_mode)

if input_sr_mode == "enunu":
    print("ustファイル名を読み込み中...")
    u2s = os.path.abspath("./bin/Utau2sinsy/utau2sinsy.exe")
    ust = os.path.abspath(input_ust)
    command = "echo enter | " + u2s + " " + ust
    os.system(command)
    shutil.move("./Data_in/ENUNU/" + sys.argv[1] + ".xml",
                "./bin/Utau2sinsy/xml_out/" + sys.argv[1] + ".xml")


# ラベル生成フェーズ
class make_labels:
    def make(self):  # クラス総合
        shutil.rmtree("./bin/Julius/wav/")
        os.mkdir("./bin/Julius/wav/")
        print("楽譜の読み込み中...\n")
        self.julius_make_lab()
        self.check_input()
        self.sinsy_make_lab()

    def check_input(self):  # 入力ファイル形式とSinsy音素辞書の確認
        assert sinsy.setLanguages("j", pysinsy.get_default_dic_dir())
        assert sinsy.loadScoreFromMusicXML(input_xml)

    def sinsy_make_lab(self):  # Sinsyラベルを生成
        is_mono = True
        print("Sinsyラベル生成中...\n")

        labels = sinsy.createLabelData(is_mono, 1, 1).getData()
        with open(temp_Slab, "w") as f:
            for l in labels:
                f.write(str(l) + "\n")

    def julius_make_lab(self):  # Juliusラベルを生成
        y, sr = librosa.core.load(input_audio, sr=16000, mono=True)  # ダウンサンプリング
        sf.write(temp_audio, y, sr, subtype="PCM_16")  # Julius用ダウンサンプリングを保存

        with wave.open(input_audio, 'rb') as wr:
            fr = wr.getframerate()

        if input_sr_mode == "enunu":
            y, sr = librosa.core.load(input_audio, sr=44100, mono=True)
            sf.write(down_audio, y, sr, subtype="PCM_16")  # 44.1kHzダウンサンプリングを保存

        self.read_XML()

        print("Julius ラベル生成中...")
        subprocess.run(["perl", "./segment_julius.pl"], cwd="./bin/Julius")
        shutil.move(raw_Jlab, temp_Jlab)
        shutil.copy(log_file, log_dir)

    def read_XML(self):  # 楽譜ファイル読み込み&歌詞取り込み          

        if input_sr_mode == "enunu":
            with open(input_xml, mode="rt", encoding="iso-8859-1") as f:
                xml_string = f.read()

            root = ET.fromstring(xml_string)
            code = ET.tostring(
                root, encoding="iso-8859-1").decode("utf-8").replace('iso-8859-1', 'utf-8')
            os.remove("./bin/Utau2sinsy/xml_out/" + sys.argv[1] + ".xml")

            with open(input_xml, mode="w", encoding="utf-8") as f:
                f.write(code)

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
                if time == str("16th") or time == str("quarter") or time == str("eighth") or time == str(
                        "half") or time == str("halfD"):
                    if len(lyrics) != 0:
                        lyrics.append(" sp ")
                if time == str("whole"):
                    lyrics.append(" sps ")
                if _.find("duration").text == str("16") and _.find('type') is not None:
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

        # デバッグ用
        # print('Lyrics : ' + ','.join(lyrics))

        if lyrics[len(lyrics) - 1] == " sps " and lyrics[len(lyrics) - 2] == " sp ":
            lyrics.pop(-1)

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
        print("ラベル結合中...")
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

        with open(temp_JlabC, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                split = line.split(' ')
                Jstart_time.append(split[0])
                Jend_time.append(split[1])
                Jphoneme.append(split[2])

        for i in range(0, len(Sphoneme)):  # JuliusとSinsyの音素ラベルの対応を取りながら置き換え
            # デバッグ
            # print(i)
            # print(Sphoneme[i] + Jphoneme[j])

            if Sphoneme[i] == "sil\n" and Jphoneme[j] == "silB\n" or \
                    Sphoneme[i] == "sil\n" and Jphoneme[j] == "sp\n":  # 無音ラベル（開始）
                final.append(str(Sstart_time[i]) + " " + str(Send_time[i]) + " " + Sphoneme[i])
                j = j + 1
            elif Sphoneme[i] == "pau\n" and Sphoneme[i - 1] == "sil\n" and Jphoneme == "silB\n" or \
                    Sphoneme[i] == "pau\n" and Sphoneme[i - 1] == "sil\n" and Jphoneme == "sp\n":  # 無音ラベル（開始連続）
                final.append(str(Send_time[i - 1]) + " " + str(Jend_time[j]) + " " + Sphoneme[i])
                j = j + 1
            elif Sphoneme[i] == Jphoneme[j] or \
                    Sphoneme[i] == "a\n" and Jphoneme[j] == "a:\n" or \
                    Sphoneme[i] == "i\n" and Jphoneme[j] == "i:\n" or \
                    Sphoneme[i] == "u\n" and Jphoneme[j] == "u:\n" or \
                    Sphoneme[i] == "e\n" and Jphoneme[j] == "e:\n" or \
                    Sphoneme[i] == "o\n" and Jphoneme[j] == "o:\n" or \
                    Sphoneme[i] == "cl\n" and Jphoneme[j] == "q\n" or \
                    Sphoneme[i] == "pau\n" and Jphoneme[j] == "sp\n" or \
                    Sphoneme[i] == "pau\n" and Jphoneme[j] == "silB\n" or \
                    Sphoneme[i] == "pau\n" and Jphoneme[j] == "silE\n":  # 単純置き換え
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
                    final[i - 1] = Jstart_time[j - 1] + " " + Sstart_time[i] + " " + Sphoneme[i - 1]
                    final.append(Sstart_time[i] + " " + end + " " + Sphoneme[i])
                else:
                    final[i - 1] = Jstart_time[j - 1] + " " + str(start) + " " + Sphoneme[i - 1]
                    final.append(str(start) + " " + end + " " + Sphoneme[i])
            elif i == len(Sphoneme) - 1:
                if Sphoneme[i] == "sil\n" and Sphoneme[i - 1] == "sil\n":  # 1小節以上の無音
                    final.append(str(Sstart_time[i]) + " " + str(Send_time[i]) + " " + Sphoneme[i])
                elif Sphoneme[i] == "sil\n" and Sphoneme[i - 1] == "pau\n" and \
                        Jphoneme[j] == "silE\n" and Jphoneme[j - 1] == "sp\n":  # 2拍以上の無音
                    final.append(str(Jend_time[j - 1]) + " " + str(Send_time[i]) + " " + Sphoneme[i])
                elif Sphoneme[i] == "pau\n" and Sphoneme[i - 1] == "pau\n":  # 2拍以上の無音
                    final.append(str(Jend_time[i]) + " " + str(Send_time[i]) + " " + Sphoneme[i])
                elif Sphoneme[i] == "pau\n" and Sphoneme[i + 1] != "pau\n":  # 1拍の無音
                    final.append(str(Send_time[i - 1]) + " " + str(Jstart_time[j]) + " " + Sphoneme[i])
            elif i != 0:
                if Sphoneme[i] == "pau\n" and Sphoneme[i - 1] == "sil\n" and Jphoneme[j] == "silB\n":
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
                                                  "ラベル位置：[{0}]".format(i)
            if i != 0:
                if Cstart_time[i] != Cend_time[i - 1]:
                    shutil.move(output_filename, error_lab)
                assert Cstart_time[i] == Cend_time[i - 1], "ERROR：一つ前の音素の終了時間と現在の音素の開始時間が不一致です\n" \
                                                           "ラベル位置：[{0}]".format(i)

        print("完了!!")


make = make_labels()
make.make()

merge = merge_labels()
merge.merge()
