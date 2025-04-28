import xml.etree.ElementTree as ET
from mahjong_py.converters import convert_tile_list
from mahjong_py.splitter import split_kyokus

def display_ryuukyoku_info(kyoku_str: str, game_index: int = None):
    print("\n\n── Game {} 流局情報 ──".format(game_index if game_index is not None else ""))

    kyoku_list = split_kyokus(kyoku_str)

    for i, kyoku_text in enumerate(kyoku_list):
        try:
            root = ET.fromstring("<root>{}</root>".format(kyoku_text))
        except ET.ParseError as e:
            print("[ERROR] XML解析失敗: {}".format(str(e)))
            continue

        ryuukyoku_tags = root.findall("RYUUKYOKU")
        if not ryuukyoku_tags:
            continue

        for tag in ryuukyoku_tags:
            print("Game {} 第{}局".format(game_index, i + 1))

            sc = tag.get("sc")
            if sc:
                print("   点数変動 (sc):", sc)

            for j in range(4):
                hai_key = f"hai{j}"
                tiles = convert_tile_list(tag.get(hai_key, ""))
                if tiles:
                    print("   {}家の公開手牌: {}".format(["東", "南", "西", "北"][j], " ".join(tiles)))
