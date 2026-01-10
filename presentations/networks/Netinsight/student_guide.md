# 📘 מדריך לתלמיד - האקתון NetInsight
## מה לעשות בכל שלב? איך לעבוד? מה להגיש?

---

# 🎯 מטרת המסמך

מסמך זה ילווה אתכם לאורך כל שלבי ההאקתון, ויסביר בדיוק:
- ✅ מה צריך לעשות בכל שלב
- ✅ איך לחלק משימות בקבוצה
- ✅ אילו החלטות צריך לקבל
- ✅ איך ליצור כל סוג תעבורה
- ✅ איך לנתח את המידע
- ✅ מה להגיש ואיך להציג

---

# 🏗️ הכנה - לפני שמתחילים

## הקמת הקבוצה (3-4 תלמידים)

### תפקידים מומלצים:

1. **👨‍💻 Developer 1** - מומחה קוד Python, יצירת datasets
2. **🤖 Developer 2** - פיתוח אלגוריתם הסיווג
3. **🎨 Designer** - ממשק משתמש וויזואליזציה
4. **📊 Analyst** - מחקר, ניתוח נתונים, מצגת

**הערה חשובה:** כולם עובדים ביחד! התפקידים הם לארגון, לא לבידוד.

### הכנות ראשוניות:

```bash
# 1. יצירת תיקיית עבודה
mkdir netinsight_team_[שם_קבוצה]
cd netinsight_team_[שם_קבוצה]

# 2. יצירת מבנה תיקיות
mkdir research datasets models ui docs

# 3. התקנת כלים
pip install scapy pandas numpy scikit-learn matplotlib gradio
```

---

# 📚 שלב 1: מחקר והבנה (45 דקות)

## 🎯 המטרה
להבין לעומק איך 3 סוגי תעבורה שונים מתנהגים ברשת.

## 📋 משימות הקבוצה

### דקות 0-15: חלוקת נושאים
כל חבר קבוצה בוחר סוג תעבורה למחקר:
- **תלמיד A:** Video Streaming (Netflix, YouTube)
- **תלמיד B:** Gaming (Fortnite, Valorant)
- **תלמיד C:** Video Calls (Zoom, Teams)

### דקות 15-35: מחקר אישי
כל אחד חוקר את הנושא שלו ועונה על:

#### שאלות למחקר:

**1. מה גודל ה-Packets?**
```
🔍 איפה לחפש:
- Wireshark documentation
- Google: "[נושא] packet size typical"
- "Network traffic analysis [נושא]"

📝 מה לרשום:
- גודל ממוצע (bytes)
- טווח (min-max)
- האם קבוע או משתנה?
```

**2. מה התדירות של Packets?**
```
🔍 שאלות:
- כמה packets לשנייה?
- האם קבוע או משתנה?
- יש bursts (פרצי תעבורה)?

📝 דוגמה:
Gaming: 30-128 packets/sec (תלוי ב-tick rate)
```

**3. כיווניות התעבורה**
```
🔍 בדקו:
- האם symmetric (דו-כיווני שווה)?
- או asymmetric (בעיקר download/upload)?

📝 דוגמה:
Streaming: Asymmetric - 90% download, 10% upload
```

**4. פרוטוקולים**
```
🔍 מצאו:
- TCP או UDP?
- פורטים נפוצים
- פרוטוקולים מיוחדים (RTP, RTMP, QUIC)

📝 דוגמה:
Gaming: בעיקר UDP, פורטים דינמיים
```

### דקות 35-45: סיכום משותף

**🤝 התכנסות קבוצתית:**
- כל אחד מציג את הממצאים שלו (5 דקות)
- יצירת טבלת השוואה משותפת
- זיהוי ההבדלים המרכזיים

---

## 📤 תוצר להגשה - שלב 1

### מסמך Word/PDF בשם: `research_report_[שם_קבוצה].pdf`

#### מבנה המסמך:

```markdown
# מחקר - ניתוח תעבורת רשת
צוות: [שמות]
תאריך: [תאריך]

---

## 1. Video Streaming

### מאפיינים עיקריים:
- גודל packet ממוצע: 1000-1460 bytes
- תדירות: 25-60 packets/second
- כיווניות: Asymmetric (85% download)

### פרוטוקולים:
- TCP/QUIC
- פורטים: 80, 443
- HTTP/2, HTTP/3

### דפוסי התנהגות:
- Bursts של video segments
- Initial buffering phase
- Adaptive bitrate

### מקורות:
[רשימת אתרים/מאמרים שבהם השתמשתם]

---

## 2. Gaming

[אותו מבנה]

---

## 3. Video Calls

[אותו מבנה]

---

## טבלת השוואה

| תכונה | Streaming | Gaming | Video Calls |
|-------|-----------|--------|-------------|
| גודל Packet | גדול (1400B) | קטן (100B) | בינוני (500B) |
| תדירות | בינונית | גבוהה | בינונית |
| כיווניות | ↓ Asymmetric | ⇆ Symmetric | ⇆ Symmetric |
| פרוטוקול | TCP/QUIC | UDP | UDP/RTP |

---

## מסקנות
המאפיינים המבדילים ביותר:
1. גודל Packet - הבדל משמעותי
2. כיווניות - Streaming שונה מהשאר
3. פרוטוקול - רמז ראשוני
```

---

## 💡 טיפים למחקר טוב

✅ **השתמשו במקורות מהימנים:**
- Wireshark Wiki
- RFC documents
- מאמרים אקדמיים (Google Scholar)
- תיעוד רשמי של פרוטוקולים

✅ **תעדו מקורות:**
רשמו כל מקור שממנו לקחתם מידע

✅ **הבינו, אל תעתיקו:**
כתבו במילים שלכם!

---

# 💾 שלב 2: יצירת Dataset (60 דקות)

