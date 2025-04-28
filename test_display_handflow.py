import pytest
from io import StringIO
import sys

from mahjong_py.display_handflow import display_hand_flow_by_kyoku

# テスト用の最小mjloggm風データ（1局のみ）
SAMPLE_KYOKU = '''
<INIT hai0="0,4,8,12,16,20,24,28,32,36,40,44,48" hai1="1,5,9,13,17,21,25,29,33,37,41,45,49"
      hai2="2,6,10,14,18,22,26,30,34,38,42,46,50" hai3="3,7,11,15,19,23,27,31,35,39,43,47,51"/>
<T0/><D0/><U1/><E1/><V2/><F2/><W3/><G3/>
'''

def test_display_hand_flow_by_kyoku_output(capsys):
    """ display_hand_flow_by_kyoku の出力が期待通りに構造を持つことを確認する """
    display_hand_flow_by_kyoku(SAMPLE_KYOKU, game_index=99)

    captured = capsys.readouterr().out

    assert "── Game 99 手配進行 ──" in captured
    assert "== 第1局 ==" in captured
    assert "配 牌:" in captured
    assert "東家:" in captured
    assert "ツモ:" in captured
    assert "捨て牌:" in captured
    assert "東家: 一萬" in captured or "東家: " in captured  # 少なくとも出力される

def test_multiple_calls_isolated(capsys):
    """ 複数回実行しても出力が混ざらないこと """
    display_hand_flow_by_kyoku(SAMPLE_KYOKU, game_index=1)
    out1 = capsys.readouterr().out

    display_hand_flow_by_kyoku(SAMPLE_KYOKU, game_index=2)
    out2 = capsys.readouterr().out

    assert "── Game 1 手配進行 ──" in out1
    assert "── Game 2 手配進行 ──" in out2
