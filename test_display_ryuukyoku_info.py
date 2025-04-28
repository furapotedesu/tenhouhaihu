# tests/test_display_ryuukyoku_info.py

import pytest
from mahjong_py.display_ryuukyoku import display_ryuukyoku_info

@pytest.mark.parametrize("kyoku_str, game_index, expected", [
    # 1) 無効入力 → ヘッダーのみ
    ("invalid input", 1, [
        "── Game 1 流局情報 ──"
    ]),
    # 2) INITのみ → ヘッダーのみ
    ('<mjloggm><INIT /></mjloggm>', 2, [
        "── Game 2 流局情報 ──"
    ]),
    # 3) INIT + sc属性のみ → 局情報 + 点数変動
    ('<mjloggm><INIT hai0=""/><RYUUKYOKU sc="100"/></mjloggm>', 3, [
        "── Game 3 流局情報 ──",
        "Game 3 第1局",
        "   点数変動 (sc): 100"
    ]),
    # 4) INIT + sc=0 + 公開手牌 → 局情報 + 点数変動 + 公開手牌
    ('<mjloggm><INIT hai0=""/><RYUUKYOKU sc="0" hai0="0,16"/></mjloggm>', 4, [
        "── Game 4 流局情報 ──",
        "Game 4 第1局",
        "   点数変動 (sc): 0",
        "   東家の公開手牌: 一萬 赤五萬"
    ]),
])
def test_display_ryuukyoku_info(kyoku_str, game_index, expected, capsys):
    display_ryuukyoku_info(kyoku_str, game_index)
    out_lines = capsys.readouterr().out.splitlines()
    # 空行を除去
    lines = [l for l in out_lines if l.strip()]
    assert lines == expected
