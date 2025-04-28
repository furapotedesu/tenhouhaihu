# shanten_calc.py

from mahjong.shanten import Shanten

# 日本語牌→34インデックス変換（赤牌対応）
tile_name_to_index = {
    # マンズ
    '一萬': 0, '二萬': 1, '三萬': 2, '四萬': 3, '五萬': 4, '六萬': 5, '七萬': 6, '八萬': 7, '九萬': 8,
    # ピンズ
    '1筒': 9, '2筒': 10, '3筒': 11, '4筒': 12, '5筒': 13, '6筒': 14, '7筒': 15, '8筒': 16, '9筒': 17,
    # ソウズ
    '1索': 18, '2索': 19, '3索': 20, '4索': 21, '5索': 22, '6索': 23, '7索': 24, '8索': 25, '9索': 26,
    # 字牌
    '東': 27, '南': 28, '西': 29, '北': 30, '白': 31, '發': 32, '中': 33,
    # 赤牌（通常の5と同じ扱い）
    '赤五萬': 4, '赤5萬': 4,
    '赤5筒': 13, '赤⑤筒': 13,
    '赤5索': 22, '赤⑤索': 22
}

def convert_to_34_array(japanese_tiles):
    array_34 = [0] * 34
    for tile in japanese_tiles:
        index = tile_name_to_index.get(tile)
        if index is None:
            raise ValueError(f"未知の牌: {tile}")
        array_34[index] += 1
    return array_34

def calculate_chiitoitsu_shanten(tiles_34):
    pairs = sum(1 for count in tiles_34 if count >= 2)
    total_tiles = sum(tiles_34)
    if total_tiles > 14:
        return 99  # 不正手牌
    return 6 - pairs + (14 - total_tiles)

def calculate_kokushi_shanten(tiles_34):
    terminals_and_honors = [0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33]
    unique = sum(1 for i in terminals_and_honors if tiles_34[i] >= 1)
    has_pair = any(tiles_34[i] >= 2 for i in terminals_and_honors)
    total_tiles = sum(tiles_34)
    if total_tiles > 14:
        return 99  # 不正手牌
    return 13 - unique - (1 if has_pair else 0) + (14 - total_tiles)

def calculate_shanten(japanese_tiles, melds_count=0):
    tiles_34 = convert_to_34_array(japanese_tiles)
    shanten = Shanten()
    return {
        '通常': shanten.calculate_shanten(tiles_34, melds_count),
        '七対子': calculate_chiitoitsu_shanten(tiles_34),
        '国士無双': calculate_kokushi_shanten(tiles_34),
    }
