def test_import_package_and_submodules():
    """
    Test that the mahjong_py package and all expected submodules can be imported.
    """
    import mahjong_py
    submodules = [
        'converters', 'splitter', 'parser', 'analyzer', 'utils',
        'display_handflow', 'display_agari_fixed', 'display_reach_fixed',
        'display_ryuukyoku', 'display_dora_fixed', 'display_call',
        'shanten_calc', 'display_discard_hand_at'
    ]
    for sub in submodules:
        __import__(f"mahjong_py.{sub}")