## 🎯 המטרה
ליצור קבצי PCAP עם תעבורה סימולטיבית של כל סוג.

## 📋 משימות הקבוצה

### דקות 0-10: תכנון והחלטות

**החלטה 1: אילו סוגי תעבורה?**
```
✅ חובה: 3 סוגים שחקרתם (Streaming, Gaming, Video Calls)
🌟 בונוס: +2 נוספים (Web Browsing, File Transfer)
```

**החלטה 2: כמה traffic ליצור?**
```
מומלץ: 60 שניות לכל סוג
→ מספיק לניתוח, לא יותר מדי לעיבוד
```

**החלטה 3: מי עושה מה?**
```
🧑‍💻 Developer 1: Streaming + Gaming
🧑‍💻 Developer 2: Video Calls + Web Browsing
🎨 Designer: עוזר, מכין תיעוד
📊 Analyst: בודק איכות, מחלץ metadata
```

### דקות 10-50: כתיבת קוד ויצירת Traffic

---

## 🎮 איך יוצרים כל סוג תעבורה?

### A. Video Streaming Traffic

**מה צריך לסמלט?**
- Packets גדולים (1200-1460 bytes)
- תדירות: ~30 packets/sec
- בעיקר download (90%)
- Bursts של video segments

**קוד לדוגמה:**

```python
from scapy.all import *
import time

def create_streaming_traffic(duration=60):
    """
    יצירת תעבורת Streaming
    """
    packets = []
    
    # הגדרות
    src_ip = "192.168.1.100"  # הלקוח
    dst_ip = "8.8.8.8"        # השרת (YouTube/Netflix)
    src_port = 50000
    dst_port = 443  # HTTPS
    
    print("[*] Creating Streaming Traffic...")
    
    start_time = time.time()
    packet_count = 0
    
    # Phase 1: Initial burst (buffering)
    for i in range(50):
        # Large packets (video data)
        payload_size = random.randint(1200, 1460)
        payload = Raw(load='V' * payload_size)
        
        pkt = IP(src=dst_ip, dst=src_ip) / \
              TCP(sport=dst_port, dport=src_port, flags='PA') / \
              payload
        
        packets.append(pkt)
        packet_count += 1
    
    # Phase 2: Steady streaming
    frame_rate = 30  # frames per second
    
    while (time.time() - start_time) < duration:
        # Video frame as multiple packets
        for _ in range(20):  # ~20 packets per frame
            payload_size = random.randint(1400, 1460)
            payload = Raw(load='V' * payload_size)
            
            pkt = IP(src=dst_ip, dst=src_ip) / \
                  TCP(sport=dst_port, dport=src_port, flags='PA') / \
                  payload
            
            packets.append(pkt)
        
        # Small ACK from client
        ack = IP(src=src_ip, dst=dst_ip) / \
              TCP(sport=src_port, dport=dst_port, flags='A')
        packets.append(ack)
        
        # Wait for next frame
        time.sleep(1.0 / frame_rate)
    
    # Save to PCAP
    wrpcap('streaming.pcap', packets)
    print(f"[✓] Created {len(packets)} packets → streaming.pcap")
    
    return packets

# הרצה
create_streaming_traffic(duration=60)
```

**🎯 נקודות חשובות:**
- השתמשו ב-`time.sleep()` ליצירת timing אמיתי
- גודלי packets צריכים להיות קרובים לאמיתיים
- שימו לב ליחס download/upload

---

### B. Gaming Traffic

**מה צריך לסמלט?**
- Packets קטנים (50-200 bytes)
- תדירות גבוהה וקבועה (60-128 Hz)
- Symmetric (דו-כיווני)
- UDP (לא TCP!)

**קוד לדוגמה:**

```python
def create_gaming_traffic(duration=60, tick_rate=64):
    """
    יצירת תעבורת Gaming
    tick_rate = updates per second (30, 64, 128)
    """
    packets = []
    
    src_ip = "192.168.1.100"
    dst_ip = "8.8.8.8"
    src_port = 50001
    dst_port = 27015  # Typical game port
    
    print(f"[*] Creating Gaming Traffic (tick_rate={tick_rate})...")
    
    start_time = time.time()
    tick_interval = 1.0 / tick_rate
    
    while (time.time() - start_time) < duration:
        # Client → Server (player actions)
        client_size = random.randint(50, 150)
        client_payload = Raw(load='C' * client_size)
        
        client_pkt = IP(src=src_ip, dst=dst_ip) / \
                    UDP(sport=src_port, dport=dst_port) / \
                    client_payload
        
        packets.append(client_pkt)
        
        # Server → Client (world state)
        server_size = random.randint(80, 200)
        server_payload = Raw(load='S' * server_size)
        
        server_pkt = IP(src=dst_ip, dst=src_ip) / \
                    UDP(sport=dst_port, dport=src_port) / \
                    server_payload
        
        packets.append(server_pkt)
        
        # Wait for next tick
        time.sleep(tick_interval)
    
    wrpcap('gaming.pcap', packets)
    print(f"[✓] Created {len(packets)} packets → gaming.pcap")
    
    return packets

# הרצה
create_gaming_traffic(duration=60, tick_rate=64)
```

**🎯 נקודות חשובות:**
- Tick rate קבוע מאוד (הכי חשוב!)
- גדלים קטנים
- UDP, לא TCP
- תעבורה סימטרית

---

### C. Video Call Traffic

**מה צריך לסמלט?**
- Packets בינוניים (300-800 bytes)
- תדירות: 30-50 packets/sec
- Symmetric
- UDP, נפרד לאודיו ווידאו

**קוד לדוגמה:**

