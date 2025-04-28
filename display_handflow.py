import xml.etree.ElementTree as ET
from mahjong_py.converters import convert_tile_list, convert_tile_id_to_str
from mahjong_py.splitter import split_kyokus

def display_hand_flow_by_kyoku(kyoku_str: str, game_index: int = None):
    print("\n\n── Game {} 手配進行 ──".format(game_index if game_index is not None else ""))

    kyoku_list = split_kyokus(kyoku_str)

    for i, kyoku_text in enumerate(kyoku_list):
        print("== 第{}局 ==".format(i + 1))

        try:
            root = ET.fromstring("<root>{}</root>".format(kyoku_text))
        except ET.ParseError as e:
            print("配 牌: [ERROR] XML解析失敗:", str(e))
            continue

        init_tag = root.find("INIT")
        if init_tag is None:
            print("配 牌: [ERROR] <INIT> タグが見つかりません")
            continue

        print("配 牌:")
        for j in range(4):
            hand_key = f"hai{j}"
            tiles = convert_tile_list(init_tag.get(hand_key, ""))
            print("  {}家: {}".format(["東", "南", "西", "北"][j], " ".join(tiles)))

        tsumos = [[] for _ in range(4)]
        discards = [[] for _ in range(4)]

        for tag in root:
            if tag.tag[0] in "TUVW":
                try:
                    who = ord(tag.tag[0]) - ord("T")
                    tile_id = int(tag.tag[1:])
                    tsumos[who].append(convert_tile_id_to_str(tile_id))
                except ValueError:
                    continue
            elif tag.tag[0] in "DEFG":
                try:
                    who = ord(tag.tag[0]) - ord("D")
                    tile_id = int(tag.tag[1:])
                    discards[who].append(convert_tile_id_to_str(tile_id))
                except ValueError:
                    continue

        print("\nツモ:")
        for j in range(4):
            print("  {}家: {}".format(["東", "南", "西", "北"][j], " ".join(tsumos[j])))

        print("\n捨て牌:")
        for j in range(4):
            print("  {}家: {}".format(["東", "南", "西", "北"][j], " ".join(discards[j])))