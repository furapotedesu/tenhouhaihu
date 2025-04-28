import xml.etree.ElementTree as ET
from mahjong_py.converters import convert_tile_list, convert_yaku_id_to_name
from mahjong_py.splitter import split_kyokus

def display_agari_details(kyoku_str: str, game_index: int = None):
    print("\n\n── Game {} 和了詳細 ──".format(game_index if game_index is not None else ""))

    kyoku_list = split_kyokus(kyoku_str)

    for i, kyoku_text in enumerate(kyoku_list):
        try:
            root = ET.fromstring("<root>{}</root>".format(kyoku_text))
        except ET.ParseError as e:
            print("[ERROR] XML解析失敗: {}".format(str(e)))
            continue

        agari_tags = root.findall("AGARI")
        if not agari_tags:
            continue

        for agari in agari_tags:
            try:
                kyoku_num = i + 1
                who = int(agari.get("who"))
                print("Game {} 第{}局 和了者: {}家".format(game_index, kyoku_num, ["東", "南", "西", "北"][who]))

                # メルド情報
                melds_str = agari.get("m", "")
                meld_count = melds_str.count(",") + 1 if melds_str else 0
                meld_tiles = meld_count * 3 + 2
                hidden_count = 14 - meld_tiles
                print("   メルド枚数: {}  隠し枚数: {}  合計: 14枚".format(meld_tiles, hidden_count))

                # 手牌表示
                tiles = convert_tile_list(agari.get("hai"))
                print("   手牌: {}".format(" ".join(tiles)))

                # 役満チェック
                yakuman_str = agari.get("yakuman", "")
                if yakuman_str:
                    yakuman_ids = list(map(int, yakuman_str.split(",")))
                    yakuman_names = convert_yaku_id_to_name(yakuman_ids)
                    print("   役満: {}".format(", ".join(yakuman_names)))

                # 通常役チェック
                yaku_str = agari.get("yaku", "")
                if yaku_str:
                    yaku_ids = list(map(int, yaku_str.split(",")))
                    # 奇数番目の値だけが役ID（偶数番目は翻数）とみなす
                    yaku_ids = [yaku_ids[i] for i in range(0, len(yaku_ids), 2)]
                    yaku_names = convert_yaku_id_to_name(yaku_ids)
                    print("   役: {}".format(", ".join(yaku_names)))
                else:
                    print("   役: なし")

                # 得点表示
                ten = agari.get("ten")
                print("   得点: {}".format(ten))

            except Exception as e:
                print("   [ERROR] 和了情報の解析に失敗:", str(e))