```python
def create_video_call_traffic(duration=60):
    """
    יצירת תעבורת Video Call
    נפרד לזרמי אודיו ווידאו
    """
    packets = []
    
    src_ip = "192.168.1.100"
    dst_ip = "8.8.8.8"
    src_port = 50002
    dst_port = 3478  # WebRTC/STUN port
    
    print("[*] Creating Video Call Traffic...")
    
    start_time = time.time()
    frame_counter = 0
    
    audio_rate = 50  # packets/sec
    video_rate = 30  # fps
    
    while (time.time() - start_time) < duration:
        # Audio stream (every other iteration)
        if frame_counter % 2 == 0:
            # Upload audio
            audio_size = random.randint(60, 120)
            audio_up = IP(src=src_ip, dst=dst_ip) / \
                      UDP(sport=src_port, dport=dst_port) / \
                      Raw(load='A' * audio_size)
            packets.append(audio_up)
            
            # Download audio
            audio_down = IP(src=dst_ip, dst=src_ip) / \
                        UDP(sport=dst_port, dport=src_port) / \
                        Raw(load='A' * audio_size)
            packets.append(audio_down)
        
        # Video stream
        # Adaptive quality - varies based on "network"
        quality = random.uniform(0.7, 1.0)
        video_size = int(random.randint(400, 1200) * quality)
        
        # Upload video
        video_up = IP(src=src_ip, dst=dst_ip) / \
                  UDP(sport=src_port, dport=dst_port) / \
                  Raw(load='V' * video_size)
        packets.append(video_up)
        
        # Download video
        video_down = IP(src=dst_ip, dst=src_ip) / \
                    UDP(sport=dst_port, dport=src_port) / \
                    Raw(load='V' * video_size)
        packets.append(video_down)
        
        frame_counter += 1
        time.sleep(1.0 / video_rate)
    
    wrpcap('video_call.pcap', packets)
    print(f"[✓] Created {len(packets)} packets → video_call.pcap")
    
    return packets

# הרצה
create_video_call_traffic(duration=60)
```

**🎯 נקודות חשובות:**
- שני זרמים: אודיו + וידאו
- Adaptive quality (גדלים משתנים)
- Bidirectional
- UDP

---

### דקות 50-60: בדיקה ותיעוד

**✅ בדיקות לעשות:**

1. **בדיקה ב-Wireshark:**
```bash
# פתח כל PCAP ב-Wireshark
wireshark streaming.pcap

# בדקו:
- מספר packets (סביר?)
- גדלי packets (תואם מה שרצינו?)
- timing (נראה טבעי?)
```

2. **חילוץ metadata:**
```python
# קוד לחילוץ סטטיסטיקות בסיסיות
from scapy.all import *
import pandas as pd

def extract_metadata(pcap_file, traffic_type):
    packets = rdpcap(pcap_file)
    
    data = {
        'file': pcap_file,
        'traffic_type': traffic_type,
        'total_packets': len(packets),
        'avg_size': sum(len(p) for p in packets) / len(packets),
        'min_size': min(len(p) for p in packets),
        'max_size': max(len(p) for p in packets),
        'duration': float(packets[-1].time - packets[0].time)
    }
    
    return data

# חלץ מכל קובץ
streaming_meta = extract_metadata('streaming.pcap', 'Streaming')
gaming_meta = extract_metadata('gaming.pcap', 'Gaming')
video_call_meta = extract_metadata('video_call.pcap', 'Video_Call')

# שמור ל-CSV
df = pd.DataFrame([streaming_meta, gaming_meta, video_call_meta])
df.to_csv('metadata.csv', index=False)
print("[✓] Metadata saved to metadata.csv")
```

---

## 📤 תוצר להגשה - שלב 2

### קבצים להגשה:

```
📁 datasets_[שם_קבוצה]/
├── streaming.pcap          # 2000-3000 packets
├── gaming.pcap             # 7000-8000 packets
├── video_call.pcap         # 3000-4000 packets
├── metadata.csv            # סטטיסטיקות
└── README.txt              # הסבר קצר
```

### תוכן README.txt:

```
NetInsight Dataset
==================

צוות: [שמות]
תאריך: [תאריך]

קבצים:
-------
1. streaming.pcap
   - סוג: Video Streaming (Netflix/YouTube)
   - זמן: 60 שניות
   - Packets: 2,500
   - מאפיינים: גדלים גדולים, bursts, asymmetric

2. gaming.pcap
   - סוג: Gaming (Fortnite style)
   - זמן: 60 שניות
   - Packets: 7,680 (64 tick rate)
   - מאפיינים: קטנים, קבועים, symmetric, UDP

3. video_call.pcap
   - סוג: Video Call (Zoom style)
   - זמן: 60 שניות
   - Packets: 3,600
   - מאפיינים: בינוניים, adaptive, symmetric

כלים שימושיים:
----------------
pip install scapy
```

---

## 💡 טיפים ליצירת Dataset טוב

✅ **Timing הוא הכל:**
השתמשו ב-`time.sleep()` ליצירת דפוסים אמיתיים

✅ **גדלים משתנים:**
אל תיצרו packets באותו גודל בדיוק - השתמשו ב-`random.randint()`

✅ **Metadata חשוב:**
תעדו מה יצרתם - יעזור לכם בשלב הבא

✅ **בדקו ב-Wireshark:**
פתחו כל PCAP ותראו שהוא נראה הגיוני

❌ **טעויות נפוצות:**
- לשכוח `time.sleep()` → כל ה-packets יווצרו ברגע
- לא להשתמש ב-random → patterns מדי "מושלמים"
- לשכוח להוסיף UDP ל-Gaming → יהיה TCP by default

---

# 🤖 שלב 3: פיתוח אלגוריתם סיווג (90 דקות)

## 🎯 המטרה
לבנות מערכת שמסוגלת לקבל PCAP ולהחזיר "זה Gaming/Streaming/Video Call"

## 📋 משימות הקבוצה

### דקות 0-15: תכנון האלגוריתם

**🤝 דיון קבוצתי - החלטות חשובות:**

