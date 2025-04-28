import re
import xml.etree.ElementTree as ET
from mahjong_py.converters import convert_tile_id_to_str
from mahjong_py.splitter import split_kyokus

def display_dora_fixed(kyoku_str: str, game_index: int = None):
    print("\n\n── Game {} ドラ表示牌 ──".format(game_index if game_index is not None else ""))

    kyoku_list = split_kyokus(kyoku_str)

    for i, kyoku_text in enumerate(kyoku_list):
        dora_ids = []

        try:
            # seed属性の取得（6番目の値が開局時のドラ表示牌）
            root = ET.fromstring("<root>{}</root>".format(kyoku_text))
            init_tag = root.find("INIT")
            if init_tag is not None:
                seed = init_tag.get("seed")
                if seed:
                    seed_parts = seed.split(",")
                    if len(seed_parts) >= 6:
                        dora_ids.append(int(seed_parts[5]))

            # <DORA> タグの追加ドラも収集
            dora_ids += [int(m) for m in re.findall(r'<DORA\s+hai=["\'](\d+)["\']', kyoku_text)]

            if not dora_ids:
                print("第{}局: [WARNING] ドラ表示牌なし".format(i + 1))
                continue

            dora_tiles = [convert_tile_id_to_str(d) for d in dora_ids]
            print("第{}局: {}".format(i + 1, " ".join(dora_tiles)))

        except Exception as e:
            print("第{}局: [ERROR] ドラ牌の解析に失敗: {}".format(i + 1, str(e)))
