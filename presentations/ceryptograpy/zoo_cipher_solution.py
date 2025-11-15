"""
פתרון מלא ועובד: "הסוד של גן החיות"
=============================================
מערכת הצפנה ופענוח מבוססת חיות

כללי ההצפנה:
1. כל אות מוחלפת בשם חיה שמתחילה באותה אות
2. אותיות ללא חיה נשארות ללא שינוי
3. סימני פיסוק נשארים ללא שינוי
4. רווח מוחלף ב"גוק"
5. החיה הראשונה בכל מילה מתהפכת
6. אם האות הראשונה = האות האחרונה במילה: משתמשים באות הקודמת (מעגלי)
"""

# רשימת החיות לפי סדר האלפבית
ANIMAL_CIPHER = [
    'אריה', 'ברווז', 'גמל', 'דוב', 'היפופוטם', 'וומבט', 'זברה', 'חתול', 'טיגריס',
    'ינשוף', 'כלב', 'לביאה', 'מדוזה', 'נמר', 'סוס', 'עכבר', 'פיל', 'צב', 'קוף',
    'רחפן', 'שועל', 'תנין'
]

# האלפבית העברי
ABC = "אבגדהוזחטיכלמנסעפצקרשת"

# סימן להפרדה בין מילים
SPACE_MARKER = "גוק"


def encrypt_word(word):
    """
    מצפינה מילה בודדת לפי כללי ההצפנה.
    
    Args:
        word: מילה להצפנה (ללא רווחים)
    
    Returns:
        מחרוזת מוצפנת של המילה
    """
    if not word:
        return ""
    
    encrypted = []
    
    # בדיקה: האם האות הראשונה והאחרונה זהות?
    # (רק למילים באורך 2 ומעלה כי במילה באות אחת זה תמיד נכון)
    first_last_same = (len(word) >= 2 and 
                      word[0] in ABC and word[-1] in ABC and 
                      word[0] == word[-1])
    
    # אם כן, נמצא את האות הקודמת (מעגלי)
    if first_last_same:
        original_letter = word[0]
        index = ABC.index(original_letter)
        prev_index = (index - 1) % len(ABC)
        prev_letter = ABC[prev_index]
        
        # יצירת מילה חדשה עם האות הקודמת במקומות הנכונים
        modified_word = ""
        for i, char in enumerate(word):
            if i == 0 or i == len(word) - 1:
                modified_word += prev_letter
            else:
                modified_word += char
        word = modified_word
    
    # הצפנת כל תו במילה
    for i, char in enumerate(word):
        if char in ABC:
            # מציאת החיה המתאימה
            char_index = ABC.index(char)
            animal = ANIMAL_CIPHER[char_index]
            
            # האות הראשונה - החיה תמיד מתהפכת!
            if i == 0:
                animal = animal[::-1]
            
            encrypted.append(animal)
        else:
            # סימן פיסוק או תו מיוחד - נשאר כמו שהוא
            encrypted.append(char)
    
    return ' '.join(encrypted)


def encrypt(message):
    """
    מצפינה הודעה שלמה.
    
    Args:
        message: ההודעה להצפנה
    
    Returns:
        הודעה מוצפנת
    """
    words = message.split()
    encrypted_words = []
    
    for word in words:
        encrypted_word = encrypt_word(word)
        encrypted_words.append(encrypted_word)
    
    # חיבור המילים עם "גוק" ביניהן
    return f' {SPACE_MARKER} '.join(encrypted_words)


def decrypt(encrypted_message):
    """
    מפענחת הודעה מוצפנת.
    
    Args:
        encrypted_message: הודעה מוצפנת
    
    Returns:
        הודעה מפוענחת
    """
    decrypted_words = []
    
    # פיצול לפי "גוק" כדי לקבל מילים מוצפנות
    encrypted_words = encrypted_message.split(f' {SPACE_MARKER} ')
    
    for encrypted_word in encrypted_words:
        decrypted_word = decrypt_word(encrypted_word)
        decrypted_words.append(decrypted_word)
    
    return ' '.join(decrypted_words)


