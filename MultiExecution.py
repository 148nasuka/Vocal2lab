import datetime
import shutil
import subprocess
import sys
import os

if len(sys.argv) != 2:
    sys.exit("ERROR : ラベル生成は以下のような入力になります\nMultiExecution.py [sampling rate(48000 or 96000)]")

counter = 1
input_dir = "./Data_in/"
out_dir = "./Data_out/"
input_files = []
input_sr_mode = sys.argv[1]
error_list = []
error = 0

dt_now = datetime.datetime.now()
output_dir = "./Data_out/" + dt_now.strftime('%Y-%m-%d_%H-%M-%S')
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
          "Progress " + str(i + 1) + " / " + str(len(input_files)) + " (" + str(input_files[i]) + ")" + \
          "\n**************************\n")
    try:
        subprocess.check_output(["python", "./Vocal2lab.py", input_files[i], input_files[i]], cwd="./")
    except subprocess.CalledProcessError as e:
        error_list.append(str(input_files[i]))
        error += 1
        print("\n**************************\n" + \
              "           ERROR!! " + \
              "\n**************************\n")

print("\n**************************\n" + \
      "Labeling completed !! \n" + \
      "ERROR : " + str(error) + " / " + str(len(input_files)) + "\n" + \
      "ERROR list : " + str(error_list) + \
      "\n**************************\n")

i = 1

for file_name in os.listdir(out_dir):
    file_path = os.path.join(out_dir, file_name)
    if os.path.isfile(file_path):
        print("Creating dataset : " + file_name)
        os.mkdir(output_dir + "/" + file_name.split(".")[0])
        shutil.move("./Data_out/" + file_name, output_dir + "/" + file_name.split(".")[0])
        if input_sr_mode == "48000":
            shutil.copy("./Data_in/" + file_name.split(".")[0] + ".wav", output_dir + "/" + file_name.split(".")[0])
        else:
            shutil.copy("./temp/downscaling/" + file_name.split(".")[0] + ".wav",
                        output_dir + "/" + file_name.split(".")[0])
        shutil.copy("./Data_in/" + file_name.split(".")[0] + ".musicxml", output_dir + "/" + file_name.split(".")[0])
        i += 1

print("\n**************************\n" + \
      "Done !! " + \
      "\n**************************\n")
