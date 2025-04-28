import pytest
from mahjong_py.analyzer import split_games, decode_mentsu

def test_split_games_single():
    text = "<mjloggm foo"
    result = split_games(text)
    assert isinstance(result, list)
    assert result == ["<mjloggm foo"]

def test_split_games_multiple():
    sep = "=" * 80
    text = "<mjloggm A\n" + sep + "\n<mjloggm B\n"
    result = split_games(text)
    assert len(result) == 2
    assert result[0].startswith("<mjloggm A")
    assert result[1].startswith("<mjloggm B")

@pytest.mark.parametrize("m,expected_type,min_len", [
    (0x0004, "chi", 3),
    (0x0008, "pon", 3),
    (0x0010, "kakan", 4),
    (0x0020, "nuki", 1),
    (0x0000, "ankan", 4),
])
def test_decode_mentsu_types(m, expected_type, min_len):
    tiles, mtype = decode_mentsu(m)
    assert mtype == expected_type
    assert isinstance(tiles, list)
    assert len(tiles) >= min_len
