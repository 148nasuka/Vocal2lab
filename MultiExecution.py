"""
./in フォルダ内のモノすべてに対してラベル生成したい場合はこちらのスクリプトを動かして下さい。
※管理者権限でないと動かない場合があります

使い方 :
python ./MultiExecution.py [モード(mono / full)]

"""

import subprocess
import sys
import os

counter = 1
input_dir = "./in/"
input_files = []
mode = sys.argv[1]
error = 0

for file_name in os.listdir(input_dir):
    file_path = os.path.join(input_dir, file_name)
    if os.path.isfile(file_path):
        if counter % 2 == 0:
            input_files.append(file_name.split(".")[0])
        counter += 1
print(input_files)

for i in range(0, len(input_files)):
    print("\n**************************\n" + \
          "Progress " + str(i + 1) + " / " + str(len(input_files)) + \
          "\n**************************\n")
    try:
        subprocess.check_output(["python", "./Vocal2lab.py", input_files[i], input_files[i], mode], cwd="./")
    except subprocess.CalledProcessError as e:
        error += 1
        print("\n**************************\n" + \
              "           ERROR!! " + \
              "\n**************************\n")

print("\n**************************\n" + \
      "Complete !! \n" + \
      "ERROR : " + str(error) + " / " + str(len(input_files)) + \
      "\n**************************\n")
