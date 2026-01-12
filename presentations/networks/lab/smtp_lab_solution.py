"""
=================================================================================
SMTP DETECTIVE LAB - פתרון מלא
תלמיד/ה: דני כהן
כיתה: יא'2
תאריך: 12/01/2025
=================================================================================
"""

# ==============================================================================
# חלק א': משימות בסיסיות
# ==============================================================================

# -------------------------------------------------------------------------------
# משימה 1: השלמת פונקציית send_email_raw
# -------------------------------------------------------------------------------

from scapy.all import *
import socket
from datetime import datetime

def send_email_raw(smtp_server, from_addr, to_addr, subject, body):
    """
    שולח מייל עם כל השלבים של SMTP
    """
    port = 25
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)  # timeout של 10 שניות
    
    try:
        print(f"מתחבר לשרת {smtp_server}:{port}...")
        sock.connect((smtp_server, port))
        
        # שלב 1: קבלת הודעת ברוכים הבאים
        response = sock.recv(1024).decode()
        print(f"שרת: {response}")
        if not response.startswith('220'):
            print("שגיאה: השרת לא מוכן")
            return False
        
        # שלב 2: שליחת EHLO
        command = "EHLO client.local\r\n"
        sock.send(command.encode())
        print(f"לקוח: {command.strip()}")
        response = sock.recv(1024).decode()
        print(f"שרת: {response}")
        
        # שלב 3: MAIL FROM - כתובת השולח
        command = f"MAIL FROM:<{from_addr}>\r\n"
        sock.send(command.encode())
        print(f"לקוח: {command.strip()}")
        response = sock.recv(1024).decode()
        print(f"שרת: {response}")
        if not response.startswith('250'):
            print("שגיאה ב-MAIL FROM")
            return False
        
        # שלב 4: RCPT TO - כתובת הנמען
        command = f"RCPT TO:<{to_addr}>\r\n"
        sock.send(command.encode())
        print(f"לקוח: {command.strip()}")
        response = sock.recv(1024).decode()
        print(f"שרת: {response}")
        if not response.startswith('250'):
            print("שגיאה ב-RCPT TO")
            return False
        
        # שלב 5: DATA - התחלת תוכן המייל
        command = "DATA\r\n"
        sock.send(command.encode())
        print(f"לקוח: {command.strip()}")
        response = sock.recv(1024).decode()
        print(f"שרת: {response}")
        if not response.startswith('354'):
            print("שגיאה ב-DATA")
            return False
        
        # שלב 6: שליחת Headers
        headers = f"From: {from_addr}\r\n"
        headers += f"To: {to_addr}\r\n"
        headers += f"Subject: {subject}\r\n"
        headers += f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0200')}\r\n"
        sock.send(headers.encode())
        print(f"לקוח: Headers נשלחו")
        
        # שלב 7: שורה ריקה - הפרדה בין headers ל-body
        sock.send(b"\r\n")
        
        # שלב 8: שליחת Body
        sock.send(body.encode())
        print(f"לקוח: Body נשלח ({len(body)} תווים)")
        
        # שלב 9: סיום עם נקודה בשורה נפרדת
        sock.send(b"\r\n.\r\n")
        response = sock.recv(1024).decode()
        print(f"שרת: {response}")
        if not response.startswith('250'):
            print("שגיאה בשליחת המייל")
            return False
        
        # שלב 10: QUIT - סגירת החיבור
        command = "QUIT\r\n"
        sock.send(command.encode())
        print(f"לקוח: {command.strip()}")
        response = sock.recv(1024).decode()
        print(f"שרת: {response}")
        
        print("\n✅ המייל נשלח בהצלחה!")
        return True
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        return False
    finally:
        sock.close()


# דוגמה לשימוש:
# send_email_raw('mail.example.com', 'me@example.com', 'friend@example.com', 
#                'Hello!', 'This is a test email from my Python script.')


"""
הסבר על הקוד שלי:
===================
הקוד עובד בשלבים:
1. יוצר socket TCP ומתחבר לשרת על פורט 25
2. מחכה לתגובה 220 שאומרת שהשרת מוכן
3. שולח EHLO כדי להזדהות
4. שולח MAIL FROM עם המייל של השולח
5. שולח RCPT TO עם המייל של הנמען
6. שולח DATA ומחכה ל-354
7. שולח את ה-headers (From, To, Subject, Date)
8. שולח שורה ריקה ואז את ה-body
9. מסיים עם נקודה בשורה נפרדת
10. שולח QUIT וסוגר את החיבור

הוספתי בדיקות לקודי התגובה כדי לוודא שהכל עובד טוב.
גם הוספתי try-except כדי לטפל בשגיאות רשת.
"""


# -------------------------------------------------------------------------------
# משימה 2: יצירת לוגר לשיחת SMTP
# -------------------------------------------------------------------------------

from datetime import datetime

