import pytest
from mahjong_py.parser import parse_init_hand, parse_draws_and_discards

def test_parse_init_hand_valid():
    # INITタグと各種ドローツモ/打牌を含む基本ケース
    kyoku_str = (
        '<mjloggm>'
        '<INIT hai0="1,2,3" hai1="" hai2="4,5" hai3=""/>'
        '<T6/>'   # 東家ツモ
        '<U7/>'   # 南家ツモ
        '<V8/>'   # 西家ツモ
        '<W9/>'   # 北家ツモ
        '<D10/>'  # 東家打牌
        '</mjloggm>'
    )
    hands, tsumos, discards = parse_init_hand(kyoku_str)
    assert hands == [[1, 2, 3], [], [4, 5], []]
    assert tsumos == [[6], [7], [8], [9]]
    assert discards == [[10], [], [], []]

def test_parse_init_hand_no_init():
    # INITタグがない場合はValueErrorをスロー
    with pytest.raises(ValueError):
        parse_init_hand('<mjloggm></mjloggm>')

def test_parse_draws_and_discards_basic():
    # 各プレイヤーのツモ・打牌タグを含む基本ケース
    kyoku = (
        '<mjloggm>'
        '<T10/>' '<U11>' '<V12/>' '<W13>'  # ツモ
        '<D14/>' '<E15>' '<F16/>' '<G17>'  # 打牌
        '</mjloggm>'
    )
    tsumos, discards = parse_draws_and_discards(kyoku)
    assert tsumos == {0: [10], 1: [11], 2: [12], 3: [13]}
    assert discards == {0: [14], 1: [15], 2: [16], 3: [17]}

def test_parse_draws_and_discards_no_tags():
    # ツモ・打牌タグがない場合は空リスト
    kyoku = '<mjloggm><INIT/></mjloggm>'
    tsumos, discards = parse_draws_and_discards(kyoku)
    assert tsumos == {0: [], 1: [], 2: [], 3: []}
    assert discards == {0: [], 1: [], 2: [], 3: []}
