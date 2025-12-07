"""
Secret Cipher System - Recovered from The Phantom's Lab
Mission: Golden Key
WARNING: Not verified - Use with extreme caution

This code was recovered from an international crime organization.
Your mission: Write comprehensive tests to verify it works correctly.
"""


def create_key_from_password(password):
    """
    המרת סיסמה טקסטואלית למפתח מספרי
    
    Args:
        password (str): סיסמה טקסטואלית
        
    Returns:
        list: רשימת אינדקסים המייצגת את סדר העמודות
        
    Example:
        >>> create_key_from_password("ZEBRA")
        [4, 1, 0, 3, 2]
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    if not password.replace(" ", "").isalnum():
        raise ValueError("Password must contain only alphanumeric characters")
    
    # יצירת רשימת טאפלים: (index, char)
    indexed_chars = list(enumerate(password))
    
    # מיון לפי התו, שמירת האינדקס המקורי
    sorted_chars = sorted(indexed_chars, key=lambda x: x[1])
    
    # יצירת רשימת המפתח - סדר הקריאה של העמודות
    key_order = [original_index for original_index, char in sorted_chars]
    
    return key_order


def encrypt_message(message, password):
    """
    הצפנת הודעה באמצעות Transposition Cipher עם סיסמה
    
    Args:
        message (str): ההודעה להצפנה
        password (str): סיסמת ההצפנה
        
    Returns:
        str: ההודעה המוצפנת
        
    Raises:
        ValueError: אם הסיסמה או ההודעה לא תקינות
    """
    if not message:
        raise ValueError("Message cannot be empty")
    
    if len(password) < 2:
        raise ValueError("Password must be at least 2 characters")
    
    key_order = create_key_from_password(password)
    cols = len(password)
    rows = (len(message) + cols - 1) // cols
    
    # הוספת רווחים למילוי המטריצה
    padded_message = message.ljust(rows * cols, " ")
    
    # יצירת מטריצה
    matrix = []
    for row in range(rows):
        matrix_row = []
        for col in range(cols):
            index = row * cols + col
            matrix_row.append(padded_message[index])
        matrix.append(matrix_row)
    
    # קריאה לפי סדר המפתח
    cipher_text = ""
    for key_pos in range(cols):
        # מציאת העמודה המתאימה למיקום הנוכחי במפתח
        col_to_read = key_order.index(key_pos)
        for row in range(rows):
            cipher_text += matrix[row][col_to_read]
    
    return cipher_text


def decrypt_message(cipher_text, password):
    """
    פענוח הודעה שהוצפנה באמצעות Transposition Cipher
    
    Args:
        cipher_text (str): ההודעה המוצפנת
        password (str): סיסמת הפענוח (זהה להצפנה)
        
    Returns:
        str: ההודעה המקורית (ללא רווחי מילוי)
        
    Raises:
        ValueError: אם הסיסמה או הטקסט המוצפן לא תקינים
    """
    if not cipher_text:
        raise ValueError("Cipher text cannot be empty")
    
    if len(password) < 2:
        raise ValueError("Password must be at least 2 characters")
    
    key_order = create_key_from_password(password)
    cols = len(password)
    rows = len(cipher_text) // cols
    
    # יצירת מטריצה ריקה
    matrix = [["" for _ in range(cols)] for _ in range(rows)]
    
    # מילוי המטריצה לפי סדר המפתח
    char_index = 0
    for key_pos in range(cols):
        col_to_fill = key_order.index(key_pos)
        for row in range(rows):
            matrix[row][col_to_fill] = cipher_text[char_index]
            char_index += 1
    
    # קריאת המטריצה שורה אחרי שורה
    decrypted = ""
    for row in matrix:
        decrypted += "".join(row)
    
    return decrypted.rstrip()  # הסרת רווחי מילוי


if __name__ == "__main__":
    # דוגמה לשימוש
    print("=== Secret Cipher System Demo ===\n")
    
    message = "ATTACK AT DAWN"
    password = "SECRET"
    
    print(f"Original Message: {message}")
    print(f"Password: {password}")
    print(f"Key Order: {create_key_from_password(password)}")
    
    encrypted = encrypt_message(message, password)
    print(f"\nEncrypted: {encrypted}")
    
    decrypted = decrypt_message(encrypted, password)
    print(f"Decrypted: {decrypted}")
    
    if message == decrypted:
        print("\n✓ Encryption/Decryption successful!")
    else:
        print("\n✗ Something went wrong!")
