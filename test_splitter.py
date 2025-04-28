import pytest
from mahjong_py.splitter import split_games, split_kyokus

def test_split_games_single_block():
    text = '<mjloggm>content1</mjloggm>'
    assert split_games(text) == ['<mjloggm>content1</mjloggm>']

def test_split_games_multiple_blocks_with_separator():
    separator = '\n' + '='*80 + '\n'
    text = '<mjloggm>game1</mjloggm>' + separator + '<mjloggm>game2</mjloggm>'
    assert split_games(text) == ['<mjloggm>game1</mjloggm>', '<mjloggm>game2</mjloggm>']

def test_split_games_ignores_extra_separators():
    sep = '\n' + '='*80 + '\n'
    text = '<mjloggm>game</mjloggm>' + sep + sep + '<mjloggm>last</mjloggm>'
    assert split_games(text) == ['<mjloggm>game</mjloggm>', '<mjloggm>last</mjloggm>']

def test_split_games_no_blocks():
    assert split_games('no mjloggm here') == []

def test_split_kyokus_basic_usage():
    game = '<INIT a="1"/><DATA/><INIT b="2"/><more/>'
    assert split_kyokus(game) == ['<INIT a="1"/><DATA/>', '<INIT b="2"/><more/>']

def test_split_kyokus_until_end_of_game():
    game = '<INIT a="x"/>foo</mjloggm>'
    assert split_kyokus(game) == ['<INIT a="x"/>foo']

def test_split_kyokus_no_init_tags():
    assert split_kyokus('<mjloggm>no init here</mjloggm>') == []