print("\nVocal2lab\n" + \
      " ./in/ に楽譜&音声ファイルを入れることで自動的にラベリングできます\n" + \
      "(楽譜&音声ファイルは同じ名前で保存してください)\n" + \
      "ラベルは ./data_out/ に出力されます" + \
      "\n")

print("\n一つだけラベリングを実行\n" + \
      "python ./Vocal2lab.py [入力ファイル名] [出力ファイル名]" + \
      "\n")

print("\n一括ラベリングを実行\n" + \
      "python ./Vocal2lab.py --multi" + \
      "\n(オプション)出力サンプリングレートを48kHz部揃える場合\n" + \
      "python ./Vocal2lab.py --multi ds" + \
      "\n")

print("\nコマンド確認\n" + \
      "python ./Vocal2lab.py --help" + \
      "\n\n")
