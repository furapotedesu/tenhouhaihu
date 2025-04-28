import pytest
from mahjong_py.display_dora_fixed import display_dora_fixed

def test_display_dora_invalid_input(capsys):
    # 無効な文字列でもクラッシュせずヘッダーのみ表示されること
    display_dora_fixed("invalid input", game_index=1)
    captured = capsys.readouterr()
    assert "── Game 1 ドラ表示牌 ──" in captured.out

def test_display_dora_no_dora(capsys):
    # INIT タグはあるが seed がなく DORA タグもないケース
    kyoku_str = '<mjloggm><INIT /></mjloggm>'
    display_dora_fixed(kyoku_str, game_index=2)
    captured = capsys.readouterr()
    assert "第1局: [WARNING] ドラ表示牌なし" in captured.out

def test_display_dora_basic(capsys):
    # seed にドラ表示牌があるケース (6番目の値が 16 と仮定)
    init = '<INIT seed="0,0,0,0,0,16" />'
    kyoku_str = f'<mjloggm>{init}</mjloggm>'
    display_dora_fixed(kyoku_str, game_index=3)
    captured = capsys.readouterr()
    assert "第1局: 赤五萬" in captured.out

def test_display_dora_with_dora_tag(capsys):
    # DORA タグによる追加ドラ牌の検出
    # 16→赤五萬, 20→六萬, 24→七萬
    kyoku_str = '<mjloggm><INIT seed=",,,,,16"/><DORA hai="20"/><DORA hai=\'24\'/></mjloggm>'
    display_dora_fixed(kyoku_str, game_index=4)
    captured = capsys.readouterr()
    assert "第1局: 赤五萬 六萬 七萬" in captured.out