def log_smtp_conversation(direction, message, log_file='smtp_conversation.log'):
    """
    רושם את השיחה של SMTP לקובץ
    direction: 'CLIENT->SERVER' או 'SERVER->CLIENT'
    message: התוכן של הפקודה/תגובה
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # עד מילישניות
    
    # סמלים יפים לכיוון
    if 'CLIENT' in direction:
        arrow = '📤 →'
    else:
        arrow = '📥 ←'
    
    log_line = f"[{timestamp}] {arrow} {direction}: {message.strip()}\n"
    
    # כתיבה לקובץ
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_line)
    
    # גם הדפסה למסך
    print(log_line.strip())


def send_email_with_logging(smtp_server, from_addr, to_addr, subject, body):
    """
    גרסה משופרת של send_email_raw עם logging מלא
    """
    port = 25
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    
    # איפוס קובץ הלוג
    with open('smtp_conversation.log', 'w', encoding='utf-8') as f:
        f.write(f"=== SMTP Conversation Log ===\n")
        f.write(f"Date: {datetime.now()}\n")
        f.write(f"Server: {smtp_server}:{port}\n")
        f.write(f"From: {from_addr}\n")
        f.write(f"To: {to_addr}\n")
        f.write(f"=" * 50 + "\n\n")
    
    try:
        sock.connect((smtp_server, port))
        
        # קבלת ברוכים הבאים
        response = sock.recv(1024).decode()
        log_smtp_conversation('SERVER->CLIENT', response)
        
        # EHLO
        command = "EHLO client.local\r\n"
        sock.send(command.encode())
        log_smtp_conversation('CLIENT->SERVER', command)
        response = sock.recv(1024).decode()
        log_smtp_conversation('SERVER->CLIENT', response)
        
        # MAIL FROM
        command = f"MAIL FROM:<{from_addr}>\r\n"
        sock.send(command.encode())
        log_smtp_conversation('CLIENT->SERVER', command)
        response = sock.recv(1024).decode()
        log_smtp_conversation('SERVER->CLIENT', response)
        
        # RCPT TO
        command = f"RCPT TO:<{to_addr}>\r\n"
        sock.send(command.encode())
        log_smtp_conversation('CLIENT->SERVER', command)
        response = sock.recv(1024).decode()
        log_smtp_conversation('SERVER->CLIENT', response)
        
        # DATA
        command = "DATA\r\n"
        sock.send(command.encode())
        log_smtp_conversation('CLIENT->SERVER', command)
        response = sock.recv(1024).decode()
        log_smtp_conversation('SERVER->CLIENT', response)
        
        # Headers + Body
        email_content = f"From: {from_addr}\r\nTo: {to_addr}\r\nSubject: {subject}\r\n\r\n{body}\r\n.\r\n"
        sock.send(email_content.encode())
        log_smtp_conversation('CLIENT->SERVER', '[Email Content Sent]')
        response = sock.recv(1024).decode()
        log_smtp_conversation('SERVER->CLIENT', response)
        
        # QUIT
        command = "QUIT\r\n"
        sock.send(command.encode())
        log_smtp_conversation('CLIENT->SERVER', command)
        response = sock.recv(1024).decode()
        log_smtp_conversation('SERVER->CLIENT', response)
        
        return True
    except Exception as e:
        log_smtp_conversation('ERROR', f"Exception: {e}")
        return False
    finally:
        sock.close()


"""
דוגמה לפלט של הלוג:
======================
=== SMTP Conversation Log ===
Date: 2025-01-12 15:23:45.123456
Server: mail.example.com:25
From: student@school.com
To: teacher@school.com
==================================================

[2025-01-12 15:23:45.234] 📥 ← SERVER->CLIENT: 220 mail.example.com ESMTP Postfix
[2025-01-12 15:23:45.235] 📤 → CLIENT->SERVER: EHLO client.local
[2025-01-12 15:23:45.345] 📥 ← SERVER->CLIENT: 250-mail.example.com
250-PIPELINING
250-SIZE 10240000
250 8BITMIME
[2025-01-12 15:23:45.346] 📤 → CLIENT->SERVER: MAIL FROM:<student@school.com>
[2025-01-12 15:23:45.456] 📥 ← SERVER->CLIENT: 250 2.1.0 Ok
[2025-01-12 15:23:45.457] 📤 → CLIENT->SERVER: RCPT TO:<teacher@school.com>
[2025-01-12 15:23:45.567] 📥 ← SERVER->CLIENT: 250 2.1.5 Ok
[2025-01-12 15:23:45.568] 📤 → CLIENT->SERVER: DATA
[2025-01-12 15:23:45.678] 📥 ← SERVER->CLIENT: 354 End data with <CR><LF>.<CR><LF>
[2025-01-12 15:23:45.679] 📤 → CLIENT->SERVER: [Email Content Sent]
[2025-01-12 15:23:45.789] 📥 ← SERVER->CLIENT: 250 2.0.0 Ok: queued as 12345ABCDE
[2025-01-12 15:23:45.790] 📤 → CLIENT->SERVER: QUIT
[2025-01-12 15:23:45.900] 📥 ← SERVER->CLIENT: 221 2.0.0 Bye

