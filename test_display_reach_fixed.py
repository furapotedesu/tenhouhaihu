# tests/test_display_reach_fixed.py

import pytest
from mahjong_py.display_reach_fixed import display_reach_info_fixed

def test_reach_invalid_xml(capsys):
    display_reach_info_fixed("invalid input", game_index=1)
    captured = capsys.readouterr()
    assert "── Game 1 リーチ情報 ──" in captured.out

def test_reach_no_tags(capsys):
    kyoku_str = '<mjloggm><INIT hai0="0" hai1="4" hai2="8" hai3="12"/></mjloggm>'
    display_reach_info_fixed(kyoku_str, game_index=2)
    captured = capsys.readouterr()
    assert "── Game 2 リーチ情報 ──" in captured.out
    assert "リーチ宣言" not in captured.out

def test_reach_successful(capsys):
    # ───────────── INIT タグ＋REACHタグを含む正しいケース ─────────────
    kyoku_str = (
        '<mjloggm>'
        '<INIT hai0="0" hai1="4" hai2="8" hai3="12"/>'
        '<REACH who="0" step="1"/>'
        '<REACH who="0" step="2"/>'
        '</mjloggm>'
    )
    display_reach_info_fixed(kyoku_str, game_index=3)
    captured = capsys.readouterr()
    out = captured.out
    # ヘッダー
    assert "── Game 3 リーチ情報 ──" in out
    # 局情報
    assert "Game 3 第1局" in out
    # リーチ宣言ログ
    assert "東家がリーチ宣言" in out
    # リーチ時点のツモ／打牌回数と成立判定
    assert "東家: リーチ時点 ツモ 0 回 / 打牌 0 回 [成立]" in out
