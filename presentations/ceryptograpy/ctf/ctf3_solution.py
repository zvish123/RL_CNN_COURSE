import re
from collections import Counter, defaultdict


# ------------------------------------
# Helper: count frequencies by words
# ------------------------------------
def word_freq(text):
    words = re.findall(r"[A-Z]+", text.upper())
    return Counter(words)


# ------------------------------------
# Step 1: initialize empty mapping
# ------------------------------------
def empty_mapping():
    m = {}
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        m[c] = None
    return m


# ------------------------------------
# Step 2: apply mapping to decrypt
# (unknown letters become "_")
# ------------------------------------
def apply_mapping(text, mapping):
    result = []
    for ch in text:
        if ch.upper() in mapping and mapping[ch.upper()] is not None:
            plain = mapping[ch.upper()]
            if ch.islower():
                plain = plain.lower()
            result.append(plain)
        elif ch.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            result.append("_")
        else:
            result.append(ch)
    return "".join(result)


# ------------------------------------
# Step 3: assign letter if still free
# ------------------------------------
def assign(mapping, cipher, plain):
    if mapping[cipher] is None:
        mapping[cipher] = plain
    return mapping


# ------------------------------------
# Step 4: find candidate words by pattern
# ------------------------------------
def find_pattern_words(text, length, pattern):
    """
    pattern: tuple representing repeated positions, e.g.
    UNDERGROUND pattern:
    (0,8), (1,9), (2,10), (4,6)
    """
    words = re.findall(r"[A-Z]+", text)
    candidates = []
    for w in words:
        if len(w) != length:
            continue
        ok = True
        for p1, p2 in pattern:
            if w[p1] != w[p2]:
                ok = False
                break
        if ok:
            candidates.append(w)
    return candidates


# ------------------------------------
# Build the solution using your clues
# ------------------------------------
def break_cipher(text):
    mapping = empty_mapping()

    # ==============================================================
    # RULE 1: Identify "THE" as the most common 3-letter word
    # ==============================================================

    freq = word_freq(text)
    most_common_3 = [w for w, f in freq.most_common() if len(w) == 3]
    if most_common_3:
        the_word = most_common_3[0]  # candidate for "THE"
        mapping = assign(mapping, the_word[0], "T")
        mapping = assign(mapping, the_word[1], "H")
        mapping = assign(mapping, the_word[2], "E")

    # ==============================================================
    # RULE 2: Find UNDERGROUND pattern
    # Pattern of UNDERGROUND:
    # positions equal: (0,8), (1,9), (2,10), (4,6)
    # ==============================================================

    pattern = [(0, 8), (1, 9), (2, 10), (4, 6)]
    underground_candidates = find_pattern_words(text, 11, pattern)
    if underground_candidates:
        u = underground_candidates[0]

        # UNDERGROUND = U N D E R G R O U N D
        plain = "UNDERGROUND"
        for ciph, pl in zip(u, plain):
            mapping = assign(mapping, ciph, pl)

    # ==============================================================
    # RULE 3: last sentence contains FLAG
    # ==============================================================

    # lines = text.strip().splitlines()
    # last_line = re.findall(r"[A-Z]+", lines[-1])
    # for w in last_line:
    #     if len(w) == 4:
    #         # try FLAG pattern: all letters unique
    #         c1, c2, c3, c4 = w
    # JNYB => FLAG
    mapping = assign(mapping, 'J', "F")
    mapping = assign(mapping, 'N', "L")
    mapping = assign(mapping, 'Y', "A")
    mapping = assign(mapping, 'B', "G")
            # break

    # ==============================================================
    # RULE 4: SECRET appears more than once
    # pattern of SECRET (6 letters):
    # positions repeated: 1,3,5 = E,E,E
    # ==============================================================

    secret_pattern = [(1, 3), (3, 5)]
    secret_candidates = find_pattern_words(text, 6, secret_pattern)
    if secret_candidates:
        s = secret_candidates[0]
        # SECRET = S E C R E T
        plain = "SECRET"
        for ciph, pl in zip(s, plain):
            mapping = assign(mapping, ciph, pl)

    # ==============================================================
    # ADD to mapping base on common sence and english words
    # ==============================================================
    # o_ => of => RJ
    assign(mapping, 'J', 'F')
    # _E_RET => KQXWQZ
    assign(mapping, 'K', 'S')
    assign(mapping, 'X', 'C')
    # _S => GK
    assign(mapping, 'G', 'I')
    #_ISSION => VGKKGRO
    # assign(mapping, 'V', 'M')
    # #CR__TOGRA_H_ => XWIMZRBWYMLI
    # assign(mapping, 'I', 'Y')
    # assign(mapping, 'M', 'P')
    # #LI_RARY=>NGPWYWI
    # assign(mapping, 'P', 'B')
    # #T_OHUNDRED =>ZARLUOCWQC
    # assign(mapping, 'A', 'W')
    # #HA_E -> LYTQ
    # assign(mapping, 'T', 'V')
    # #NETWOR_=>OQZARWS
    # assign(mapping, 'S', 'K')

    # ==============================================================
    # Apply mapping on text
    # ==============================================================

    decrypted = apply_mapping(text, mapping)
    return mapping, decrypted