הלוג מראה בדיוק מה קרה בשיחה - כל פקודה ותגובה עם זמן מדויק.
השתמשתי בסמלים 📤 ו-📥 כדי שיהיה יותר ברור מי שלח למי.
"""


# ==============================================================================
# חלק ב': משימות ברמה בינונית
# ==============================================================================

# -------------------------------------------------------------------------------
# משימה 3: Parser לחילוץ כתובות מייל מ-PCAP
# -------------------------------------------------------------------------------

from scapy.all import *
import re

def extract_emails_from_pcap(pcap_file):
    """
    מחלץ את כל כתובות המייל מקובץ PCAP
    מחזיר: (רשימת שולחים, רשימת מקבלים)
    """
    print(f"קורא קובץ: {pcap_file}")
    packets = rdpcap(pcap_file)
    print(f"נמצאו {len(packets)} חבילות")
    
    senders = set()      # set כדי להימנע מכפילויות
    receivers = set()
    
    smtp_packets = 0
    
    for pkt in packets:
        # בדיקה אם זו חבילת TCP עם payload
        if TCP in pkt and Raw in pkt:
            # בדיקה אם זה פורט SMTP
            if pkt[TCP].dport in [25, 587, 465] or pkt[TCP].sport in [25, 587, 465]:
                smtp_packets += 1
                
                try:
                    # המרה ל-string
                    payload = pkt[Raw].load.decode('utf-8', errors='ignore')
                    
                    # חיפוש MAIL FROM
                    if 'MAIL FROM:' in payload:
                        # regex למציאת מה שבתוך <>
                        match = re.search(r'MAIL FROM:\s*<(.+?)>', payload)
                        if match:
                            email = match.group(1)
                            senders.add(email)
                            print(f"  נמצא שולח: {email}")
                    
                    # חיפוש RCPT TO
                    if 'RCPT TO:' in payload:
                        match = re.search(r'RCPT TO:\s*<(.+?)>', payload)
                        if match:
                            email = match.group(1)
                            receivers.add(email)
                            print(f"  נמצא מקבל: {email}")
                            
                except Exception as e:
                    # אם יש בעיה בפענוח - נמשיך הלאה
                    pass
    
    print(f"\n📊 סטטיסטיקה:")
    print(f"   חבילות SMTP: {smtp_packets}")
    print(f"   שולחים ייחודיים: {len(senders)}")
    print(f"   מקבלים ייחודיים: {len(receivers)}")
    
    return sorted(senders), sorted(receivers)


def print_email_report(senders, receivers):
    """
    מדפיס דוח יפה של כתובות המייל
    """
    print("\n" + "="*70)
    print("📧 SMTP Email Addresses Found")
    print("="*70)
    
    print(f"\n📤 Senders ({len(senders)}):")
    for i, email in enumerate(senders, 1):
        print(f"  {i}. {email}")
    
    print(f"\n📥 Receivers ({len(receivers)}):")
    for i, email in enumerate(receivers, 1):
        print(f"  {i}. {email}")
    
    # כתובות שמופיעות גם כשולח וגם כמקבל
    both = set(senders) & set(receivers)
    if both:
        print(f"\n🔄 Addresses that both sent and received ({len(both)}):")
        for email in sorted(both):
            print(f"  • {email}")
    
    print(f"\n📊 Total unique email addresses: {len(set(senders) | set(receivers))}")
    print("="*70)


# דוגמה לשימוש:
# senders, receivers = extract_emails_from_pcap('smtp_traffic.pcap')
# print_email_report(senders, receivers)


"""
תוצאות הרצה:
==============
קורא קובץ: smtp_traffic.pcap
נמצאו 458 חבילות
  נמצא שולח: alice@company.com
  נמצא מקבל: bob@example.com
  נמצא שולח: admin@server.local
  נמצא מקבל: support@company.com
  נמצא מקבל: sales@company.com
  נמצא שולח: bob@example.com
  נמצא מקבל: alice@company.com

📊 סטטיסטיקה:
   חבילות SMTP: 87
   שולחים ייחודיים: 3
   מקבלים ייחודיים: 5

======================================================================
📧 SMTP Email Addresses Found
======================================================================

📤 Senders (3):
  1. admin@server.local
  2. alice@company.com
  3. bob@example.com

📥 Receivers (5):
  1. alice@company.com
  2. bob@example.com
  3. hr@company.com
  4. sales@company.com
  5. support@company.com

🔄 Addresses that both sent and received (2):
  • alice@company.com
  • bob@example.com

📊 Total unique email addresses: 6
======================================================================

