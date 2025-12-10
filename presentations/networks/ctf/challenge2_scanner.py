import socket


def scan_port(host, port):
    """סריקת פורט בודד וקבלת תגובה"""
    try:
        # יצירת socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        # נסיון חיבור
        result = sock.connect_ex((host, port))

        if result == 0:
            print(f"✅ פורט {port} פתוח!")

            # שליחת בקשה וקבלת תגובה
            try:
                sock.send(b"GET INFO\n")
                response = sock.recv(1024).decode('utf-8', errors='ignore')
                print(f"   📨 תגובה: {response.strip()}")

                # בדיקה אם זה חלק מהדגל
                if "SECRET_PART" in response:
                    print(f"🔐 נמצא חלק דגל בפורט {port}!")
                    return response.strip()

            except Exception as e:
                print(f"   ❌ שגיאה בקבלת תגובה: {e}")

        sock.close()
        return None

    except Exception:
        return None


def main():
    host = "127.0.0.1"
    start_port = 8000
    end_port = 8100

    flag_parts = []

    print("=" * 60)
    print(f"🔍 סורק פורטים בטווח {start_port}-{end_port} על {host}")
    print("=" * 60)
    print()

    for port in range(start_port, end_port + 1):
        result = scan_port(host, port)
        if result and "SECRET_PART" in result:
            flag_parts.append(result)

    print()
    print("=" * 60)
    print(f"🎯 נמצאו {len(flag_parts)} חלקי דגל:")
    for i, part in enumerate(flag_parts, 1):
        print(f"   {i}. {part}")
    print("=" * 60)

    if len(flag_parts) == 2:
        print()
        print("💡 עכשיו הרכב את שני החלקים והגש את הדגל המלא!")


def caesar_decrypt(ciphertext, shift):
    result = ""

    for char in ciphertext:
        if char.isalpha():
            # קביעת בסיס לפי אותיות גדולות או קטנות
            base = ord('A') if char.isupper() else ord('a')
            # פענוח על ידי הזזה אחורה
            decrypted_char = chr((ord(char) - base - shift) % 26 + base)
            result += decrypted_char
        else:
            # תווים שאינם אותיות נשארים ללא שינוי
            result += char

    return result

def print_possible_flags():
    first_part = "FLAG{h1dd3n_p0rt"
    part2_encrypted = "xh9ss8w_r9xy8w"

    for key in range (-1, -26, -1):
        possible_flag = first_part + "_" + caesar_decrypt(part2_encrypted, key) + "}"
        print(f"key: {key}, possible_flag: {possible_flag}")


if __name__ == "__main__":
    main()
    print_possible_flags()



    """
    FLAG{h1dd3n_p0rt
    
    xh9ss8w_r9xy8w
    
    """