**שאלה 1: איזו גישה לבחור?**
```
אופציה A: Rule-Based בלבד
✅ פשוט יותר
❌ פחות מדויק

אופציה B: ML בלבד
✅ מדויק יותר
❌ מסובך, צריך אימון

אופציה C: Hybrid (מומלץ!)
✅ מהיר + מדויק
✅ מקבל בונוס נקודות!
```

**שאלה 2: אילו features לחלץ?**
```
רשימת features מומלצת (בחרו 10-15):

📏 Packet Size:
☑ mean_packet_size
☑ std_packet_size
☑ min/max_packet_size

⏱️ Timing:
☑ mean_iat (inter-arrival time)
☑ std_iat
☑ packet_rate

🔄 Bidirectional:
☑ upload_ratio
☑ download_ratio
☑ symmetry

🌊 Patterns:
☑ burst_count
☑ protocol (TCP/UDP)
☑ ports
```

**שאלה 3: חלוקת עבודה**
```
👨‍💻 Dev 1: Feature Extraction
👨‍💻 Dev 2: Classifier (Rules + ML)
🎨 Designer: ויזואליזציה של תוצאות
📊 Analyst: testing ו-evaluation
```

---

### דקות 15-60: כתיבת הקוד

## 🔧 חלק א': Feature Extraction

**מטרה:** לקבל PCAP ולהחזיר DataFrame עם features

**קוד מלא:**

```python
from scapy.all import *
import pandas as pd
import numpy as np
from collections import defaultdict

class FeatureExtractor:
    """
    מחלץ features מ-PCAP
    """
    
    def extract_from_pcap(self, pcap_file):
        """
        הפונקציה הראשית
        """
        print(f"[*] Reading {pcap_file}...")
        packets = rdpcap(pcap_file)
        
        print(f"[*] Grouping {len(packets)} packets to flows...")
        flows = self._group_packets_to_flows(packets)
        
        print(f"[*] Extracting features from {len(flows)} flows...")
        features_list = []
        
        for flow_id, flow_packets in flows.items():
            features = self._extract_flow_features(flow_id, flow_packets)
            features_list.append(features)
        
        df = pd.DataFrame(features_list)
        print(f"[✓] Extracted {len(df)} flows with {len(df.columns)} features")
        
        return df
    
    def _group_packets_to_flows(self, packets):
        """
        קיבוץ packets ל-flows
        """
        flows = defaultdict(list)
        
        for pkt in packets:
            if IP not in pkt:
                continue
            
            # Extract 5-tuple
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            
            if TCP in pkt:
                src_port = pkt[TCP].sport
                dst_port = pkt[TCP].dport
                protocol = "TCP"
            elif UDP in pkt:
                src_port = pkt[UDP].sport
                dst_port = pkt[UDP].dport
                protocol = "UDP"
            else:
                continue
            
            # Create flow ID (bidirectional)
            flow_id = f"{src_ip}:{src_port}<->{dst_ip}:{dst_port}:{protocol}"
            flows[flow_id].append(pkt)
        
        return flows
    
    def _extract_flow_features(self, flow_id, packets):
        """
        חילוץ features מ-flow בודד
        """
        features = {}
        
        # Protocol
        protocol = flow_id.split(':')[-1]
        features['protocol'] = protocol
        
        # Packet count
        features['packet_count'] = len(packets)
        
        # Packet sizes
        sizes = [len(pkt) for pkt in packets]
        features['mean_packet_size'] = np.mean(sizes)
        features['std_packet_size'] = np.std(sizes)
        features['min_packet_size'] = min(sizes)
        features['max_packet_size'] = max(sizes)
        
        # Time-based features
        if len(packets) > 1:
            timestamps = [float(pkt.time) for pkt in packets]
            
            # Flow duration
            features['flow_duration'] = timestamps[-1] - timestamps[0]
            
            # Inter-arrival times
            iats = [timestamps[i+1] - timestamps[i] 
                   for i in range(len(timestamps)-1)]
            
            features['mean_iat'] = np.mean(iats)
            features['std_iat'] = np.std(iats)
            
            # Packet rate
            features['packet_rate'] = len(packets) / features['flow_duration']
            
            # IAT coefficient of variation (קביעות)
            if features['mean_iat'] > 0:
                features['iat_cv'] = features['std_iat'] / features['mean_iat']
            else:
                features['iat_cv'] = 0
        else:
            features['flow_duration'] = 0
            features['mean_iat'] = 0
            features['std_iat'] = 0
            features['packet_rate'] = 0
            features['iat_cv'] = 0
        
        # Bidirectional analysis
        src_ip = packets[0][IP].src
        upload_bytes = sum(len(p) for p in packets if p[IP].src == src_ip)
        download_bytes = sum(len(p) for p in packets if p[IP].dst == src_ip)
        total_bytes = upload_bytes + download_bytes
        
        features['upload_ratio'] = upload_bytes / total_bytes if total_bytes > 0 else 0
        features['download_ratio'] = download_bytes / total_bytes if total_bytes > 0 else 0
        
        # Symmetry (0 = asymmetric, 1 = symmetric)
        features['symmetry'] = 1 - abs(features['upload_ratio'] - features['download_ratio'])
        
        return features

# שימוש
extractor = FeatureExtractor()
features_df = extractor.extract_from_pcap('streaming.pcap')
print(features_df.head())
```

**🎯 הסבר Features חשובים:**

**mean_packet_size** - גודל ממוצע
```
Gaming: ~100 bytes
Video Call: ~500 bytes
Streaming: ~1400 bytes
```

**iat_cv** - Coefficient of Variation של IAT
```
Gaming: ~0.2 (קבוע מאוד!)
Video Call: ~0.5 (בינוני)
Streaming: ~1.0+ (משתנה)
```

**symmetry** - סימטריה
```
Gaming: ~0.8-1.0 (סימטרי)
Video Call: ~0.7-0.9 (כמעט סימטרי)
Streaming: ~0.1-0.3 (לא סימטרי בכלל)
```

