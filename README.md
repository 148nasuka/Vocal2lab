# Vocal2lab

<p><a href="https://github.com/r9y9/nnsvs">NNSVS</a>および<a href="https://github.com/oatsu-gh/enunu_training_kit">ENUNU Training Kit </a>向けの教師データ作成を支援する自動ラベリングツールです。<br>
使用方法はそれぞれ<br>
    <li>アーティスト向けチュートリアル(ENUNU).pdf ※準備中</li>
    <li>研究者向けチュートリアル(NNSVS).pdf</li>
    <p>をつけていますのでそちらを参照してください。
</p><br>

<h1>動作環境</h1>

<p>動作には以下の環境が必要になります。</p>

<li>Windows</li>

<li><a href = "https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe">Python3.8 </a></li>

<li><a href = "https://strawberryperl.com/">Perl</a></li>

<h1>使い方</h1>

<b><p>留意事項</b></p>

<p>Vocal2labは ./Vocal2lab/Data_in/[モード名]/ 内のファイルに対してラベリングを行うことができます。<br>
入力ファイル名は楽譜、音声共に同じ名前にして下さい。</p>
<b>入力形式</b><br>
NNSVSモードの場合、楽譜データ（.xml / .musicxml）音声データ（.wav ※モノラル ）です。<br>
ENUNUモードの場合、楽譜データ（.ust）音声データ（.wav ※モノラル）
出力形式は .lab（ラベル）です。</p><br>

<b>現状、下記の要素を含む入力は正しくラベリング出来ません。</p></b>

<li>46秒以上の音声（46秒以上でもラベリング可能ですが、精度が非常に低いです）</li>

<li>音割れしている音声</li>

<li>捨て仮名表記の発音が記入された楽譜<br>

　（小文字「ぁ,ぃ,ぅ,ぇ,ぉ」で表現される発音）</li>

<li>息継ぎ記号を含んだ楽譜</li>

<h2>1. セットアップ</h2>

<p>※本ツールはCUIプログラムとなっています。<br>
尚、venv等の仮想環境では正しく動作しない可能性があります。</p>

<b><p>初回実行時のみ、管理者権限のターミナルで ./Vocal2lab/setup/ を開き、下記のコマンドを入力してください。<br>（必須PythonライブラリとSinsy音素辞書のインストールを自動で行います。）</p></b>

    python ./setup.py

<h2>2. 実行方法</h2>

<p><b>一つだけラベリングを実行する場合。</b><br>
    
    python ./Vocal2lab.py [入力ファイル名]　[出力ファイル名] [モード(nnsvs / enunu)]

<b>（ラベルデータは ./Data_out/　にラベル単体で保存されます。）</strong><br><br></p>

<p><strong>一括ラベリングを実行する場合。(NNSVS)</strong><br>
    
    python ./Vocal2lab.py --multi nnsvs
</p>

<p><strong>一括ラベリングを実行する場合。(ENUNU)</strong><br>
    
    python ./Vocal2lab.py --multi enunu

<b>（ラベルデータは ./Data_out/[実行日時]/　に楽譜、音声、ラベルのセットで保存されます。）</b><br><br></p>

<p><b>コマンドリストを確認する場合。</b><br>
    
    python ./Vocal2lab.py --help
</p><br>

<h2>3. ラベルの確認＆修正</h2>

<p>出力ラベルは<a href="https://www.speech.kth.se/wavesurfer/man.html">WaveSurfer</a>で精度の確認と編集ができます。</p>

<img src="./bin/Github_img/WaveSurfer.jpg" alt="WaveSurfer" title="WaveSurfer">

<h1>Vocal2labの構成（開発者向け）</h1>

<p>このツールは<a href="https://github.com/julius-speech/segmentation-kit">Julius segmentation-kit</a> を利用して音素ラベリングを実行しています。<br>

尚、構成は以下の図のようになっています。</p>

<img src="./bin/Github_img/Vocal2lab.jpg" alt="Vocal2lab" title="Vocal2lab">

<h1>更新履歴</h1>
<b><p>v0.0.1</b></p>
<li>初回公開</li>
<li>NNSVS用教師データラベリングにのみ対応</li>

<b><p>v0.0.2</b></p>
<li>ENUNU用教師データラベリングに対応</li>
<li>NNSVSモードの.xml形式入力に対応</li>
<li>音声の最大入力長を45秒に拡張</li>
<li>音声認識エンジンをアップデート（Julius-4.3.1 → Juliusu-4.5）</li>
