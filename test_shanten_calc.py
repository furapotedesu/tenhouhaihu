import pytest
from mahjong_py.shanten_calc import calculate_shanten

def test_no_melds_tenpai():
    hand = ['一萬','二萬','三萬','4筒','5筒','6筒','7索','8索','9索','東','東','白','白']
    result = calculate_shanten(hand, melds_count=0)
    assert result['通常'] == 0

def test_chiitoitsu_basic():
    # 対子が1つ → 6 - 1 = 5 シャンテン
    hand = [
        '一萬','一萬',  # 対子１つ
        '二萬','三萬','四萬','五萬','六萬','七萬','八萬','九萬',  # 8種ユニーク
        '1筒','2筒','3筒','4筒'  # 4種ユニークで計14枚
    ]
    result = calculate_shanten(hand, melds_count=0)
    assert result['七対子'] == 5
