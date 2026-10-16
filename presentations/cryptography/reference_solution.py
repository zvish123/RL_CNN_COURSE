"""
פתרון ייחוס למורה בלבד - צופן טרנספוזיציה עמודתי עם סיסמה
לא להפיץ לתלמידים לפני סוף השיעור.

מוסכמות (זהות לדף העבודה ולמצגת):
1. נרמול: אותיות גדולות, נשמרות רק האותיות A-Z (רווחים וסימנים נמחקים).
2. כותבים את ההודעה בשורות, ברוחב = אורך הסיסמה.
3. אם השורה האחרונה לא מלאה - מרפדים ב-X.
4. סדר קריאת העמודות = הסדר האלפביתי של אותיות הסיסמה.
   אותיות זהות בסיסמה: העמודה השמאלית יותר נקראת קודם.
5. קוראים כל עמודה מלמעלה למטה ומחברים.

הקוד כתוב בכוונה רק עם כלים שתלמידי י' מכירים: לולאות, מחרוזות, רשימות, פונקציות.
"""

PAD = "X"


def normalize(text):
    """אותיות גדולות, רק A-Z."""
    result = ""
    for ch in text.upper():
        if "A" <= ch <= "Z":
            result += ch
    return result


def get_order(key):
    """
    מחזירה רשימה של אינדקסי עמודות בסדר הקריאה.
    דוגמה: get_order("ZEBRA") -> [4, 2, 1, 3, 0]
    אותיות זהות: לפי המיקום משמאל לימין.
    """
    key = normalize(key)
    # דרגה של כל עמודה = כמה אותיות קטנות ממנה + כמה זהות לה שמופיעות לפניה
    ranks = []
    for i in range(len(key)):
        rank = 0
        for j in range(len(key)):
            if key[j] < key[i] or (key[j] == key[i] and j < i):
                rank += 1
        ranks.append(rank)
    # הופכים "דרגה של כל עמודה" ל"איזו עמודה בכל תור"
    order = [0] * len(key)
    for col in range(len(key)):
        order[ranks[col]] = col
    return order


def encrypt(plaintext, key):
    text = normalize(plaintext)
    width = len(normalize(key))
    if width == 0:
        raise ValueError("key must contain at least one letter")
    while len(text) % width != 0:
        text += PAD
    rows = []
    for start in range(0, len(text), width):
        rows.append(text[start:start + width])
    ciphertext = ""
    for col in get_order(key):
        for row in rows:
            ciphertext += row[col]
    return ciphertext


def decrypt(ciphertext, key):
    text = normalize(ciphertext)
    width = len(normalize(key))
    if width == 0:
        raise ValueError("key must contain at least one letter")
    if len(text) % width != 0:
        raise ValueError("ciphertext length must be a multiple of key length")
    n_rows = len(text) // width
    # כל n_rows אותיות רצופות בצופן = עמודה אחת
    columns = [""] * width
    pos = 0
    for col in get_order(key):
        columns[col] = text[pos:pos + n_rows]
        pos += n_rows
    plaintext = ""
    for r in range(n_rows):
        for c in range(width):
            plaintext += columns[c][r]
    return plaintext


def show_grid(plaintext, key):
    """עזר להדגמה: מדפיס את הטבלה עם מספרי הסדר."""
    text = normalize(plaintext)
    k = normalize(key)
    while len(text) % len(k) != 0:
        text += PAD
    order = get_order(k)
    ranks = [0] * len(k)
    for pos, col in enumerate(order):
        ranks[col] = pos + 1
    print(" ".join(k))
    print(" ".join(str(r) for r in ranks))
    print("-" * (2 * len(k) - 1))
    for s in range(0, len(text), len(k)):
        print(" ".join(text[s:s + len(k)]))


# ---------------- בדיקות ----------------
if __name__ == "__main__":
    # סדר עמודות
    assert get_order("ZEBRA") == [4, 2, 1, 3, 0]
    assert get_order("CAT") == [1, 0, 2]
    assert get_order("BAD") == get_order("CAT")          # אותה תבנית = אותו מפתח בפועל
    assert get_order("SECRET") == [2, 1, 4, 3, 0, 5]      # שתי E: השמאלית קודם
    assert get_order("A") == [0]
    # ZEBRA/KEY/BYTE are self-inverse: a "ranks instead of order" bug passes them.
    # CODE and CYBER catch it.
    assert get_order("CODE") == [0, 2, 3, 1]
    assert get_order("CYBER") == [2, 0, 3, 4, 1]
    # נרמול
    assert normalize("Meet me, at 5!") == "MEETMEAT"
    # הצפנה
    assert encrypt("ABCDEF", "BA") == "BDFACE"
    assert encrypt("hello", "A") == "HELLO"                # מפתח באורך 1 = אין שינוי
    # הלוך-חזור על מקרים רבים
    for msg in ["MEET AT THE LAB AFTER SCHOOL", "A", "TRANSPOSITION", "XYZ" * 7]:
        for key in ["ZEBRA", "SECRET", "CAT", "LONGERKEYTHANMSG", "Q"]:
            c = encrypt(msg, key)
            p = decrypt(c, key)
            assert p.startswith(normalize(msg)), (msg, key)
            assert len(c) % len(key) == 0
            assert sorted(c) == sorted(normalize(msg) + PAD * (len(c) - len(normalize(msg))))
    print("all tests passed")