---

## 🎲 חלק ב': Classifier - Rule-Based

**מטרה:** כללים פשוטים לזיהוי מהיר

```python
class RuleBasedClassifier:
    """
    סיווג מבוסס כללים
    """
    
    def classify(self, features):
        """
        מחזיר: (class_name, confidence) או (None, 0)
        """
        
        # Rule 1: Gaming Detection
        # קטן + מהיר + סימטרי + UDP
        if (50 < features['mean_packet_size'] < 200 and
            30 < features['packet_rate'] < 150 and
            features['symmetry'] > 0.6 and
            features['iat_cv'] < 0.5 and
            features['protocol'] == 'UDP'):
            
            return 'Gaming', 1.0
        
        # Rule 2: Streaming Detection
        # גדול + לא סימטרי + bursts
        if (features['mean_packet_size'] > 800 and
            features['download_ratio'] > 0.7):
            
            return 'Streaming', 1.0
        
        # Rule 3: Video Call Detection
        # בינוני + סימטרי + UDP
        if (300 < features['mean_packet_size'] < 800 and
            features['symmetry'] > 0.6 and
            features['protocol'] == 'UDP'):
            
            return 'Video_Call', 1.0
        
        # No rule matched
        return None, 0

# בדיקה
classifier = RuleBasedClassifier()

# דוגמה: Gaming features
gaming_features = {
    'mean_packet_size': 95,
    'packet_rate': 64,
    'symmetry': 0.85,
    'iat_cv': 0.18,
    'protocol': 'UDP',
    'download_ratio': 0.48
}

result, conf = classifier.classify(gaming_features)
print(f"Classification: {result}, Confidence: {conf}")
# Output: Classification: Gaming, Confidence: 1.0
```

**🎯 איך לבנות Rules טובים?**

1. **הסתכלו על המחקר שלכם (שלב 1)**
   - מה הבדלים ברורים?
   - מה המאפיינים הייחודיים?

2. **השתמשו בלוגיקה AND**
   ```python
   if condition1 AND condition2 AND condition3:
       return class
   ```

3. **תנו טווחים, לא ערכים מדויקים**
   ```python
   ✅ if 50 < size < 200:
   ❌ if size == 95:
   ```

---

## 🤖 חלק ג': Classifier - Machine Learning

**מטרה:** ML למקרים מורכבים

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

class MLClassifier:
    """
    סיווג עם Decision Tree
    """
    
    def __init__(self):
        self.model = DecisionTreeClassifier(
            max_depth=10,
            min_samples_split=5,
            random_state=42
        )
        self.feature_names = None
    
    def train(self, X_train, y_train):
        """
        אימון המודל
        """
        print("[*] Training ML model...")
        
        # Select numeric features only
        numeric_cols = X_train.select_dtypes(include=[np.number]).columns
        X_train_numeric = X_train[numeric_cols]
        self.feature_names = list(numeric_cols)
        
        # Train
        self.model.fit(X_train_numeric, y_train)
        
        print("[✓] Model trained successfully")
        print(f"    Features used: {len(self.feature_names)}")
    
    def predict(self, features):
        """
        סיווג
        """
        # Convert to DataFrame if dict
        if isinstance(features, dict):
            features_df = pd.DataFrame([features])
        else:
            features_df = features
        
        # Select features
        X = features_df[self.feature_names]
        
        # Predict
        prediction = self.model.predict(X)[0]
        
        # Get confidence
        if hasattr(self.model, 'predict_proba'):
            probs = self.model.predict_proba(X)[0]
            confidence = max(probs)
        else:
            confidence = 0.8
        
        return prediction, confidence
    
    def save(self, filepath='ml_model.pkl'):
        """
        שמירה
        """
        joblib.dump({
            'model': self.model,
            'features': self.feature_names
        }, filepath)
        print(f"[✓] Model saved to {filepath}")

# דוגמה: אימון
# קודם כל, צור dataset מכל ה-PCAPs שלך

all_features = []

for pcap_file, label in [('streaming.pcap', 'Streaming'),
                          ('gaming.pcap', 'Gaming'),
                          ('video_call.pcap', 'Video_Call')]:
    df = extractor.extract_from_pcap(pcap_file)
    df['label'] = label
    all_features.append(df)

# Combine
combined = pd.concat(all_features, ignore_index=True)

# Split
X = combined.drop('label', axis=1)
y = combined['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train
ml_clf = MLClassifier()
ml_clf.train(X_train, y_train)

# Test
y_pred = []
for idx in range(len(X_test)):
    pred, conf = ml_clf.predict(X_test.iloc[idx])
    y_pred.append(pred)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.2%}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
```

---

## 🔄 חלק ד': Hybrid Classifier (בונוס!)

**שילוב של שניהם:**

```python
class HybridClassifier:
    """
    מסווג היברידי - Rules קודם, אחר כך ML
    """
    
    def __init__(self):
        self.rules = RuleBasedClassifier()
        self.ml = MLClassifier()
    
    def classify(self, features):
        """
        סיווג היברידי
        """
        # Try rules first
        rule_result, rule_conf = self.rules.classify(features)
        
        if rule_result is not None:
            # Rule matched!
            return rule_result, rule_conf, 'rule-based'
        
        # No rule matched, use ML
        ml_result, ml_conf = self.ml.predict(features)
        return ml_result, ml_conf, 'ml-based'

# שימוש
hybrid = HybridClassifier()
# (צריך לאמן את ML קודם)

