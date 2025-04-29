# tenhouhaihu

このプログラムは、**Google Colab環境**での実行を前提としています。  
ローカル環境での動作はサポートされていません。

悪意はありませんが素人の初心者が作ったプログラムなので、使用して不利益があっても自己責任で構わないという方のみご利用ください。

## 実行方法（もっと詳細に知りたい人はnote記事を読んでください：https://note.com/comtefurapote/n/nab5d0c44eea9）

1. 以下のリンクから、Google Colabで各ノートブックを開いてください。

### 天鳳牌譜ダウンロード統合
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/furapotedesu/tenhouhaihu/blob/main/tenhoudownload.ipynb)

### 天鳳牌譜解析スタートスニペット
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/furapotedesu/tenhouhaihu/blob/main/tenhou_analysis_start.ipynb)

## 付属のPythonファイルについて

このノートブックでは、以下のファイルを使用しています。

- test_display_ryuukyoku_info.py
- test_init.py
- test_parser.py
- test_shanten_calc.py
- test_splitter.py
- test_analyzer.py
- test_converters.py
- test_display_agari_fixed.py
- test_display_call.py
- test_display_discard_hand_at.py
- test_display_dora_fixed.py
- test_display_handflow.py
- test_display_reach_fixed.py
- utils.py
- analyzer.py
- display_discard_hand_at.py
- display_ryuukyoku.py
- __init__.py
- converters.py
- display_agari_fixed.py
- display_call.py
- display_dora_fixed.py
- display_handflow.py
- display_reach_fixed.py
- mahjong_py.html
- parser.py
- shanten_calc.py
- splitter.py

## 共有設定について

ノートブックはGoogle Drive上で「リンクを知っている全員に閲覧可能」と設定されています。  
リンクをクリックすれば、どなたでも実行できます。

## 注意事項

- 実行にはGoogleアカウントが必要です。
- ローカル環境（PC単体）での動作サポートは行っていません。

## ライセンス

このプロジェクトのコードはパブリックドメインとして公開されています。  
自由に利用・改変・再配布が可能です。

ただし、以下の外部ライブラリを利用していますので、それぞれのライセンスに従ってください。

- **requests**: Apache License 2.0
- **BeautifulSoup (bs4)**: MIT License
- **pytest**: MIT License
- **mahjong**: GNU General Public License v3 or later (GPLv3+)

外部ライブラリのライセンスについては、それぞれの公式ページをご確認ください。
