import re
import xml.etree.ElementTree as ET
from typing import Tuple, List

# ───────── 配牌＋ツモ＋捨て牌 を解析 ─────────
def parse_init_hand(kyoku_str: str) -> Tuple[List[List[int]], List[List[int]], List[List[int]]]:
    """
    1局分の kyoku_str を受け取り、
    各プレイヤーの初期手牌・ツモ・捨て牌を返す。
    """
    # 初期手牌抽出
    init_match = re.search(r"<INIT[^>]*/>", kyoku_str)
    if not init_match:
        raise ValueError("<INIT> タグが見つかりません")
    init_tag = init_match.group(0)

    root = ET.fromstring(init_tag)
    hands = []
    for i in range(4):
        hai_str = root.attrib.get(f"hai{i}", "")
        ids = list(map(int, hai_str.split(","))) if hai_str else []
        hands.append(ids)

    # ツモタグ: T, U, V, W（0〜3に対応）
    tsumos = [[] for _ in range(4)]
    tsumo_tag_map = {"T": 0, "U": 1, "V": 2, "W": 3}
    for m in re.finditer(r"<([TUVW])(\d+)/?>", kyoku_str):
        who = tsumo_tag_map[m.group(1)]
        tile_id = int(m.group(2))
        tsumos[who].append(tile_id)

    # 捨て牌タグ: D, E, F, G（0〜3に対応）
    discards = [[] for _ in range(4)]
    discard_tag_map = {"D": 0, "E": 1, "F": 2, "G": 3}
    for m in re.finditer(r"<([DEFG])(\d+)/?>", kyoku_str):
        who = discard_tag_map[m.group(1)]
        tile_id = int(m.group(2))
        discards[who].append(tile_id)

    return hands, tsumos, discards


# ───────── 巡目解析（リーチ用）─────────
def parse_draws_and_discards(kyoku: str) -> Tuple[dict[int, List[int]], dict[int, List[int]]]:
    """
    各プレイヤーごとのツモ・打牌を記録して返す。
    返り値: (tsumos, discards)
        tsumos: {0: [ツモ牌ID,...], 1: [...], ...}
        discards: {0: [捨て牌ID,...], ...}
    """
    tsumos = {i: [] for i in range(4)}
    discards = {i: [] for i in range(4)}

    # ツモタグ
    tsumo_tag_map = {"T": 0, "U": 1, "V": 2, "W": 3}
    for m in re.finditer(r"<([TUVW])(\d+)/?>", kyoku):
        who = tsumo_tag_map[m.group(1)]
        tile_id = int(m.group(2))
        tsumos[who].append(tile_id)

    # 打牌タグ
    discard_tag_map = {"D": 0, "E": 1, "F": 2, "G": 3}
    for m in re.finditer(r"<([DEFG])(\d+)/?>", kyoku):
        who = discard_tag_map[m.group(1)]
        tile_id = int(m.group(2))
        discards[who].append(tile_id)

    return tsumos, discards