result, conf, method = hybrid.classify(gaming_features)
print(f"{result} ({conf:.1%}) - method: {method}")
```

---

### דקות 60-90: בדיקה והערכה

**🧪 בדיקות לבצע:**

```python
# 1. Test על כל PCAP
for pcap_file in ['streaming.pcap', 'gaming.pcap', 'video_call.pcap']:
    features_df = extractor.extract_from_pcap(pcap_file)
    
    print(f"\n=== Testing {pcap_file} ===")
    
    # Test first flow
    test_features = features_df.iloc[0].to_dict()
    result, conf, method = hybrid.classify(test_features)
    
    print(f"Result: {result}")
    print(f"Confidence: {conf:.1%}")
    print(f"Method: {method}")

# 2. Confusion Matrix
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Streaming', 'Gaming', 'Video_Call'],
            yticklabels=['Streaming', 'Gaming', 'Video_Call'])
plt.title('Confusion Matrix')
plt.ylabel('True')
plt.xlabel('Predicted')
plt.savefig('confusion_matrix.png')
print("[✓] Confusion matrix saved")
```

---

## 📤 תוצר להגשה - שלב 3

### קבצים להגשה:

```
📁 models_[שם_קבוצה]/
├── feature_extractor.py    # הקוד שלכם
├── classifier.py            # הקוד שלכם
├── ml_model.pkl            # המודל המאומן
├── confusion_matrix.png    # גרף
├── model_report.txt        # דוח ביצועים
└── README.txt              # הסבר
```

### תוכן model_report.txt:

```
NetInsight Classification System
=================================

צוות: [שמות]
תאריך: [תאריך]

## גישה אלגוריתמית

בחרנו בגישה היברידית:
1. Layer 1: Rule-Based Classification
   - 3 כללים פשוטים
   - זיהוי מהיר למקרים ברורים
   
2. Layer 2: ML Classification
   - Decision Tree
   - 15 features
   - אימון על 500 flows

## ביצועים

Overall Accuracy: 87%

Per Class:
- Streaming: 92%
- Gaming: 89%
- Video Call: 85%

Method Distribution:
- Rule-Based: 45%
- ML-Based: 55%

## Features חשובים

Top 5 features (by importance):
1. mean_packet_size: 35.4%
2. download_ratio: 21.9%
3. packet_rate: 16.5%
4. symmetry: 12.0%
5. iat_cv: 8.9%

## מסקנות

המערכת מצליחה לסווג טוב!
הדיוק הגבוה ביותר הוא ב-Streaming
כי יש לו מאפיינים ייחודיים מאוד.
```

---

## 💡 טיפים לאלגוריתם טוב

✅ **Feature Engineering הוא הכל:**
Features טובים חשובים יותר מאלגוריתם מסובך

✅ **התחילו פשוט:**
Rules פשוטים → ML פשוט → שיפורים

✅ **בדקו הרבה:**
Test על כל PCAP, על flows שונים

✅ **תעדו הכל:**
רשמו מה עבד ומה לא

❌ **טעויות נפוצות:**
- יותר מדי features → overfitting
- לא לבדוק על test set
- לשכוח feature normalization (אם צריך)

---

# 🎨 שלב 4: ממשק משתמש (75 דקות)

## 🎯 המטרה
לבנות ממשק שמאפשר להעלות PCAP ולראות את הניתוח

## 📋 משימות הקבוצה

### דקות 0-10: תכנון הממשק

**🤝 דיון קבוצתי:**

**החלטה 1: Gradio או Flask?**
```
Gradio:
✅ מהיר מאוד לבניה (30 דקות)
✅ יפה מאוד out-of-the-box
✅ מומלץ למתחילים
❌ פחות גמישות בעיצוב

Flask:
✅ גמישות מלאה
✅ נראה "מקצועי"
❌ לוקח יותר זמן
❌ צריך לכתוב HTML/CSS

המלצה: Gradio! (אלא אם יש לכם ניסיון ב-web)
```

**החלטה 2: מה להציג?**
```
חובה:
☑ העלאת PCAP file
☑ סיכום טקסטואלי
☑ Pie chart של התפלגות
☑ טבלה של flows

בונוס:
☑ Timeline chart
☑ Real-time progress
☑ Download results as CSV
```

---

### דקות 10-60: בניית הממשק

## 🎨 אופציה A: Gradio (מומלץ!)

**קוד מלא:**

```python
import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Import your classes
from feature_extractor import FeatureExtractor
from classifier import HybridClassifier

# Initialize
extractor = FeatureExtractor()
classifier = HybridClassifier()
# Load trained model
classifier.ml.model = joblib.load('ml_model.pkl')

def analyze_pcap(pcap_file):
    """
    הפונקציה שמנתחת PCAP
    """
    try:
        # Extract features
        features_df = extractor.extract_from_pcap(pcap_file.name)
        
        # Classify each flow
        results = []
        for idx in range(len(features_df)):
            features = features_df.iloc[idx].to_dict()
            traffic_type, confidence, method = classifier.classify(features)
            
            results.append({
                'Flow': idx + 1,
                'Type': traffic_type,
                'Confidence': f"{confidence:.1%}",
                'Method': method,
                'Packets': features.get('packet_count', 0),
                'Bytes': features.get('packet_count', 0) * features.get('mean_packet_size', 0)
            })
        
        results_df = pd.DataFrame(results)
        
        # Create summary
        summary = create_summary(results_df)
        
        # Create pie chart
        pie_chart = create_pie_chart(results_df)
        
        # Return all outputs
        return summary, pie_chart, results_df
        
    except Exception as e:
        return f"Error: {str(e)}", None, None

def create_summary(results_df):
    """
    סיכום טקסטואלי
    """
    total = len(results_df)
    traffic_counts = results_df['Type'].value_counts()
    
    summary = f"# 📊 Analysis Results\n\n"
    summary += f"**Total Flows:** {total}\n\n"
    summary += "## Traffic Distribution:\n"
    
    for traffic_type, count in traffic_counts.items():
        pct = (count / total) * 100
        emoji = {'Streaming': '📹', 'Gaming': '🎮', 'Video_Call': '📞'}.get(traffic_type, '📊')
        summary += f"- {emoji} **{traffic_type}**: {count} flows ({pct:.1f}%)\n"
    
    return summary

