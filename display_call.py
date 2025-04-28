import xml.etree.ElementTree as ET
from mahjong_py.splitter import split_kyokus
from mahjong_py.analyzer import decode_mentsu
from mahjong_py.converters import convert_tile_id_to_str
import logging

logger = logging.getLogger(__name__)


def display_calls_fixed(kyoku_str: str, game_index: int = None):
    print("\n\n└─ Game {} 鳴き情報 ┐".format(game_index if game_index is not None else ""))

    kyoku_list = split_kyokus(kyoku_str)

    for i, kyoku_text in enumerate(kyoku_list):
        try:
            root = ET.fromstring("<root>{}</root>".format(kyoku_text))
        except ET.ParseError as e:
            print(f"[ERROR] XML parse error at kyoku {i+1}: {e}")
            continue

        tags = list(root)
        tsumo_counts = [0, 0, 0, 0]
        hand_state = [[] for _ in range(4)]
        call_events = []

        init_tag = root.find("INIT")
        if init_tag is not None:
            for j in range(4):
                hai_str = init_tag.get(f"hai{j}", "")
                if hai_str:
                    hand_state[j] = list(map(int, hai_str.split(",")))

        current_index = 0

        while current_index < len(tags):
            tag = tags[current_index]
            tagname = tag.tag

            if tagname[0] in "TUVW" and tagname[1:].isdigit():
                who = ord(tagname[0]) - ord("T")
                tile = int(tagname[1:])
                hand_state[who].append(tile)
                tsumo_counts[who] += 1

            elif tagname[0] in "DEFG" and tagname[1:].isdigit():
                who = ord(tagname[0]) - ord("D")
                tile = int(tagname[1:])
                if tile in hand_state[who]:
                    hand_state[who].remove(tile)

            elif tagname == "N":
                who = int(tag.get("who"))
                meld = int(tag.get("m"))
                meld_tiles, meld_type = decode_mentsu(meld)

                tsumo_count = tsumo_counts[who]
                pre_naki_hand = hand_state[who][:]
                temp_hand = pre_naki_hand[:]

                logger.debug(f"[DEBUG] Before removal: who={who}, hand={sorted(temp_hand)}")
                logger.debug(f"[DEBUG] Meld tiles: {meld_tiles}, type: {meld_type}")

                if meld_type == "kakan":
                    # 加槓時は加えた1枚だけを除去（ポン済みの3枚はすでに手牌にない前提）
                    target_tile = meld_tiles[-1]
                    if target_tile in temp_hand:
                        temp_hand.remove(target_tile)
                else:
                    if meld_type in ("ankan", "daiminkan"):
                        removal_count = 4
                    else:
                        removal_count = 3

                    removed = 0
                    for tile in meld_tiles:
                        if tile in temp_hand and removed < removal_count:
                            temp_hand.remove(tile)
                            removed += 1

                logger.debug(f"[DEBUG] After removal: temp_hand={sorted(temp_hand)}")

                post_discard = None
                post_hand = None
                for lookahead in range(current_index + 1, len(tags)):
                    next_tag = tags[lookahead]
                    next_tagname = next_tag.tag
                    if next_tagname[0] in "DEFG" and next_tagname[1:].isdigit():
                        discard_who = ord(next_tagname[0]) - ord("D")
                        if discard_who == who:
                            discard_tile = int(next_tagname[1:])
                            post_discard = convert_tile_id_to_str(discard_tile)
                            if discard_tile in temp_hand:
                                temp_hand.remove(discard_tile)
                            post_hand = " ".join(sorted([convert_tile_id_to_str(t) for t in temp_hand]))
                            break

                meld_tile_strs = [convert_tile_id_to_str(t) for t in meld_tiles]

                if meld_type == "ankan":
                    call_str = f"{meld_tile_strs[-1]} を暗槓した（{' '.join(meld_tile_strs)}）"
                elif meld_type == "daiminkan":
                    call_str = f"{meld_tile_strs[-1]} を大明槓した（{' '.join(meld_tile_strs)}）"
                elif meld_type == "kakan":
                    call_str = f"{meld_tile_strs[-1]} を加槓した（{' '.join(meld_tile_strs)}）"
                elif meld_type == "pon":
                    call_str = f"{meld_tile_strs[-1]} をポンして {' '.join(meld_tile_strs[:-1])} と組み合わせた"
                elif meld_type == "chi":
                    call_str = f"{meld_tile_strs[-1]} をチーして {' '.join(meld_tile_strs[:-1])} と組み合わせた"
                else:
                    call_str = f"{meld_tile_strs[-1]} を鳴いた（{' '.join(meld_tile_strs)}）"

                call_events.append({
                    "局": i + 1,
                    "家": who,
                    "ツモ数": tsumo_count,
                    "鳴き": call_str,
                    "打牌": post_discard or "不明",
                    "手牌": post_hand or "不明"
                })

                for tile in meld_tiles:
                    if tile in hand_state[who]:
                        hand_state[who].remove(tile)

            current_index += 1

        for call in call_events:
            print("Game {} 第{}局 {}家".format(game_index, call["局"], ["東", "南", "西", "北"][call["家"]]))
            print("   ツモ数: {}".format(call["ツモ数"]))
            print("   鳴き内容: {}".format(call["鳴き"]))
            print("   直後の打牌: {}".format(call["打牌"]))
            print("   直後の手牌: {}".format(call["手牌"]))
