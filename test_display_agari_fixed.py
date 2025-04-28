import pytest
from mahjong_py.display_agari_fixed import display_agari_details

def test_display_agari_header_only_for_invalid(capsys):
    # 不正な入力でもヘッダーが表示され、クラッシュしないことをテスト
    display_agari_details("invalid input", game_index=1)
    captured = capsys.readouterr()
    assert "── Game 1 和了詳細 ──" in captured.out

def test_display_agari_no_agari_tag(capsys):
    # INITタグはあるがAGARIタグなしのケース
    kyoku_str = '<mjloggm><INIT hai0="0" hai1="4" hai2="8" hai3="12"/></mjloggm>'
    display_agari_details(kyoku_str, game_index=2)
    captured = capsys.readouterr()
    # ヘッダーは常に出力
    assert "── Game 2 和了詳細 ──" in captured.out
    # AGARI情報がないため役や得点出力はない
    assert "役:" not in captured.out
    assert "得点:" not in captured.out