# ---------------------------------------------------------------
# RUN
# ---------------------------------------------------------------
secret_text = """ZLQ KQXWQZ VGKKGRO RJ ZLQ XWIMZRBWYMLI GK LGCCQO GO ZLQ RNC NGPWYWI PUGNCGOB
OQYW ZLQ ZWYGO KZYZGRO PQLGOC ZLQ PYOS GO ZLQ ORWZLQWO KQXZGRO RJ ZLQ LGNNK
ZLQ QOQVI JRWXQK LYTQ PUGNZ Y OQZARWS RJ ZUOOQNK UOCQWBWRUOC GO ZLQ XRYKZYN
YWQYK ZR ZWYOKMRWZ AQYMROK YOC KUMMNGQK JRW ZLQGW VGNGZYWI RMQWYZGROK ZLQKQ
ZUOOQNK YWQ BUYWCQC PI ZLQ PQKZ KRNCGQWK JWRV ZLQ WQBGVQOZ YOC ZLQI LYTQ
KZWGXZ RWCQWK ZR CQJQOC ZLQV AGZL ZLQGW NGTQK GJ OQXQKKYWI ZLQ JGWKZ ZUOOQN
GK NRXYZQC UOCQWBWRUOC YZ ZLQ RNC XLUWXL ALQWQ ZLQ MWYIQW PRRS GK LGCCQO
PQLGOC ZLQ YNZYW ZLQ KQXROC ZUOOQN GK OQYW ZLQ WRXS XRTQK ALQWQ ZLQ AGZXL
NQJZ LQW VYWS GO ZLQ JYXQ RJ ZLQ WGKGOB KUO ZLQ ZLGWC ZUOOQN GK UOCQWBWRUOC
UOCQW ZLQ YQWGYN WGCBQ GO ZLQ LYWPRW ALQWQ ZLQ JGKLQWVQO KYGNZLQGW PRYZK YZ
CYAO YOC ALQWQ ZLQ KQXWQZ VQQZGOB MNYXQ AYKKQZ UM JRW VRWQ ZLYO ZARLUOCWQC
IQYWK ZLQ GVMRWZYOZ CRXUVQOZ GK GO ZLQ KQXROC ZUOOQN YOC ZLQ XWUXGYN XNUQK
GK GO ZLQ RONI KYJQ MNYXQ GK UOCQW ZLQ KZROQKZQMK ZLQ JNYB GO ZLQ XYZLQCWYN"""


mapping, result = break_cipher(secret_text)

print("=== MAPPING (partial) ===")
print(mapping)
print("\n=== DECRYPTED TEXT (partial) ===")
print(result)
