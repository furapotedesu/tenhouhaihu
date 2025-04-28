import pytest
from mahjong_py.display_call import display_calls_fixed

def test_display_calls_invalid_input(capsys):
    # 無効な文字列を渡してもクラッシュせずヘッダーのみ表示されること
    display_calls_fixed("invalid input", game_index=1)
    captured = capsys.readouterr()
    assert "Game 1 鳴き情報" in captured.out

def test_display_calls_no_call(capsys):
    # 有効なINITのみで鳴きイベントがないケース
    kyoku_str = '<mjloggm><INIT hai0="0" hai1="4" hai2="8" hai3="12"/></mjloggm>'
    display_calls_fixed(kyoku_str, game_index=2)
    captured = capsys.readouterr()
    # ヘッダーは出力されるが、ツモ数や鳴き情報は出力されない
    assert "Game 2 鳴き情報" in captured.out
    assert "ツモ数" not in captured.out
    assert "鳴き内容" not in captured.out