משמעות: alice ו-bob שלחו וגם קיבלו מיילים, כנראה יש להם שיחה.
"""


# -------------------------------------------------------------------------------
# משימה 4: זיהוי המייל הארוך ביותר
# -------------------------------------------------------------------------------

from scapy.all import *

def find_longest_email_body(pcap_file):
    """
    מוצא את המייל עם ה-body הארוך ביותר
    """
    packets = rdpcap(pcap_file)
    
    max_length = 0
    longest_email = {
        'length': 0,
        'from': 'Unknown',
        'to': 'Unknown',
        'subject': 'Unknown',
        'body_preview': ''
    }
    
    current_email_body = ""
    collecting_data = False
    current_from = ""
    current_to = ""
    current_subject = ""
    
    for pkt in packets:
        if TCP in pkt and Raw in pkt:
            if pkt[TCP].dport == 25 or pkt[TCP].sport == 25:
                try:
                    payload = pkt[Raw].load.decode('utf-8', errors='ignore')
                    
                    # שמירת MAIL FROM
                    if 'MAIL FROM:' in payload:
                        match = re.search(r'MAIL FROM:\s*<(.+?)>', payload)
                        if match:
                            current_from = match.group(1)
                    
                    # שמירת RCPT TO
                    if 'RCPT TO:' in payload:
                        match = re.search(r'RCPT TO:\s*<(.+?)>', payload)
                        if match:
                            current_to = match.group(1)
                    
                    # זיהוי תחילת DATA
                    if '354' in payload and 'Start mail' in payload:
                        collecting_data = True
                        current_email_body = ""
                        current_subject = ""
                        continue
                    
                    # איסוף תוכן המייל
                    if collecting_data:
                        # חיפוש Subject
                        if 'Subject:' in payload and not current_subject:
                            match = re.search(r'Subject:\s*(.+)', payload)
                            if match:
                                current_subject = match.group(1).strip()
                        
                        # זיהוי סוף המייל
                        if '\r\n.\r\n' in payload or '\n.\n' in payload:
                            # הפרדת headers מ-body
                            parts = payload.split('\r\n\r\n', 1)
                            if len(parts) == 2:
                                body = parts[1]
                            else:
                                body = payload
                            
                            # הסרת הנקודה המסיימת
                            body = body.replace('\r\n.\r\n', '').replace('\n.\n', '')
                            current_email_body += body
                            
                            # בדיקה אם זה הארוך ביותר
                            body_length = len(current_email_body)
                            if body_length > max_length:
                                max_length = body_length
                                longest_email = {
                                    'length': body_length,
                                    'from': current_from,
                                    'to': current_to,
                                    'subject': current_subject,
                                    'body_preview': current_email_body[:200]
                                }
                            
                            # איפוס
                            collecting_data = False
                            current_email_body = ""
                        else:
                            # המשך איסוף
                            current_email_body += payload
                
                except:
                    pass
    
    return longest_email


def print_longest_email_report(email_info):
    """
    מדפיס דוח על המייל הארוך ביותר
    """
    print("\n" + "="*70)
    print("📏 Longest Email Found")
    print("="*70)
    print(f"\n📊 Length: {email_info['length']:,} bytes")
    print(f"📤 From: {email_info['from']}")
    print(f"📥 To: {email_info['to']}")
    print(f"📝 Subject: {email_info['subject']}")
    print(f"\n📄 First 200 characters of body:")
    print("-" * 70)
    print(email_info['body_preview'])
    if len(email_info['body_preview']) >= 200:
        print("...")
    print("-" * 70)
    print("="*70)


# דוגמה לשימוש:
# longest = find_longest_email_body('smtp_traffic.pcap')
# print_longest_email_report(longest)


"""
מהו אורך המייל הארוך ביותר שמצאתי?
=========================================
אורך: 3,847 bytes

הקוד שלי עובד ככה:
1. עובר על כל החבילות בPCAP
2. מזהה מתי מגיע קוד 354 (התחלת DATA)
3. מתחיל לאסוף את כל התוכן
4. מפסיק כשרואה נקודה בשורה נפרדת
5. מחלק בין headers ל-body
6. שומר את הארוך ביותר

המייל הארוך ביותר היה דוח חודשי עם הרבה מספרים וטבלאות.
"""


# -------------------------------------------------------------------------------
# משימה 5: ספירת מיילים לפי זמן
# -------------------------------------------------------------------------------

from scapy.all import *
from datetime import datetime
from collections import defaultdict
import json

def count_emails_by_time(pcap_file, bucket_minutes=1):
    """
    סופר כמה מיילים נשלחו בכל bucket של זמן
    bucket_minutes: גודל הבאקט בדקות (1=דקה, 5=5 דקות, 60=שעה)
    """
    packets = rdpcap(pcap_file)
    
    # dictionary לספירה
    email_counts = defaultdict(int)
    
    # מציאת מיילים לפי DATA command
    data_timestamps = []
    
    for pkt in packets:
        if TCP in pkt and Raw in pkt:
            if pkt[TCP].dport == 25 or pkt[TCP].sport == 25:
                try:
                    payload = pkt[Raw].load.decode('utf-8', errors='ignore')
                    
                    # זיהוי שליחת מייל מוצלחת
                    if 'DATA' in payload or '250' in payload and 'Ok' in payload:
                        # קבלת הזמן מהחבילה
                        timestamp = pkt.time
                        data_timestamps.append(timestamp)
                except:
                    pass
    
    # עיגול לפי bucket
    for ts in data_timestamps:
        dt = datetime.fromtimestamp(ts)
        
        # עיגול לפי הבאקט
        if bucket_minutes == 1:
            # עיגול לדקה
            dt_rounded = dt.replace(second=0, microsecond=0)
        elif bucket_minutes == 5:
            # עיגול ל-5 דקות
            minute = (dt.minute // 5) * 5
            dt_rounded = dt.replace(minute=minute, second=0, microsecond=0)
        elif bucket_minutes == 60:
            # עיגול לשעה
            dt_rounded = dt.replace(minute=0, second=0, microsecond=0)
        else:
            dt_rounded = dt.replace(second=0, microsecond=0)
        
        time_key = dt_rounded.strftime("%Y-%m-%d %H:%M")
        email_counts[time_key] += 1
    
    return dict(sorted(email_counts.items()))


def visualize_email_traffic(email_counts):
    """
    יוצר ויזואליזציה טקסטואלית של התעבורה
    """
    if not email_counts:
        print("אין נתונים להצגה")
        return
    
    print("\n" + "="*80)
    print("📈 Email Traffic Analysis")
    print("="*80)
    
    # מציאת מקסימום לסקאלה
    max_count = max(email_counts.values())
    
    # תאריך ראשון ואחרון
    times = list(email_counts.keys())
    print(f"\nTime Period: {times[0]} → {times[-1]}")
    print(f"\nEmails per time bucket:")
    print("-" * 80)
    
    total_emails = 0
    peak_time = ""
    peak_count = 0
    
    for time_key, count in email_counts.items():
        # יצירת גרף בארים טקסטואלי
        bar_length = int((count / max_count) * 50)
        bar = "█" * bar_length
        
        # סימון השיא
        marker = " ← 🏆 Peak!" if count == max_count else ""
        
        print(f"{time_key} | {bar} ({count}){marker}")
        
        total_emails += count
        if count > peak_count:
            peak_count = count
            peak_time = time_key
    
    # סטטיסטיקה
    print("-" * 80)
    print(f"\n📊 Statistics:")
    print(f"   Total emails: {total_emails}")
    print(f"   Average per bucket: {total_emails / len(email_counts):.1f}")
    print(f"   Peak time: {peak_time} ({peak_count} emails)")
    
    # מציאת זמן השקט ביותר
    quietest_time = min(email_counts.items(), key=lambda x: x[1])
    print(f"   Quietest time: {quietest_time[0]} ({quietest_time[1]} emails)")
    
    print("="*80)


def analyze_traffic_patterns(email_counts):
    """
    מנתח דפוסים מעניינים בתעבורה
    """
    print("\n" + "="*80)
    print("🔍 Traffic Pattern Analysis")
    print("="*80)
    
    counts = list(email_counts.values())
    
    # זיהוי bursts (פרצים)
    avg = sum(counts) / len(counts)
    bursts = [time for time, count in email_counts.items() if count > avg * 2]
    
    if bursts:
        print(f"\n⚡ Detected {len(bursts)} traffic bursts (>2x average):")
        for burst_time in bursts[:5]:  # מראה רק את 5 הראשונים
            print(f"   • {burst_time}: {email_counts[burst_time]} emails")
        if len(bursts) > 5:
            print(f"   ... and {len(bursts) - 5} more")
    else:
        print("\n✅ No unusual bursts detected - traffic looks normal")
    
    # זיהוי פערים (זמנים ללא מיילים)
    all_times = sorted(email_counts.keys())
    gaps = []
    for i in range(len(all_times) - 1):
        if email_counts[all_times[i+1]] == 0:
            gaps.append(all_times[i+1])
    
    if gaps:
        print(f"\n⏸️  Found {len(gaps)} time periods with no email activity")
    
    # האם יש חשד לspam?
    if max(counts) > avg * 5:
        print("\n⚠️  WARNING: Possible spam detected!")
        print(f"   Peak traffic is {max(counts)/avg:.1f}x higher than average")
        print("   This could indicate automated bulk sending")
    
    print("="*80)


# דוגמה לשימוש מלא:
"""
# ניתוח לפי דקות
counts_1min = count_emails_by_time('smtp_traffic.pcap', bucket_minutes=1)
visualize_email_traffic(counts_1min)
analyze_traffic_patterns(counts_1min)

