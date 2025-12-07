"""
Test Suite for Secret Cipher System
Mission: Golden Key
Agent: [YOUR NAME HERE]

TODO: Complete all 12 testing principles for full coverage
"""

import pytest
import random
import string
from secret_cipher import create_key_from_password, encrypt_message, decrypt_message


# ==========================================
# עקרון 1: בדיקה לכל פונקציה
# ==========================================

def test_create_key_basic():
    """בדיקה בסיסית ליצירת מפתח מסיסמה"""
    key = create_key_from_password("ZEBRA")
    assert key == [4, 1, 0, 3, 2], "Key generation failed for ZEBRA"
    print("✓ Test 1.1: Basic key creation passed")


def test_encrypt_basic():
    """בדיקה בסיסית להצפנה"""
    message = "HELLO"
    password = "KEY"
    cipher = encrypt_message(message, password)
    assert isinstance(cipher, str), "Encryption should return a string"
    assert len(cipher) >= len(message), "Cipher should not be shorter than message"
    print("✓ Test 1.2: Basic encryption passed")


def test_decrypt_basic():
    """בדיקה בסיסית לפענוח"""
    # TODO: השלם בדיקה זו
    pass


# ==========================================
# עקרון 2: מקרי שימוש (Use Cases)
# ==========================================

def test_full_encryption_cycle():
    """בדיקת מחזור שלם: הצפנה ופענוח"""
    message = "ATTACK AT DAWN"
    password = "SECRET"
    
    encrypted = encrypt_message(message, password)
    decrypted = decrypt_message(encrypted, password)
    
    assert decrypted == message, f"Expected '{message}', got '{decrypted}'"
    print("✓ Test 2.1: Full cycle passed")


def test_short_message():
    """בדיקת הודעה קצרה"""
    # TODO: בדוק הודעה בת 3-5 תווים
    pass


def test_long_message():
    """בדיקת הודעה ארוכה"""
    # TODO: בדוק הודעה בת 100+ תווים
    pass


def test_message_with_spaces():
    """בדיקת הודעה עם רווחים"""
    # TODO: בדוק הודעה עם רווחים מרובים
    pass


# ==========================================
# עקרון 3: מקרי קצה (Edge Cases)
# ==========================================

def test_empty_message_error():
    """בדיקה שהודעה ריקה זורקת שגיאה"""
    with pytest.raises(ValueError, match="Message cannot be empty"):
        encrypt_message("", "SECRET")
    print("✓ Test 3.1: Empty message error passed")


def test_short_password_error():
    """בדיקה שסיסמה קצרה מדי זורקת שגיאה"""
    # TODO: השלם בדיקה זו - סיסמה בת תו אחד
    pass


def test_empty_password_error():
    """בדיקה שסיסמה ריקה זורקת שגיאה"""
    # TODO: השלם בדיקה זו
    pass


def test_single_character_message():
    """בדיקת הודעה בת תו אחד"""
    # TODO: השלם בדיקה זו
    pass


# ==========================================
# עקרון 4: כיסוי קוד (Code Coverage)
# ==========================================

# רוץ: pytest test_secret_cipher.py --cov=secret_cipher
# וודא שכל השורות מכוסות

def test_matrix_creation_coverage():
    """בדיקה שמכסה את יצירת המטריצה"""
    # TODO: בדוק מקרים שונים של גדלי מטריצה
    pass


# ==========================================
# עקרון 5: כיסוי ענפים (Branch Coverage)
# ==========================================

def test_password_validation_branches():
    """בדיקת כל הענפים בבדיקת הסיסמה"""
    # TODO: בדוק את כל התנאים ב-if statements
    pass


# ==========================================
# עקרון 6: תלויות חיצוניות (External Dependencies)
# ==========================================

# אין תלויות חיצוניות בקוד הזה, אבל נוודא שכל פונקציה עובדת בנפרד

def test_create_key_independent():
    """בדיקה ש-create_key_from_password עובדת בנפרד"""
    # TODO: השלם בדיקות נוספות
    pass


# ==========================================
# עקרון 7: בדיקות שילוב (Integration Tests)
# ==========================================

def test_multiple_encryption_cycles():
    """בדיקת מספר מחזורי הצפנה ופענוח"""
    messages = ["HELLO", "WORLD", "TEST MESSAGE"]
    password = "KEY123"
    
    for msg in messages:
        encrypted = encrypt_message(msg, password)
        decrypted = decrypt_message(encrypted, password)
        assert decrypted == msg, f"Failed for message: {msg}"
    
    print("✓ Test 7.1: Multiple cycles passed")


def test_different_passwords_produce_different_ciphers():
    """בדיקה שסיסמאות שונות מייצרות הצפנות שונות"""
    # TODO: השלם בדיקה זו
    pass


# ==========================================
# עקרון 8: טיפול בחריגים (Exception Handling)
# ==========================================

def test_invalid_password_characters():
    """בדיקת תווים לא חוקיים בסיסמה"""
    with pytest.raises(ValueError):
        encrypt_message("TEST", "PASS@WORD!")
    print("✓ Test 8.1: Invalid password characters passed")


def test_all_exception_cases():
    """בדיקת כל מקרי החריגים האפשריים"""
    # TODO: בדוק את כל ה-ValueError שהקוד יכול לזרוק
    pass


# ==========================================
# עקרון 9: קלטים בלתי צפויים (Unexpected Inputs)
# ==========================================