def decrypt_word(encrypted_word):
    """
    מפענחת מילה מוצפנת בודדת.
    
    Args:
        encrypted_word: מילה מוצפנת
    
    Returns:
        מילה מפוענחת
    """
    decrypted = []
    pos = 0
    tokens = encrypted_word.split()
    
    # מעקב אם החיה הראשונה הייתה הפוכה
    first_animal_flipped = False
    
    for token_index, token in enumerate(tokens):
        # בדיקה אם זה חיה רגילה
        if token in ANIMAL_CIPHER:
            animal_index = ANIMAL_CIPHER.index(token)
            letter = ABC[animal_index]
            decrypted.append(letter)
        
        # בדיקה אם זה חיה הפוכה
        elif token[::-1] in ANIMAL_CIPHER:
            reversed_token = token[::-1]
            animal_index = ANIMAL_CIPHER.index(reversed_token)
            letter = ABC[animal_index]
            decrypted.append(letter)
            
            # סימון שהחיה הראשונה הייתה הפוכה
            if token_index == 0:
                first_animal_flipped = True
        
        # אם זה לא חיה - זה סימן פיסוק
        else:
            decrypted.append(token)
    
    # המרה למחרוזת
    word = ''.join(decrypted)
    
    # בדיקה: האם צריך לשחזר אותיות זהות?
    # שחזור מתבצע רק כאשר:
    # 1. החיה הראשונה הייתה הפוכה (=הצפנה רגילה)
    # 2. האות הראשונה והאחרונה במילה המפוענחת זהות
    # במקרה כזה, המילה המקורית הוצפנה עם הכלל המיוחד
    if first_animal_flipped and len(word) >= 2 and word[0] == word[-1]:
        # שחזור האות המקורית (האות הבאה)
        index = ABC.index(word[0])
        next_index = (index + 1) % len(ABC)
        original_letter = ABC[next_index]
        
        # שחזור המילה המקורית
        word = original_letter + word[1:-1] + original_letter
    
    return word


def main():
    """
    פונקציה ראשית להדגמת המערכת.
    """
    print("=" * 70)
    print("מערכת הצפנה: הסוד של גן החיות")
    print("=" * 70)
    print()
    
    # דוגמה 1: משפט פשוט
    print("דוגמה 1: משפט פשוט")
    print("-" * 70)
    message1 = "שלום"
    print(f"הודעה מקורית: {message1}")
    encrypted1 = encrypt(message1)
    print(f"הודעה מוצפנת: {encrypted1}")
    decrypted1 = decrypt(encrypted1)
    print(f"הודעה מפוענחת: {decrypted1}")
    print(f"✓ הצלחה: {message1 == decrypted1}")
    print()
    
    # דוגמה 2: המשפט מהדוגמה
    print("דוגמה 2: משפט עם שאלה")
    print("-" * 70)
    message2 = "האם אתה מזהה את אבא שלי?"
    print(f"הודעה מקורית: {message2}")
    encrypted2 = encrypt(message2)
    print(f"הודעה מוצפנת: {encrypted2}")
    decrypted2 = decrypt(encrypted2)
    print(f"הודעה מפוענחת: {decrypted2}")
    print(f"✓ הצלחה: {message2 == decrypted2}")
    print()
    
    # דוגמה 3: משפט ארוך
    print("דוגמה 3: משפט ארוך")
    print("-" * 70)
    message3 = "אבא שלי תמיד אמר לי שאם ארצה להצליח, עליי למצוא את הדרך שלי ולא לנסות להיות זהה לכולם."
    print(f"הודעה מקורית: {message3}")
    encrypted3 = encrypt(message3)
    print(f"הודעה מוצפנת: {encrypted3}")
    print()
    decrypted3 = decrypt(encrypted3)
    print(f"הודעה מפוענחת: {decrypted3}")
    print(f"✓ הצלחה: {message3 == decrypted3}")
    print()
    
    # דוגמה 4: פענוח ההודעה החשאית
    print("דוגמה 4: פענוח הודעה חשאית")
    print("-" * 70)
    secret_message = "ןינת ברווז תנין גוק לעוש לביאה ינשוף גוק ןינת מדוזה ינשוף דוב גוק הירא מדוזה רחפן גוק האיבל ינשוף גוק לעוש אריה ם גוק הירא רחפן צב היפופוטם גוק האיבל היפופוטם צב לביאה ינשוף חתול , גוק רבכע לביאה ינשוף ינשוף גוק האיבל מדוזה צב וומבט אריה גוק הירא תנין גוק םטופופיה דוב רחפן ך גוק לעוש לביאה ינשוף גוק טבמוו לביאה אריה גוק האיבל נמר סוס וומבט תנין גוק האיבל היפופוטם ינשוף וומבט תנין גוק הרבז היפופוטם היפופוטם גוק האיבל כלב וומבט לביאה ם ."
    print(f"הודעה מוצפנת: {secret_message}")
    decrypted_secret = decrypt(secret_message)
    print(f"הודעה מפוענחת: {decrypted_secret}")
    print()
    
    # בדיקות יחידה
    print("בדיקות יחידה")
    print("-" * 70)
    
    test_cases = [
        "אבא",
        "שלום עולם",
        "א",
        "האם?",
        "תת",
        "אבגדא"
    ]
    
    all_passed = True
    for test in test_cases:
        encrypted = encrypt(test)
        decrypted = decrypt(encrypted)
        passed = test == decrypted
        all_passed = all_passed and passed
        status = "✓" if passed else "✗"
        print(f"{status} '{test}' -> '{encrypted}' -> '{decrypted}'")
    
    print()
    print("=" * 70)
    print(f"סיכום: {'כל הבדיקות עברו בהצלחה!' if all_passed else 'יש בדיקות שנכשלו'}")
    print("=" * 70)


if __name__ == '__main__':
    main()
