# coding: UTF-8
# v0.0.2 (2022/03/12)

import datetime
import shutil
import subprocess
import sys
import os

if len(sys.argv) != 2:
    sys.exit("ERROR : ラベル生成は以下のような入力になります\nMultiExecution.py [mode(nnsvs or enunu)]")

input_sr_mode = sys.argv[1]
if input_sr_mode == "nnsvs":
    input_dir = "./Data_in/NNSVS/"
elif input_sr_mode == "enunu":
    input_dir = "./Data_in/ENUNU/"
counter = 1
out_dir = "./Data_out/"
input_files = []
error_list = []
error = 0

dt_now = datetime.datetime.now()
if input_sr_mode == "nnsvs":
    output_dir = "./Data_out/" + dt_now.strftime('%Y-%m-%d_%H-%M-%S(NNSVS)')
elif input_sr_mode == "enunu":
    output_dir = "./Data_out/" + dt_now.strftime('%Y-%m-%d_%H-%M-%S(ENUNU)')
else:
    sys.exit("ERROR :正しい入力オプションを指定してください (nnsvs or enunu)")

os.mkdir(output_dir)

for file_name in os.listdir(input_dir):
    file_path = os.path.join(input_dir, file_name)
    if os.path.isfile(file_path):
        if counter % 2 == 0:
            input_files.append(file_name.split(".")[0])
        counter += 1

if counter == 1:
    sys.exit("ERROR : ./Data_in/ ディレクトリに楽譜と音声ファイルを置いてください")
print(input_files)

for i in range(0, len(input_files)):
    print("\n**************************\n" + \
          "進捗 " + str(i + 1) + " / " + str(len(input_files)) + " (" + str(input_files[i]) + ")" + \
          "\n**************************\n")
    try:
        subprocess.check_output(
            ["python", "./Vocal2lab.py", input_files[i], input_files[i], input_sr_mode], cwd="./")
    except subprocess.CalledProcessError as e:
        error_list.append(str(input_files[i]))
        error += 1
        print("\n**************************\n" + \
              "           ERROR!! " + \
              "\n**************************\n")

print("\n**************************\n" + \
      "ラベリング完了 !! \n" + \
      "ERROR : " + str(error) + " / " + str(len(input_files)) + "\n" + \
      "ERROR リスト : " + str(error_list) + \
      "\n**************************\n")

i = 1

for file_name in os.listdir(out_dir):
    file_path = os.path.join(out_dir, file_name)
    if os.path.isfile(file_path):
        print("データセット作成中 : " + file_name)
        os.mkdir(output_dir + "/" + file_name.split(".")[0])
        shutil.move("./Data_out/" + file_name, output_dir + "/" + file_name.split(".")[0])
        if input_sr_mode == "nnsvs":
            shutil.copy("./Data_in/NNSVS/" + file_name.split(".")[0] + ".wav",
                        output_dir + "/" + file_name.split(".")[0])
            if os.path.isfile("./Data_in/NNSVS/" + file_name.split(".")[0] + ".musicxml"):
                shutil.copy("./Data_in/NNSVS/" + file_name.split(".")[0] + ".musicxml",
                            output_dir + "/" + file_name.split(".")[0])
            else:
                shutil.copy("./Data_in/NNSVS/" + file_name.split(".")[0] + ".xml",
                            output_dir + "/" + file_name.split(".")[0] + "/" + file_name.split(".")[0] + ".musicxml")
        elif input_sr_mode == "enunu":
            shutil.copy("./bin/temp/downscaling/" + file_name.split(".")[0] + ".wav",
                        output_dir + "/" + file_name.split(".")[0])
            shutil.copy("./Data_in/ENUNU/" + file_name.split(".")[0] + ".ust",
                        output_dir + "/" + file_name.split(".")[0])
        i += 1

print("\n**************************\n" + \
      "完了 !! " + \
      "\n**************************\n")
