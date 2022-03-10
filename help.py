# coding: UTF-8
# v0.0.2 (2022/03/12)

print("\n*****************************\n" +
      "Vocal2lab v0.0.2 (2022/03/12)" +
      "\n*****************************\n" +
      " 本ツールはNNSVS、ENUNU向けの歌声DB制作支援ツールです\n" + \
      "音声(.wav)と楽譜(.musicxml/.xml/.ust)の入力で音素ラベリングを自動的に行います\n\n" + \
      "・入力は./Data_in/[NNSVS or ENUNU]に入れてください\n" + \
      "・実行は必ずモード指定(NNSVS or ENUNU)してください\n")

print("\n・一つだけラベリングを実行\n" + \
      "     python ./Vocal2lab.py [入力ファイル名] [出力ファイル名] [nnsvs or enunu]\n" + \
      "     結果は./Data_out/にラベルだけ保存されます\n")

print("\n・一括ラベリングを実行\n" + \
      "     python ./Vocal2lab.py --multi [nnsvs or enunu]\n" + \
      "     結果は./Data_out/に日付フォルダの歌声DB形式で保存されます\n")

print("\n・一時キャッシュを消去\n" +
      "     python ./Vocal2lab.py --cash_clear\n" +
      "     キャッシュ済みラベルデータ と ダウンサンプリング音声 を消去します\n" +
      "     (./Data_in/に無いファイルがリストに出てエラーが起きる場合使用してください)\n")

print("\n・コマンド確認\n" + \
      "     python ./Vocal2lab.py --help" + \
      "\n")
