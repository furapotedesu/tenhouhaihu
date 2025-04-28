import pytest
from mahjong_py.converters import convert_tile_list, convert_tile_id_to_str, convert_yaku_id_to_name

def test_convert_tile_list_empty():
    assert convert_tile_list("") == []

def test_convert_tile_list_basic():
    # 136-ID の 0 は base=0 -> "一萬"
    assert convert_tile_list("0") == ["一萬"]
    # 136-ID の 4,8,12 は base=1,2,3 -> "二萬","三萬","四萬"
    assert convert_tile_list("4,8,12") == ["二萬", "三萬", "四萬"]

def test_convert_tile_list_red():
    # 赤ドラID の 16 -> base=4 -> "五萬", 赤ドラなので "赤五萬"
    assert convert_tile_list("16") == ["赤五萬"]

def test_convert_tile_id_to_str():
    assert convert_tile_id_to_str(0) == "一萬"
    # 赤ドラ
    assert convert_tile_id_to_str(16) == "赤五萬"

def test_convert_yaku_id_to_name_known():
    names = convert_yaku_id_to_name([0, 7, 47])
    assert "門前清自摸和" in names
    assert "平和" in names
    assert "国士無双" in names

def test_convert_yaku_id_to_name_unknown():
    assert convert_yaku_id_to_name([999]) == ["不明(999)"]