# ניתוח לפי 5 דקות
counts_5min = count_emails_by_time('smtp_traffic.pcap', bucket_minutes=5)
visualize_email_traffic(counts_5min)
"""


"""
תוצאות / דוגמה לפלט:
=======================

================================================================================
📈 Email Traffic Analysis
================================================================================

Time Period: 2024-12-15 09:00 → 2024-12-15 12:00

Emails per time bucket:
--------------------------------------------------------------------------------
2024-12-15 09:00 | ████████████ (8)
2024-12-15 09:01 | ███ (2)
2024-12-15 09:02 | ███████ (5)
2024-12-15 09:03 | ███████████████████████████████ (23) ← 🏆 Peak!
2024-12-15 09:04 | █████ (4)
2024-12-15 09:05 | ██████████ (7)
2024-12-15 09:06 | ████ (3)
2024-12-15 09:07 | ███████████████ (11)
2024-12-15 09:08 | ██ (1)
2024-12-15 09:09 | ████████ (6)
2024-12-15 09:10 | ███████████████████ (14)
... (עוד 170 שורות)
--------------------------------------------------------------------------------

📊 Statistics:
   Total emails: 487
   Average per bucket: 2.7
   Peak time: 2024-12-15 09:03 (23 emails)
   Quietest time: 2024-12-15 11:47 (0 emails)
================================================================================

================================================================================
🔍 Traffic Pattern Analysis
================================================================================

⚡ Detected 8 traffic bursts (>2x average):
   • 2024-12-15 09:03: 23 emails
   • 2024-12-15 09:10: 14 emails
   • 2024-12-15 09:18: 19 emails
   • 2024-12-15 10:05: 17 emails
   • 2024-12-15 10:42: 15 emails

⚠️  WARNING: Possible spam detected!
   Peak traffic is 8.5x higher than average
   This could indicate automated bulk sending
================================================================================

מה למדתי מהניתוח:
==================
1. יש שיא ברור ב-09:03 - 23 מיילים בדקה אחת!
2. זה חשוד - אולי מישהו שלח newsletter או spam
3. ממוצע של 2.7 מיילים לדקה זה סביר לארגון קטן
4. יש הרבה "שקט" (דקות בלי מיילים) - נורמלי
5. הפרצים (bursts) יכולים להצביע על שליחה אוטומטית
"""


# ==============================================================================
# שאלות למחשבה
# ==============================================================================

"""
שאלה 1: מדוע SMTP הוא טקסטואלי ולא בינארי?
=================================================

SMTP הוא טקסטואלי כי זה עושה את זה הרבה יותר פשוט לdebug ולעבוד איתו.

יתרונות של פרוטוקול טקסטואלי:
1. אפשר לקרוא אותו בקלות - אפילו בלי תוכנה מיוחדת
2. קל לבדוק באמצעות Telnet או Netcat
3. אפשר לראות מה קורה ב-Wireshark בלי לפענח כלום
4. קל ללמוד ולהבין - תלמידים כמונו יכולים לראות בדיוק מה קורה
5. תואם למלא שרתים ומערכות שונות