def test_numeric_password():
    """בדיקת סיסמה מספרית"""
    message = "SECRET"
    password = "12345"
    encrypted = encrypt_message(message, password)
    decrypted = decrypt_message(encrypted, password)
    assert decrypted == message
    print("✓ Test 9.1: Numeric password passed")


def test_mixed_case_password():
    """בדיקת סיסמה עם אותיות גדולות וקטנות"""
    # TODO: בדוק סיסמה כמו "AbCdEf"
    pass


def test_unicode_characters():
    """בדיקת תווי Unicode"""
    # TODO: מה קורה עם תווים לא אנגליים?
    pass


def test_special_whitespace():
    """בדיקת רווחים מיוחדים"""
    # TODO: tabs, newlines וכו'
    pass


# ==========================================
# עקרון 10: תרחישי קצה מורכבים
# ==========================================

def test_password_with_repeated_characters():
    """בדיקת סיסמה עם תווים חוזרים"""
    message = "HELLO WORLD"
    password = "AAABBB"  # תווים זהים
    # TODO: השלם בדיקה זו - מה אמור לקרות?
    pass


def test_very_long_message():
    """בדיקת הודעה ארוכה מאוד"""
    message = "A" * 1000  # 1000 תווים
    password = "SECRET"
    # TODO: השלם בדיקה זו
    pass


def test_password_longer_than_message():
    """בדיקת מקרה שבו הסיסמה ארוכה מההודעה"""
    # TODO: מה קורה במקרה כזה?
    pass


def test_message_exact_multiple_of_password():
    """בדיקת הודעה שאורכה כפולה מדויקת של הסיסמה"""
    # TODO: הודעה באורך שמתחלק בדיוק על ידי אורך הסיסמה
    pass


# ==========================================
# עקרון 11: קלטים אקראיים (Random Testing)
# ==========================================

def test_random_messages_100_iterations():
    """בדיקה עם 100 הודעות וסיסמאות רנדומליות"""
    print("\n🎲 Running 100 random tests...")
    passed = 0
    failed = 0
    
    for i in range(100):
        try:
            # יצירת הודעה רנדומלית
            msg_length = random.randint(5, 50)
            message = ''.join(random.choices(string.ascii_letters + ' ', k=msg_length))
            
            # יצירת סיסמה רנדומלית
            pass_length = random.randint(2, 10)
            password = ''.join(random.choices(string.ascii_uppercase, k=pass_length))
            
            # בדיקה
            encrypted = encrypt_message(message, password)
            decrypted = decrypt_message(encrypted, password)
            
            if decrypted == message:
                passed += 1
            else:
                failed += 1
                print(f"  ✗ Test {i+1} failed")
                print(f"    Message: {message}")
                print(f"    Password: {password}")
                print(f"    Got: {decrypted}")
        
        except Exception as e:
            failed += 1
            print(f"  ✗ Test {i+1} error: {e}")
    
    print(f"✓ Random tests: {passed} passed, {failed} failed")
    assert failed == 0, f"{failed} random tests failed"


def test_random_with_special_cases():
    """בדיקות רנדומליות עם מקרי קצה"""
    # TODO: הוסף בדיקות רנדומליות עם:
    # - רווחים מרובים
    # - תווים מיוחדים שמותרים
    # - אורכים קיצוניים
    pass


# ==========================================
# עקרון 12: בדיקות גבולות (Boundary Testing)
# ==========================================

def test_minimum_password_length():
    """בדיקת אורך סיסמה מינימלי (2 תווים)"""
    message = "TEST"
    password = "AB"  # האורך המינימלי המותר
    encrypted = encrypt_message(message, password)
    decrypted = decrypt_message(encrypted, password)
    assert decrypted == message
    print("✓ Test 12.1: Minimum password length passed")


def test_password_length_boundary():
    """בדיקת גבולות אורך הסיסמה"""
    # TODO: בדוק סיסמה באורך 1 (אמור לזרוק שגיאה)
    # TODO: בדוק סיסמה באורך 2 (אמור לעבוד)
    pass


def test_message_length_boundaries():
    """בדיקת גבולות אורך ההודעה"""
    # TODO: בדוק הודעה באורך 1, 2, 100, 1000
    pass


def test_maximum_realistic_values():
    """בדיקת ערכים מקסימליים ריאליים"""
    # TODO: בדוק עם הודעה ארוכה מאוד וסיסמה ארוכה
    pass


# ==========================================
# בדיקות נוספות (יצירתיות)
# ==========================================

def test_same_message_different_passwords():
    """בדיקה שאותה הודעה עם סיסמאות שונות מייצרת תוצאות שונות"""
    # TODO: השלם בדיקה זו
    pass


def test_key_consistency():
    """בדיקה שאותה סיסמה מייצרת תמיד אותו מפתח"""
    # TODO: השלם בדיקה זו
    pass


def test_case_sensitivity():
    """בדיקת רגישות לאותיות גדולות/קטנות"""
    # TODO: האם "SECRET" ו-"secret" מייצרות אותו מפתח?
    pass


# ==========================================
# הרצה ישירה
# ==========================================

if __name__ == "__main__":
    print("=" * 60)
    print("🕵️  SECRET CIPHER TEST SUITE 🕵️")
    print("=" * 60)
    print("\nRunning tests...\n")
    
    # הרץ את כל הבדיקות
    pytest.main([__file__, "-v", "--tb=short"])
    
    print("\n" + "=" * 60)
    print("For detailed coverage report, run:")
    print("pytest test_secret_cipher.py --cov=secret_cipher --cov-report=html")
    print("=" * 60)
