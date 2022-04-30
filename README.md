# Vocal2lab

<p><a href="https://github.com/r9y9/nnsvs">NNSVS</a>および<a href="https://github.com/oatsu-gh/enunu_training_kit">ENUNU Training Kit </a>向けの教師データ作成を支援する自動ラベリングツールです。
</p>

<h1>動作環境</h1>

<p>動作には以下の環境が必要になります。</p>

<li>Windows</li>

<li>C++コンパイル環境（VisualStudio C++）</li>

<li><a href = "https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe">Python3.8 </a></li>

<li><a href = "https://strawberryperl.com/">Perl</a></li>


<h1>使い方</h1>
<h2>1. セットアップ</h2>
<p>./Vocal2lab/Setup/内のSetup.batを実行してください。</p>


<h2><p>2. データの準備</h2>

<p>Vocal2labは ./Vocal2lab/Data_in/[モード名]/ 内のファイルに対してラベリングを行うことができます。<br>
入力ファイル名は楽譜、音声共に同じ名前にして下さい。</p>
<b>入力形式</b><br>
NNSVSモード：楽譜データ（.xml / .musicxml）音声データ（.wav ※モノラル ）です。<br>
ENUNUモード：楽譜データ（.ust）音声データ（.wav ※モノラル）
出力形式は .lab（ラベル）です。</p><br>

<b>現状、下記の要素を含む入力は正しくラベリング出来ません。</p></b>

<li>46秒以上の音声（46秒以上でもラベリングされますが、精度が非常に低いです）</li>

<li>音割れしている音声</li>

<li>母音を省略して発音している音声</li>

<li>捨て仮名表記の発音が記入された楽譜<br>

　（小文字「ぁ,ぃ,ぅ,ぇ,ぉ」で表現される発音）</li>

<li>息継ぎ記号を含んだ楽譜</li>

<li>ファイル名に日本語を含む場合</li>



<h2>3. 実行</h2>
<p><b>ENUNU用に一括ラベリングを実行する場合。</b><br>
    Vocal2lab-ENUNU.batを実行</p>

<p><strong>NNSVS用に一括ラベリングを実行する場合。</strong><br>
    Vocal2lab-NNSVS.batを実行</p>
</p>


<h2>4. ラベルの確認＆修正</h2>

<p>出力ラベルは./Vocal2lab/Data_out/日付(動作モード)/にENUNUまたはNNSVSへそのまま使える形のディレクトリ構造で保存されます。<br>また、<a href="https://www.speech.kth.se/wavesurfer/man.html">WaveSurfer</a>でラベル精度の確認と編集ができます。</p>

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
<li>音声認識エンジンをアップデート（Julius-4.3.1 → Juliusu-4.5）</li>
<li>音声の最大入力長を20秒から45秒に拡張</li>
<li>コマンド不要で動作するようにbatch fileを追加</li>