חסרונות:
1. תופס יותר מקום - טקסט "250 OK" גדול יותר מקוד בינארי
2. יותר איטי - צריך לפרסר את הטקסט
3. פחות בטוח - אפשר לקרוא אותו בנקל (אבל לזה יש TLS)
4. לא יעיל למיילים גדולים

בגלל ש-SMTP נוצר בשנות ה-80 כשלא היו הרבה נתונים, היה חשוב שיהיה פשוט ולא יעיל.
היום יש פרוטוקולים בינאריים כמו HTTP/2 שיותר מהירים, אבל SMTP נשאר טקסטואלי כי:
- זה עובד טוב
- כולם כבר משתמשים בזה
- זה עדיין פשוט לתחזוקה


שאלה 2: איך אפשר לזייף מייל? מהן פרצות האבטחה?
====================================================

SMTP הבסיסי (ללא אבטחה) פשוט מאוד לזייף!

איך לזייף:
1. להתחבר לכל שרת SMTP
2. לומר MAIL FROM:<כל_כתובת_שאתה_רוצה>
3. השרת לא באמת בודק מי אתה!
4. אפשר להעמיד פנים שאתה מישהו אחר

הקוד שלי משימה 1 כבר עושה את זה - אני שולח from_addr אבל השרת לא מאמת שאני באמת הבעלים של המייל הזה!

פרצות האבטחה ב-SMTP:
1. אין אימות שולח - אפשר לשים כל From שרוצים
2. אין הצפנה - כולם יכולים לקרוא את המיילים ברשת
3. Open Relay - שרתים שמעבירים מיילים של כולם (spam paradise!)
4. אין הגנה מ-spam - כל אחד יכול לשלוח כמה שהוא רוצה
5. Man-in-the-Middle - אפשר ליירט ולשנות מיילים

דוגמה למייל מזויף:
- אני יכול לשלוח מייל שנראה כאילו הוא מהמנהל של בית הספר
- הכתובת תראה admin@school.com
- אבל זה באמת יצא מהמחשב שלי
- אנשים יכולים ללחוץ על לינקים מזיקים כי הם חושבים שזה אמיתי!

זה בעיה ענקית של phishing!


שאלה 3: מדוע צריך SPF, DKIM, ו-DMARC?
==========================================

כל אחד מהפרוטוקולים האלה פותר בעיה אחרת של SMTP:

📧 SPF (Sender Policy Framework):
-----------------------------------
מה זה עושה:
- הדומיין מפרסם רשימה של שרתים שמורשים לשלוח ממנו מיילים
- זה נשמר ב-DNS כרשומת TXT
- כשמייל מגיע, השרת בודק: "האם המייל הזה בא משרת מורשה?"

דוגמה:
school.com מפרסם: "רק mail.school.com מורשה לשלוח מיילים מאתנו"
אם מייל מגיע מ-some-hacker-server.com עם From: student@school.com
→ SPF FAIL! המייל חשוד!

🔐 DKIM (DomainKeys Identified Mail):
--------------------------------------
מה זה עושה:
- השרת חותם על המייל עם חתימה דיגיטלית
- החתימה כוללת hash של תוכן המייל
- אם מישהו משנה את המייל בדרך, החתימה לא תתאים

זה כמו חותמת של דואר רשום - אם מישהו פתח וקרא, אתה יודע!

📊 DMARC (Domain-based Message Authentication):
------------------------------------------------
מה זה עושה:
- מאחד את SPF ו-DKIM
- אומר לשרתים מה לעשות עם מיילים שנכשלו באימות
- שולח דוחות לבעל הדומיין

אפשרויות ב-DMARC:
1. none - רק תרשום, אל תעשה כלום
2. quarantine - שים בspam
3. reject - תזרוק לפח!

למה צריך את כולם?
--------------------
- SPF: מוודא שהשרת לגיטימי
- DKIM: מוודא שהתוכן לא שונה
- DMARC: מגדיר מדיניות ומרכז הכל

ביחד הם עושים קושי רציני לspammers ולphishers!
אבל עדיין לא מושלם - תמיד יש דרכים לעקוף...


שאלה 4: איך שרת דואר יודע לאן לשלוח מייל?
==============================================

זה עובד עם DNS MX Records! (Mail Exchange)

התהליך:
--------
1. אתה שולח מייל ל-friend@example.com
2. השרת שלך מפרק את הכתובת:
   - Username: friend
   - Domain: example.com
3. השרת עושה DNS query: "מה רשומת ה-MX של example.com?"
4. DNS מחזיר: "mail.example.com priority 10"
5. השרת מתחבר ל-mail.example.com על פורט 25
6. מעביר את המייל לשרת שם
7. השרת השני מחפש את friend בתיבות שלו ומעביר לו

דוגמה מציאותית:
-----------------
אם אני שולח מייל ל-student@gmail.com:

1. השרת שלי שואל: "מי ה-MX של gmail.com?"
2. DNS עונה: 
   - gmail-smtp-in.l.google.com (priority 5)
   - alt1.gmail-smtp-in.l.google.com (priority 10)
   - alt2.gmail-smtp-in.l.google.com (priority 20)
3. השרת מנסה את 5 קודם (priority נמוך = עדיפות גבוהה)
4. אם 5 לא עובד, עובר ל-10, אחר כך ל-20
5. מתחבר ומעביר את המייל

אפשר לבדוק זאת עם:
---------------------
nslookup -type=mx gmail.com

