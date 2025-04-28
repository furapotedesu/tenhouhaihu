# splitter.py
import re

def split_games(text: str) -> list:
    """
    テキスト全体を、
    `<mjloggm` から始まるブロックごとに切り出して返します。
    区切り線（80個の=）は正規表現で無視します。
    """
    pattern = r'(<mjloggm[\s\S]*?)(?=\r?\n={80}\r?\n|\Z)'
    return re.findall(pattern, text)


def split_kyokus(text: str) -> list[str]:
    """
    各局を <INIT> タグから、
    次の <INIT> または </mjloggm> 直前までを1局とみなして抽出。
    """
    pattern = r'(<INIT[\s\S]*?)(?=(<INIT|</mjloggm>|\Z))'
    return [m[0] for m in re.findall(pattern, text)]


if __name__ == '__main__':
    # テストコード
    sample = (
        '<mjloggm>'
        '<INIT seed="0"/><D0/><RYUUKYOKU sc="250,0,250,0,250,0,250,0"/>'
        '<INIT seed="1"/><D1/></mjloggm>'
    )
    games = split_games(sample)
    assert len(games) == 1, f"split_games failed: {games}"

    kyokus = split_kyokus(games[0])
    assert len(kyokus) == 2, f"split_kyokus failed: {kyokus}"

    print('All splitter tests passed')