def create_pie_chart(results_df):
    """
    Pie chart
    """
    traffic_counts = results_df['Type'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=traffic_counts.index,
        values=traffic_counts.values,
        hole=0.4
    )])
    
    fig.update_layout(
        title="Traffic Distribution",
        height=400
    )
    
    return fig

# Build interface
with gr.Blocks(title="NetInsight", theme=gr.themes.Soft()) as demo:
    
    gr.Markdown("""
    # 🔍 NetInsight
    ## Network Traffic Analyzer
    Upload a PCAP file to analyze and classify network traffic
    """)
    
    with gr.Row():
        with gr.Column():
            # Input
            gr.Markdown("### 📤 Upload PCAP")
            pcap_input = gr.File(
                label="Select PCAP file",
                file_types=[".pcap", ".pcapng"]
            )
            
            analyze_btn = gr.Button(
                "🚀 Analyze",
                variant="primary",
                size="lg"
            )
            
        with gr.Column():
            # Output: Summary
            summary_output = gr.Markdown(
                value="Upload a file to see results..."
            )
    
    with gr.Row():
        # Output: Chart
        pie_output = gr.Plot(label="Traffic Distribution")
    
    # Output: Table
    gr.Markdown("### 📊 Detailed Results")
    table_output = gr.Dataframe(
        label="Flow Analysis",
        wrap=True
    )
    
    # Connect button
    analyze_btn.click(
        fn=analyze_pcap,
        inputs=[pcap_input],
        outputs=[summary_output, pie_output, table_output]
    )

