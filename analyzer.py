from mahjong_py.converters import convert_tile_list
import logging
import re
from mahjong_py import splitter

# ───────── ログ設定 ─────────
logging.basicConfig(level=logging.DEBUG, force=True)
logger = logging.getLogger(__name__)

# ───────── ゲーム分割 ─────────
def split_games(text: str) -> list[str]:
    """
    テキスト全体を、
    <mjloggm から始まるブロックごとに切り出して返します。
    区切り線（80個の=）は自動で無視されます。
    """
    pattern = rf'(<mjloggm[\s\S]*?)(?=\r?\n{"="*80}\r?\n|\Z)'
    return re.findall(pattern, text)

# ───────── 鳴り形デコード ─────────#
def decode_mentsu(m: int) -> tuple[list[int], str]:
    """
    16bit の副露ビットフィールド m を
    136-ID のリストと副露タイプ ('chi', 'pon', 'ankan', 'daiminkan', 'kakan') に展開して返します。
    """
    tiles: list[int] = []
    kui = m & 0x3  # 食い仕掛け情報

    # --- 順子 (チー) ---
    if m & 0x0004:
        t = (m & 0xFC00) >> 10
        r = t % 3
        t = t // 3
        t = (t // 7) * 9 + (t % 7)
        t *= 4
        offs = [((m & 0x0018) >> 3), ((m & 0x0060) >> 5), ((m & 0x0180) >> 7)]
        order = [r, (r+1)%3, (r+2)%3]
        for i in order:
            tiles.append(t + 4*i + offs[i])
        meld_type = "chi"

    # --- ポン / 加槓 ---
    elif m & 0x0008 or m & 0x0010:
        t = (m & 0xFE00) >> 9
        r = t % 3
        t = (t // 3) * 4
        unused = (m & 0x0060) >> 5
        h = [t, t, t]
        if unused == 0:
            h = [t+1, t+2, t+3]
        elif unused == 1:
            h = [t,   t+2, t+3]
        elif unused == 2:
            h = [t,   t+1, t+3]
        else:
            h = [t,   t+1, t+2]
        if r == 1:
            h.insert(0, h.pop(1))
        elif r == 2:
            h.insert(0, h.pop(2))
        if m & 0x0010:
            tiles.extend(h + [h[2]])
            meld_type = "kakan"
        else:
            tiles.extend(h)
            meld_type = "pon"

    # --- 北抜き ---
    elif m & 0x0020:
        hai0 = (m & 0xFF00) >> 8
        tiles.append(hai0)
        meld_type = "nuki"

    # --- 暗槓 / 大明槓 ---
    else:
        hai0 = (m & 0xFF00) >> 8
        base = (hai0 & ~3)
        ids = [base, base+1, base+2, base+3]
        if not kui:
            tiles.extend(ids)
            meld_type = "ankan"
        else:
            r = m & 0x3
            if r == 1:
                h = [ids[2], hai0, ids[0], ids[1]]
            elif r == 2:
                h = [ids[0], ids[2], hai0, ids[1]]
            else:
                h = [hai0, ids[0], ids[1], ids[2]]
            tiles.extend(h)
            meld_type = "daiminkan"

    logger.debug(f"[DEBUG] decode_mentsu({m:#06x}) → {tiles}, type={meld_type}")
    return tiles, meld_type

# ───────── 和了形抽出 ─────────
def get_all_agari_tiles(game_str: str) -> list[list[str]]:
    logger.debug(">>> get_all_agari_tiles() が呼ばれました")
    agari_lists: list[list[str]] = []

    games = split_games(game_str)
    for idx, kyoku in enumerate(games, start=1):
        logger.debug(f"[LOG] ======= Game {idx} =======")

        init_match = re.search(r'<INIT[^>]*hai0="([^"]+)"[^>]*hai1="([^"]+)"[^>]*hai2="([^"]+)"[^>]*hai3="([^"]+)"', kyoku)
        if not init_match:
            logger.warning("INITタグが見つかりませんでした")
            continue
        hands = [list(map(int, init_match.group(i).split(','))) for i in range(1, 5)]

        melds: list[tuple[int, list[int]]] = []
        for nm in re.finditer(r'<N\s+who="([0-3])"\s+m="(\d+)"', kyoku):
            who = int(nm.group(1))
            m = int(nm.group(2))
            meld_tiles, _ = decode_mentsu(m)
            melds.append((who, meld_tiles))

        agari_match = re.search(r'<AGARI[^>]*who="([0-3])"', kyoku)
        if not agari_match:
            logger.debug("AGARIタグがありません（流局など）")
            continue
        winner = int(agari_match.group(1))

        final_ids = []
        for pid, tiles in melds:
            if pid == winner:
                final_ids.extend(tiles)

        result_text = convert_tile_list(','.join(map(str, final_ids)))
        logger.debug(f"[RESULT] Game {idx} → {result_text}")
        agari_lists.append(result_text)

    logger.debug(f"[DEBUG] 処理終了。和了形を {len(agari_lists)} 件見つけました")
    return agari_lists
