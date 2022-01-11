"""
./in フォルダ内のモノすべてに対してラベル生成したい場合はこちらのスクリプトを動かして下さい。
※管理者権限でないと動かない場合があります

使い方 :
python ./MultiExecution.py [モード(mono / full)] [サンプリングレート(48000 / 96000)]

"""
import datetime
import shutil
import subprocess
import sys
import os

counter = 1
input_dir = "./in/"
out_dir = "./out/"
input_files = []
mode = sys.argv[1]
input_sr_mode = sys.argv[2]
position = []
error = 0


dt_now = datetime.datetime.now()
output_dir = "./out/" + dt_now.strftime('%Y-%m-%d_%H-%M-%S')
os.mkdir(output_dir)

if len(sys.argv) != 3:
    sys.exit("xml2lab.py [mode] [sampling rate]")

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
        position.append(i + 1)
        error += 1
        print("\n**************************\n" + \
              "           ERROR!! " + \
              "\n**************************\n")

print("\n**************************\n" + \
      "Labeling completed !! \n" + \
      "ERROR : " + str(error) + " / " + str(len(input_files)) + "\n" + \
      "ERROR list (index) : " + str(position) + \
      "\n**************************\n")

i = 1

for file_name in os.listdir(out_dir):
    file_path = os.path.join(out_dir, file_name)
    if os.path.isfile(file_path):
        print("Creating dataset : " + file_name)
        os.mkdir(output_dir + "/" + file_name.split(".")[0])
        shutil.move("./out/" + file_name, output_dir + "/" + file_name.split(".")[0])
        if input_sr_mode == 48000:
            shutil.copy("./in/" + file_name.split(".")[0] + ".wav", output_dir + "/" + file_name.split(".")[0])
        else:
            shutil.copy("./downscaling/" + file_name.split(".")[0] + ".wav", output_dir + "/" + file_name.split(".")[0])
        shutil.copy("./in/" + file_name.split(".")[0] + ".musicxml", output_dir + "/" + file_name.split(".")[0])
        i += 1

print("\n**************************\n" + \
      "Done !! " + \
      "\n**************************\n")