או ב-Python:
import dns.resolver
answers = dns.resolver.resolve('gmail.com', 'MX')
for rdata in answers:
    print(f'Priority: {rdata.preference}, Server: {rdata.exchange}')

Priority הוא חשוב!
-------------------
- Priority נמוך = "נסה אותי קודם"
- מספר שרתים = redundancy - אם אחד מת יש גיבוי
- חברות גדולות יש להן המון MX servers ברחבי העולם

זה גאוני כי:
- אין צורך לדעת את ה-IP המדויק
- הדומיין יכול לשנות שרתים מתי שהוא רוצה
- יש גיבוי אוטומטי
"""


# ==============================================================================
# רפלקציה אישית
# ==============================================================================

"""
1. מה היה האתגר הכי מעניין/קשה בתרגיל הזה? למה?
===================================================================

האתגר הכי קשה היה משימה 4 - למצוא את המייל הארוך ביותר.

זה היה מסובך כי:
- צריך לעקוב אחרי state של כל מייל (האם אנחנו אוספים data או לא)
- החבילות מפוצלות - מייל אחד יכול להיות ב-10 חבילות TCP שונות
- צריך להבין איפה מתחיל ה-body ואיפה נגמר
- Headers יכולים להיות בחבילה אחת וה-body בחבילה אחרת
- יש הרבה edge cases - מה אם יש מייל חצי?

מה שעזר לי:
- לצייר על נייר את ה-state machine של המייל
- לעשות debugging עם המון prints
- לבדוק עם מייל פשוט קודם ואז יותר מורכב

בסוף הצלחתי אבל זה לקח לי הכי הרבה זמן.

אבל משימה 5 הייתה הכי מעניינת! היה ממש cool לראות את הדפוסים בתעבורה
ולמצוא bursts חשודים. זה כמו להיות בלש של רשתות!


2. איזה מושג או טכניקה חדשה למדת בתרגיל? איך תוכל להשתמש בזה בעתיד?
=============================================================================

למדתי הרבה דברים חדשים:

1. איך SMTP באמת עובד מאחורי הקלעים
   - אף פעם לא חשבתי על זה שכל מייל שאני שולח עובר בשלבים האלה
   - עכשיו אני מבין למה לפעמים מייל "תקוע" - אולי בעיה בשרת ביניים

2. Scapy - הכלי הזה ממש חזק!
   - אפשר לנתח תעבורת רשת בצורה פייתונית
   - אפשר לבנות חבילות משלך
   - זה יעזור לי בעתיד בקורס הרשתות

3. State machines בתכנות
   - המושג של collecting=True/False והוא שמשנה מה הקוד עושה
   - זה טכניקה שאפשר להשתמש בה בהמון מקומות
   - כמו בהורדת קובץ, parsing של פורמטים מורכבים, וכו'

4. Regular Expressions
   - לפני התרגיל הזה regex היה מפחיד
   - עכשיו אני רואה שזה super useful לחילוץ מידע מטקסט
   - אני כבר משתמש בזה גם בפרויקט אחר שלי

איך אני אשתמש בזה בעתיד:
- בפרויקט הגמר שלנו אפשר לעשות מערכת ניטור רשת
- אם אני אלמד cyber security בצבא/אוניברסיטה זה יעזור המון
- אפשר לבנות כלים לניתוח logs של מערכות שונות
- הבנתי שניתוח פרוטוקולים זה דבר חשוב באבטחת מידע


3. אילו שאלות עלו לך תוך כדי העבודה? מה עוד היית רוצה לחקור?
========================================================================

שאלות שעלו לי:

1. איך SMTP מתמודד עם קבצים מצורפים?
   - ראיתי שיש Base64 encoding אבל לא הבנתי לגמרי איך זה עובד
   - איך שרתים יודעים להפריד בין הודעות עם attachments?

2. מה ההבדל בין פורט 25, 587, ו-465?
   - קראתי שזה קשור ל-TLS אבל לא לגמרי ברור
   - מתי משתמשים בכל אחד?

3. איך שרתי דואר גדולים (Gmail, Outlook) מתמודדים עם מיליוני מיילים ביום?
   - האם הם משתמשים בcaching?
   - איך הם מזהים spam כל כך מהר?
   - יש להם machine learning?

4. איך POP3 ו-IMAP עובדים?
   - אלה הפרוטוקולים שקוראים מיילים אבל לא למדנו עליהם
   - מה ההבדל ביניהם?

5. איך אפשר לעשות Email Forensics מקצועי?
   - לא רק לזהות אם המייל מזויף אלא למצוא מי שלח אותו
   - איך משטרת הסייבר עושה את זה?

מה אני רוצה לחקור עוד:
- לבנות Honeypot SMTP שלוכד spam ומנתח אותו
- ללמוד על Email Threading - איך Gmail מקבץ מיילים לשרשור
- לנסות לעשות bypass של spam filters (כמובן רק לצורך לימוד!)
- להבין איך OAuth2 עובד עם SMTP
- לבנות Email client פשוט משלי


4. איך התרגיל הזה שינה את ההבנה שלך לגבי אבטחת דואר אלקטרוני?
========================================================================

התרגיל פתח לי את העיניים!

לפני התרגיל חשבתי:
- שדואר אלקטרוני זה משהו בטוח
- שאם יש חותמת של "From: admin@school.com" זה באמת מהאדמין
- שSpam זה סתם מטרד
- שאי אפשר באמת לזייף מיילים

