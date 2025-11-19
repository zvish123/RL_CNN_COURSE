#!/usr/bin/env python3
"""
סקריפט ליצירת hash לדגלים חדשים
להריץ: python3 generate_flag_hash.py
"""

import hashlib

def generate_hash(flag):
    """יוצר SHA-256 hash לדגל"""
    return hashlib.sha256(flag.encode()).hexdigest()

def main():
    print("=" * 60)
    print("🔐 מחולל Hash לדגלי CTF")
    print("=" * 60)
    print("\nהכנס את הדגל שברצונך להצפין (או 'exit' לסיום):")
    
    while True:
        flag = input("\nדגל: ").strip()
        
        if flag.lower() == 'exit':
            print("להתראות! 👋")
            break
        
        if not flag:
            print("❌ אנא הכנס דגל תקין")
            continue
        
        # המרה לאותיות גדולות (אופציונלי)
        flag_upper = flag.upper()
        
        # יצירת hash
        hash_value = generate_hash(flag_upper)
        
        print(f"\n✅ Hash נוצר בהצלחה!")
        print(f"   דגל: {flag_upper}")
        print(f"   Hash: {hash_value}")
        print(f"\n📋 העתק את זה לקוד ה-HTML:")
        print(f'   "{hash_value}", // {flag_upper}')

if __name__ == "__main__":
    # דוגמאות
    print("\n💡 דוגמאות לדגלים:")
    examples = [
        "FLAG{4_22_6}",
        "FLAG{FOUR_TWENTYTWO_SIX}",
        "FLAG{TEST_123}"
    ]
    
    for example in examples:
        print(f"   {example} -> {generate_hash(example)}")
    
    print("\n" + "=" * 60)
    main()
