import os
import shutil

print("\n************************************************\n" + \
      "Vocal2labに必要なライブラリをインストールします" + \
      "\n************************************************\n")

os.system('pip install -r requirements.txt')

print("\n**********************************************\n" + \
      "pysinsy 音素辞書ファイルの確認をします"
      "\n**********************************************\n")

import pysinsy

sinsy_location = str(pysinsy.__file__)
dic_location = sinsy_location.replace("__init__.py", "_dic")
copy_location = "./Sinsy_dic"

if os.path.exists(dic_location):
    print("pysinsy インストール先 : " + dic_location)
    if os.path.isfile(dic_location + "\japanese.euc_jp.conf"):
        print("japanese.euc_jp.conf : check")
    else:
        shutil.copy(copy_location + "\japanese.euc_jp.conf", dic_location + "\japanese.euc_jp.conf")
        print("japanese.euc_jp.conf : set")

    if os.path.isfile(dic_location + "\japanese.euc_jp.table"):
        print("japanese.euc_jp.table : check")
    else:
        shutil.copy(copy_location + "\japanese.euc_jp.table", dic_location + "\japanese.euc_jp.table")
        print("japanese.euc_jp.table : set")

    if os.path.isfile(dic_location + "\japanese.macron"):
        print("japanese.macron : check")
    else:
        shutil.copy(copy_location + "\japanese.macron", dic_location + "\japanese.macron")
        print("japanese.macron : set")

    if os.path.isfile(dic_location + "\japanese.shift_jis.conf"):
        print("japanese.shift_jis.conf : check")
    else:
        shutil.copy(copy_location + "\japanese.shift_jis.conf", dic_location + "\japanese.shift_jis.conf")
        print("japanese.shift_jis.conf : set")

    if os.path.isfile(dic_location + "\japanese.shift_jis.table"):
        print("japanese.shift_jis.table : check")
    else:
        shutil.copy(copy_location + "\japanese.shift_jis.table", dic_location + "\japanese.shift_jis.table")
        print("japanese.shift_jis.table : set")

    if os.path.isfile(dic_location + "\japanese.utf_8.conf"):
        print("japanese.utf_8.conf : check")
    else:
        shutil.copy(copy_location + "\japanese.utf_8.conf", dic_location + "\japanese.utf_8.conf")
        print("japanese.utf_8.conf : set")

    if os.path.isfile(dic_location + "\japanese.utf_8.table"):
        print("japanese.utf_8.table : check")
    else:
        shutil.copy(copy_location + "\japanese.utf_8.table", dic_location + "\japanese.utf_8.table")
        print("japanese.utf_8.table : set")
else:
    print("pysinsy のインストールに失敗している可能性があります\nライブラリの再インストールをしてください")

print("\n*****************\n" + \
      "インストール完了"
      "\n*****************\n")
