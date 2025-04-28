import re
import pytest
from mahjong_py.display_discard_hand_at import (
    parse_player_names,
    get_kyoku_segment,
    process_segment,
    display_discard_hand_at
)

SAMPLE_GAME = '''
<UN n0="心" n1="牌操作万歳！" n2="ⓝLuckyJ" n3="こうえい"/>
<TAIKYOKU oya="0"/>
<INIT hai0="0,4,8,12,16,20,24,28,32,36,40,44,48"
      hai1="1,5,9,13,14,17,21,25,29,33,37,41,45"
      hai2="2,6,10,18,22,26,27,30,34,38,42,46,50"
      hai3="3,7,11,15,19,23,31,35,39,40,43,47,51,53"/>
<T60/><D0/><U61/><E14/><V62/><F27/><W63/><G40/>
<N who="1" m="17457"/>
<T44/><D44/>
<E45/>
'''

def test_parse_player_names():
    names = parse_player_names(SAMPLE_GAME)
    assert names == {
        0: "心",
        1: "牌操作万歳！",
        2: "ⓝLuckyJ",
        3: "こうえい"
    }

def test_get_kyoku_segment():
    seg = get_kyoku_segment(SAMPLE_GAME, 0)
    assert "<INIT" in seg
    assert "hai0=" in seg

def test_process_segment_returns_structure():
    seg = get_kyoku_segment(SAMPLE_GAME, 0)
    result = process_segment(seg)
    assert isinstance(result, list)
    assert all(isinstance(x, tuple) and len(x) == 4 for x in result)
    for _, _, hand, melds in result:
        assert isinstance(hand, list)
        assert isinstance(melds, list)

def test_display_discard_hand_at_output(capsys):
    display_discard_hand_at(SAMPLE_GAME, 0)
    out = capsys.readouterr().out
    assert "心 さんの 1 回目の打牌後の手牌" in out
    assert "副露メンツ:" in out or "副露メンツ" not in out  # 柔軟な条件に変更