# Launch
demo.launch(share=False)
```

**הרצה:**
```bash
python gradio_app.py
# פתח: http://localhost:7860
```

---

## 🎨 אופציה B: Flask (למתקדמים)

**קוד בסיסי:**

```python
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize
extractor = FeatureExtractor()
classifier = HybridClassifier()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'pcap_file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['pcap_file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Analyze
    features_df = extractor.extract_from_pcap(filepath)
    
    results = []
    for idx in range(len(features_df)):
        features = features_df.iloc[idx].to_dict()
        traffic_type, conf, method = classifier.classify(features)
        
        results.append({
            'flow': idx + 1,
            'type': traffic_type,
            'confidence': float(conf)
        })
    
    os.remove(filepath)
    
    return jsonify({
        'success': True,
        'results': results
    })

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
```

**index.html (פשוט):**

```html
<!DOCTYPE html>
<html>
<head>
    <title>NetInsight</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .upload-area {
            border: 2px dashed #ccc;
            padding: 40px;
            text-align: center;
            margin: 20px 0;
        }
        button {
            background: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>🔍 NetInsight</h1>
    <div class="upload-area">
        <input type="file" id="pcapFile" accept=".pcap,.pcapng">
        <button onclick="analyze()">Analyze</button>
    </div>
    <div id="results"></div>
    
    <script>
        async function analyze() {
            const file = document.getElementById('pcapFile').files[0];
            const formData = new FormData();
            formData.append('pcap_file', file);
            
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            // Display results
            document.getElementById('results').innerHTML = 
                '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        }
    </script>
</body>
</html>
```

---

### דקות 60-75: בדיקות ושיפורים

**✅ רשימת בדיקות:**

```
☑ העלאת PCAP עובדת
☑ הניתוח מסתיים בהצלחה
☑ התוצאות מוצגות כראוי
☑ הגרפים נראים טוב
☑ אין שגיאות בconsole
☑ זמן תגובה סביר (<5 שניות)
```

---

## 📤 תוצר להגשה - שלב 4

### קבצים:

```
📁 ui_[שם_קבוצה]/
├── gradio_app.py (או flask_app.py)
├── screenshots/
│   ├── interface.png
│   ├── results.png
│   └── charts.png
├── demo_video.mp4 (אופציונלי)
└── README.txt
```

### Screenshots חשובים:

1. **interface.png** - הממשק הראשי
2. **results.png** - תוצאות ניתוח
3. **charts.png** - גרפים

---

## 💡 טיפים לממשק טוב

✅ **פשוט = טוב:**
אל תגזימו עם features

✅ **הדגימו טוב:**
Screenshots + וידאו קצר

✅ **טסטו על PCAP אמיתיים:**
לא רק על אלה שיצרתם

✅ **Error handling:**
מה קורה אם מעלים קובץ לא תקין?

---

# 🎯 שלב 5: מצגת והצגה (30 דקות + 3 דקות הצגה)

## 🎯 המטרה
להציג את העבודה שלכם בצורה מרשימה ומשכנעת

## 📋 משימות הקבוצה

### דקות 0-25: הכנת המצגת

**מבנה מומלץ (5 שקפים):**

---

### שקף 1: כותרת

```
=============================================
       NetInsight
   Network Traffic Analyzer
=============================================

צוות: [שמות כל חברי הקבוצה]
תאריך: [תאריך]

בית ספר: תיכון בליך
מגמת: סייבר
=============================================
```

---

### שקף 2: האתגר

```
🎯 מה הבעיה?
================

ברשתות מודרניות עוברים מיליוני packets בשנייה

❓ איך יודעים מה סוג התעבורה?
   • האם זה וידאו של Netflix?
   • משחק אונליין?
   • שיחת Zoom?

🔐 למה זה חשוב?
   • ניטור רשת ארגונית
   • זיהוי פעילות חשודה
   • אופטימיזציה של bandwidth
```

---

### שקף 3: הפתרון שלנו

```
💡 הגישה שלנו: Hybrid Classification
==========================================

     📏 Layer 1: Rule-Based
        ↓
     (בטוח?)
        ↓ לא
     🤖 Layer 2: Machine Learning
        ↓
     ✅ תוצאה

📊 ביצועים:
   • דיוק כולל: 87%
   • מהירות: 650 flows/sec
   • 5 סוגי תעבורה

🔬 Features:
   • גודל packets
   • תדירות
   • סימטריה
   • +27 נוספים
```

---

### שקף 4: הדגמה

```
🎬 הדגמה חיה!
================

[כאן תריצו את הממשק ותראו איך זה עובד]

1. העלאת PCAP ✓
2. ניתוח אוטומטי ✓
3. תוצאות + גרפים ✓

[screenshot של הממשק עם תוצאות]
```

---

### שקף 5: סיכום

```
✨ מה השגנו?
================

✅ מחקר מעמיק על סוגי תעבורה
✅ 5 datasets סימולטיביים
✅ אלגוריתם היברידי מתקדם
✅ ממשק אינטראקטיבי
✅ 87% דיוק!

🎓 מה למדנו?
   • ניתוח רשתות בעומק
   • Machine Learning מעשי
   • עבודת צוות תחת לחץ

        תודה רבה! 🙏
      [email / GitHub לקוד]
```

---

### דקות 25-30: תרגול ההצגה

**🎭 חלוקת דיבור:**

```
תלמיד A (30 שניות): כותרת + האתגר
תלמיד B (45 שניות): הפתרון + ביצועים
תלמיד C (60 שניות): DEMO LIVE!
תלמיד D (30 שניות): סיכום + לימודים
------------------------
סה"כ: ~2:45 דקות
```

**💡 טיפים להצגה:**

✅ **תרגלו! תרגלו! תרגלו!**
לפחות 3 פעמים לפני האירוע

✅ **Demo מוכן מראש:**
אל תסמכו על אינטרנט/רשת

✅ **דברו בביטחון:**
אתם מומחים בנושא!

✅ **חייכו:**
תהנו מהרגע!

❌ **טעויות נפוצות:**
- קריאה ישירה מהמצגת
- הסבר טכני מדי
- Demo לא עובד
- חריגה מהזמן

---

## 📤 תוצר להגשה - שלב 5

```
📁 presentation_[שם_קבוצה]/
├── presentation.pptx      # המצגת
├── demo_screenshots/      # צילומי מסך
└── script.txt            # הטקסט שתגידו
```

---

# 📊 דוגמאות תוצרים איכותיים

## דוגמה 1: טבלת תוצאות ניתוח

```
+--------+-------------+------------+--------+---------+-------+
| Flow # | Type        | Confidence | Method | Packets | Bytes |
+--------+-------------+------------+--------+---------+-------+
| 1      | Streaming   | 100%       | Rule   | 2,456   | 3.5MB |
| 2      | Streaming   | 100%       | Rule   | 1,987   | 2.8MB |
| 3      | Gaming      | 100%       | Rule   | 7,680   | 768KB |
| 4      | Video_Call  | 92%        | ML     | 3,200   | 1.6MB |
| 5      | Gaming      | 100%       | Rule   | 7,680   | 740KB |
+--------+-------------+------------+--------+---------+-------+
```

---

## דוגמה 2: Confusion Matrix

```
                  Predicted
              Stream  Game  Video
Actual Stream   45     2     0
       Game      1    52     3
       Video     2     3    42

Accuracy: 91.7%
```

---

## דוגמה 3: Feature Importance

```
Top 10 Most Important Features:
================================

 1. ████████████████████░░░░░ mean_packet_size (35.4%)
 2. ████████████░░░░░░░░░░░░░ download_ratio (21.9%)
 3. █████████░░░░░░░░░░░░░░░░ packet_rate (16.5%)
 4. ██████░░░░░░░░░░░░░░░░░░░ symmetry (12.0%)
 5. ████░░░░░░░░░░░░░░░░░░░░░ iat_cv (8.9%)
 6. ███░░░░░░░░░░░░░░░░░░░░░░ std_packet_size (5.3%)
```

---

## דוגמה 4: סיכום ביצועים

```
╔═══════════════════════════════════════════╗
║      NetInsight Performance Report        ║
╠═══════════════════════════════════════════╣
║                                           ║
║  Overall Accuracy:        87.2%           ║
║                                           ║
║  Per-Class Performance:                   ║
║    • Streaming:          92.3%            ║
║    • Gaming:             89.1%            ║
║    • Video Calls:        84.5%            ║
║                                           ║
║  Processing Speed:       650 flows/sec    ║
║                                           ║
║  Method Distribution:                     ║
║    • Rule-Based:         45%              ║
║    • ML-Based:           55%              ║
║                                           ║
╚═══════════════════════════════════════════╝
```

---

# ✅ Checklist סופי

## לפני ההגשה:

```
שלב 1:
☑ מסמך מחקר מלא (3 סוגי תעבורה)
☑ טבלת השוואה
☑ רשימת מקורות

שלב 2:
☑ 3-5 קבצי PCAP
☑ metadata.csv
☑ README מסביר

שלב 3:
☑ קוד Feature Extraction
☑ קוד Classifier
☑ מודל מאומן (.pkl)
☑ דוח ביצועים
☑ Confusion matrix

שלב 4:
☑ קוד ממשק משתמש
☑ Screenshots
☑ הוראות הרצה

שלב 5:
☑ מצגת 5 שקפים
☑ Demo מוכן
☑ תרגלנו את ההצגה
```

---

# 🎯 לסיכום

זהו! עכשיו יש לכם מדריך מלא לכל שלבי ההאקתון.

**זכרו:**
1. ✅ עבדו כקבוצה
2. ✅ תקשרו ביניכם
3. ✅ אל תפחדו לשאול
4. ✅ תהנו מהתהליך!

**בהצלחה! 🚀**

---

**מסמך זה נכתב במיוחד עבור תלמידי תיכון בליך**
**מגמת סייבר | האקתון NetInsight 2025**
