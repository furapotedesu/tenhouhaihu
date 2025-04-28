import xml.etree.ElementTree as ET
from mahjong_py.splitter import split_kyokus


def display_reach_info_fixed(kyoku_str: str, game_index: int = None):
    print("\n\n── Game {} リーチ情報 ──".format(game_index if game_index is not None else ""))

    kyoku_list = split_kyokus(kyoku_str)

    for i, kyoku_text in enumerate(kyoku_list):
        try:
            root = ET.fromstring("<root>{}</root>".format(kyoku_text))
        except ET.ParseError as e:
            print("[ERROR] XML解析失敗: {}".format(str(e)))
            continue

        reach_tags = root.findall("REACH")
        if not reach_tags:
            continue

        print("Game {} 第{}局".format(game_index, i + 1))
        tsumo_counts = [0] * 4
        dahai_counts = [0] * 4
        reach_steps = {}
        reach_success = {}

        # 先にリーチのstepを記録
        for tag in reach_tags:
            who = int(tag.get("who", -1))
            step = int(tag.get("step", -1))
            if who == -1 or step == -1:
                continue

            if step == 1:
                reach_steps[who] = None  # リーチ宣言時点でのカウントを後で記録
                print("   {}家がリーチ宣言".format(["東", "南", "西", "北"][who]))
            elif step == 2:
                reach_success[who] = True

        # ツモ・打牌カウントしつつリーチ宣言時点を記録
        for tag in root:
            if tag.tag[0] in "TUVW":
                who = ord(tag.tag[0]) - ord("T")
                tsumo_counts[who] += 1
            elif tag.tag[0] in "DEFG":
                who = ord(tag.tag[0]) - ord("D")
                dahai_counts[who] += 1
            elif tag.tag == "REACH":
                who = int(tag.get("who", -1))
                step = int(tag.get("step", -1))
                if step == 1 and who in reach_steps:
                    reach_steps[who] = (tsumo_counts[who], dahai_counts[who])

        for j in range(4):
            if j in reach_steps:
                tsumo, dahai = reach_steps[j]
                success = "成立" if reach_success.get(j, False) else "不成立"
                print("   {}家: リーチ時点 ツモ {} 回 / 打牌 {} 回 [{}]".format(
                    ["東", "南", "西", "北"][j], tsumo, dahai, success))