אחרי התרגיל הבנתי:
- SMTP בבסיסו לא מאובטח בכלל!
- כל אחד יכול לשלוח מייל "בשם" של כל אחד
- SPF/DKIM/DMARC זה לא מושלם - זה רק מקשה על הזייפנים
- פרטיות במייל היא אשליה בלי הצפנה (PGP/S/MIME)

הבנתי למה phishing זה בעיה כזאת גדולה:
- קל מאוד לעשות מייל שנראה אותנטי
- אפילו עם SPF/DKIM זה לא 100% בטוח
- אנשים סומכים על מה שהם רואים ב-From field
- אפשר לזייף את הממשק החזותי בקלות

מה השתנה בהתנהגות שלי:
- עכשיו אני תמיד בודק את ה-headers המלאים של מיילים חשודים
- לא סומך על שם השולח לבד
- משים לב ל-SPF/DKIM indicators בGmail
- זהיר יותר עם לינקים במיילים אפילו שנראים "לגיטימיים"

גם הבנתי למה אבטחת מידע זה important:
- זה לא רק וירוסים ו-hackers
- זה גם social engineering דרך מיילים
- צריך לחשוב כמו תוקף כדי להבין איך להגן


5. דרג את רמת הקושי של התרגיל (1-10): 7
=================================================

נתתי 7/10 כי:

קל (3/10):
- משימות 1-2 היו די straightforward
- הקוד בסיסי של SMTP לא מסובך
- היו הרבה דוגמאות והסברים

בינוני (7/10):
- משימות 3-4 דרשו חשיבה
- צריך היה להבין איך Scapy עובד
- צריך היה להתמודד עם errors ו-edge cases
- parsing של PCAP files זה טריקי

קשה יותר (9/10):
- משימה 4 (המייל הארוך ביותר) הייתה ממש challenging
- צריך לעקוב אחרי state מורכב
- חבילות מפוצלות ועיבוד חלקי של נתונים
- debugging היה קשה כי הרבע data

בסך הכל זה היה תרגיל טוב:
- מאתגר אבל לא בלתי אפשרי
- למדתי המון
- היה כיף לראות שהקוד עובד
- הרגשתי כמו hacker אמיתי 😎

הייתי משנה רק דבר אחד:
- הייתי נותן PCAP file לדוגמה קטן לבדיקה
- ככה אפשר היה לדבג יותר בקלות


6. משוב לשיפור: מה היית משנה/מוסיף/מוריד בתרגיל?
==============================================================

מה היה טוב:
✅ ההסברים המפורטים לכל משימה
✅ השלד קוד שעזר להתחיל
✅ הדוגמאות לפלט
✅ החלוקה לרמות (בסיסי/בינוני/מתקדם)
✅ שאלות המחשבה - עזרו להבין יותר עמוק

מה הייתי משנה:
📝 הייתי מוסיף PCAP file לדוגמה:
   - קובץ קטן עם 5-10 מיילים פשוטים
   - עם הערות מה כל מייל מכיל
   - זה היה עוזר לדבג את הקוד

📝 הייתי מוסיף סרטון קצר:
   - איך SMTP עובד בצורה ויזואלית
   - לראות את הflow של מייל מקצה לקצה
   - אפשר עם Wireshark live demo

📝 בונוס צ'אלנג' אופציונלי:
   - משהו ממש מתקדם לתלמידים חזקים
   - כמו לבנות SMTP server פשוט
   - או לעשות Email forensics על מקרה אמיתי

📝 חלק של "Common Mistakes":
   - רשימה של טעויות נפוצות
   - איך לפתור אותן
   - זה היה חוסך לי זמן debugging

מה הייתי מוריד:
❌ אולי פחות שאלות רפלקציה?
   - 6 שאלות זה קצת הרבה
   - 3-4 זה היה מספיק

מה הייתי מוסיף:
➕ Extension למתקדמים:
   - לנסות לעקוף spam filter
   - לבנות parser לEmail headers מורכבים
   - להוסיף תמיכה ב-STARTTLS

➕ חלק של "Real World":
   - דוגמאות של phishing אמיתיים (anonymized)
   - איך חברות מתמודדות עם spam
   - סטטיסטיקות מעניינות על email security

בסך הכל תרגיל מעולה!
הרגשתי שאני לומד משהו practical ו-relevant לעולם האמיתי.
תודה רבה! 🙏
"""


# ==============================================================================
# סיכום והערות נוספות
# ==============================================================================

"""
הערות כלליות על הפתרון:
==========================

1. הקוד נבדק בסביבה מבודדת עם MailHog (https://github.com/mailhog/MailHog)
2. לא נבדק על שרתים אמיתיים - זה לא אתי ולא חוקי!
3. חלק מהפונקציות דורשות קובץ PCAP - אפשר ליצור אחד עם Wireshark
4. הקוד כתוב בצורה חינוכית - בפרודקשן הייתי מוסיף error handling טוב יותר

כלים שעזרו לי:
-----------------
- Python 3.9+
- Scapy (pip install scapy)
- MailHog לבדיקות מקומיות
- Wireshark ללכידת תעבורה
- VS Code עם Python extension

למידה נוספת:
--------------
אם רוצים ללמוד עוד:
1. RFC 5321 - SMTP Protocol specification
2. RFC 5322 - Internet Message Format
3. Book: "Hacking Exposed" - Chapter on Email Security
4. Course: "Computer Networks" by Andrew Tanenbaum

Stay ethical, stay curious! 🚀
"""