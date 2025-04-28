import re
from typing import Dict, List, Tuple, Any
from mahjong_py.converters import convert_tile_id_to_str
from mahjong_py.analyzer import decode_mentsu

def parse_player_names(game_str: str) -> Dict[int, str]:
    m = re.search(r'<UN\s+([^>]+)>', game_str)
    if not m:
        raise ValueError("<UN>タグが見つかりませんでした。")
    attrs = m.group(1)
    name_map: Dict[int, str] = {}
    for num, name in re.findall(r'n(\d+)="([^"]+)"', attrs):
        name_map[int(num)] = name
    return name_map


def get_kyoku_segment(game_str: str, kyoku_index: int) -> str:
    segments = re.split(r'(?=<INIT\b)', game_str)
    ks = segments[1:]
    if kyoku_index < 0 or kyoku_index >= len(ks):
        raise IndexError(f"局インデックス {kyoku_index} は範囲外です。利用可能な局数: {len(ks)}")
    return ks[kyoku_index]


def process_segment(segment: str) -> List[Tuple[int, int, List[int], List[Tuple[str, List[int]]]]]:
    init = re.search(r'<INIT\s+([^>]+)>', segment)
    if not init:
        raise ValueError("INITタグが見つかりませんでした。")
    attrs = init.group(1)
    hands: Dict[int, List[int]] = {}
    melds: Dict[int, List[Tuple[str, List[int]]]] = {i: [] for i in range(4)}
    for i in range(4):
        m = re.search(r'hai{}="([0-9,]+)"'.format(i), attrs)
        if not m:
            raise ValueError(f"hai{i} が INIT タグにありません。")
        tiles = list(map(int, m.group(1).split(',')))
        hands[i] = tiles.copy()

    pattern = re.compile(r'<([TUVWDEFG])(\d+)/>|<N\s+who="(\d+)"\s+m="(\d+)"\s*/>')
    events = pattern.finditer(segment)
    discard_counts: Dict[int, int] = {i: 0 for i in range(4)}
    results: List[Tuple[int, int, List[int], List[Tuple[str, List[int]]]]] = []

    for ev in events:
        tag = ev.group(1)
        if tag:
            num = int(ev.group(2))
            if tag in ('T', 'U', 'V', 'W'):
                player = {'T': 0, 'U': 1, 'V': 2, 'W': 3}[tag]
                hands[player].append(num)
            else:
                player = {'D': 0, 'E': 1, 'F': 2, 'G': 3}[tag]
                discard_counts[player] += 1
                if num in hands[player]:
                    hands[player].remove(num)
                else:
                    raise ValueError(f"プレイヤー {player} の手牌に {num} が存在しません: {hands[player]}")
                hand_snap = hands[player].copy()
                meld_snap = [(mt, ml.copy()) for mt, ml in melds[player]]
                results.append((player, discard_counts[player], hand_snap, meld_snap))
        else:
            player = int(ev.group(3))
            m_flags = int(ev.group(4))
            tiles, meld_type = decode_mentsu(m_flags)
            melds[player].append((meld_type, tiles.copy()))
            for t in tiles:
                if t in hands[player]:
                    hands[player].remove(t)

    return results


def display_discard_hand_at(game_str: str, kyoku_index: int) -> None:
    name_map = parse_player_names(game_str)
    segment = get_kyoku_segment(game_str, kyoku_index)
    data = process_segment(segment)
    for player, count, hand, meld_list in data:
        name = name_map.get(player, f"Player{player}")
        hidden = [convert_tile_id_to_str(t) for t in hand]
        melds_str: List[str] = []
        for mtype, tiles in meld_list:
            txt = [convert_tile_id_to_str(t) for t in tiles]
            melds_str.append(f"{mtype}:{txt}")
        print(f"{name} さんの {count} 回目の打牌後の手牌 (隠れ牌): {hidden}")
        if melds_str:
            print(f"  副露メンツ: {melds_str}")
