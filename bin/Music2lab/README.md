# Music2lab

<p><a href="https://github.com/r9y9/nnsvs">NNSVS（Neural network-based singing voice synthesis）</a>の学習済みレシピで任意の曲を歌わせるためのラベルデータを楽譜データ(MusicXML)から生成するスクリプト。</p><br>

<h1>使い方</h1>
<p>1. 楽譜データを /Vocal2lab/Music2lab/xml_in/ に入れる</p>

<p>2. <strong>楽譜ファイルから生成用のラベルデータを生成する</strong><br>
    
    python ./music2lab [入力ファイル名.musicxml] [出力ファイル名.lab] generate
</p>

<p>3. 変換後、 /Vocal2lab/Music2lab/lab_out/ に出力されるラベルデータを<br>NNSVSの生成フェーズで指定する事で任意の曲を歌わせることができる。<br>
例：/nnsvs/egs/_commmon/spsvs/synthesis.sh 44～47行目
    <code>
    
    # 変更前
    # utt_list=./data/list/$s.list \
    # in_dir=data/acoustic/$input/ \
    # out_dir=$expdir/synthesis/$s/${acoustic_eval_checkpoint/.pth/}/$input \
    # ground_truth_duration=$ground_truth_duration 
    
    # 以下に置き換え
    ground_truth_duration=false \
    label_path=~/Download/amehuri.lab \    #楽譜ラベルのパス
    out_wav_path=~/Download/amehuri.wav    #保存先のパス
</code>
