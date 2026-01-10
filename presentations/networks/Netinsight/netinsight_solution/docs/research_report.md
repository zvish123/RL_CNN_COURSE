# מסמך מחקר - ניתוח סוגי תעבורת רשת
## שלב 1: מחקר והבנה

---

## 1️⃣ Video Streaming (Netflix, YouTube)

### מאפיינים ייחודיים

**גודלי Packets:**
- גדלים משתנים: 200-1500 bytes
- רוב ה-packets בגודל מקסימלי (MTU = 1500)
- Burst mode: הרבה packets ברצף
- אין symmetry: הרבה download, מעט upload

**תדירות תקשורת:**
- קבועה ורציפה (Continuous flow)
- ~25-60 packets לשנייה למשך זמן ארוך
- לא רגישה במיוחד ל-latency (עד 2-3 שניות OK)
- רגישה מאוד ל-bandwidth

**פורטים נפוצים:**
- HTTP/HTTPS: 80, 443 (YouTube, Netflix)
- RTMP: 1935 (Streaming protocols)
- QUIC: UDP 443 (YouTube משתמש הרבה)

### פרוטוקולים בשימוש
- **HTTP/2 או HTTP/3 (QUIC)**: הרוב של הסטרימינג המודרני
- **TCP**: עבור HTTP/1.1 ו-HTTP/2
- **UDP**: עבור QUIC (YouTube)
- **TLS 1.2/1.3**: הצפנה
- **DASH/HLS**: פרוטוקולי adaptive streaming

### דפוסי התנהגות אופייניים
1. **Startup Phase**: כמה seconds של burst עם packets קטנים (requests)
2. **Buffering Phase**: burst גדול של data (initial buffer)
3. **Steady Streaming**: flow קבוע ורציף
4. **Adaptive Behavior**: שינויי איכות לפי bandwidth (קפיצות בגודלי segments)

**Bandwidth Usage:**
- 480p: ~1-2 Mbps
- 720p: ~3-5 Mbps
- 1080p: ~5-8 Mbps
- 4K: 15-25 Mbps

**Signature Pattern:**
- Long-lived connections (minutes to hours)
- High download ratio (asymmetric)
- Periodic patterns (segment fetching every 2-10 seconds)

---

## 2️⃣ Gaming (Fortnite, Valorant, CS:GO)

### מאפיינים ייחודיים

**גודלי Packets:**
- קטנים מאוד: 50-200 bytes בממוצע
- גדלים קבועים יחסית
- Symmetric traffic (דו-כיווני בערך שווה)
- בעיקר UDP packets

**תדירות תקשורת:**
- גבוהה מאוד: 30-128 packets/second
- תדירות קבועה (תלוי ב-tick rate של המשחק)
- קבועה גם בזמן "אי-פעילות" במשחק
- רגישה מאוד ל-latency (<50ms ideal)

**פורטים נפוצים:**
- UDP: טווחים דינמיים (27000-27100, 7777-7778)
- Fortnite: UDP 9000-9100
- Valorant: UDP 8180-8198
- CS:GO: UDP 27015

### פרוטוקולים בשימוש
- **UDP**: פרוטוקול עיקרי (real-time, לא צריך reliability)
- **Custom Game Protocols**: פרוטוקולים ייעודיים של כל משחק
- **TCP**: רק ל-lobby, matchmaking, chat
- **DTLS/SSL**: הצפנה במשחקים מסוימים

### דפוסי התנהגות אופייניים
1. **Connection Phase**: TCP handshakes, authentication
2. **In-Game Phase**: 
   - UDP packets ברצף קבוע
   - גדלים דומים
   - Low latency requirement
3. **State Updates**: player position, actions - 30-64 times/sec
4. **Heartbeat packets**: keep-alive messages

**Network Requirements:**
- Latency: < 50ms (competitive), < 100ms (casual)
- Bandwidth: נמוך! 50-150 Kbps
- Packet Loss: < 1%
- Jitter: < 30ms

**Signature Pattern:**
- Constant bitrate (CBR)
- Small packets with fixed rate
- Low bandwidth, high frequency
- Bidirectional symmetry

---

## 3️⃣ Video Calls (Zoom, Teams, Google Meet)

### מאפיינים ייחודיים

**גודלי Packets:**
- וידאו: 200-1500 bytes (משתנה)
- אודיו: קטנים יותר 50-200 bytes
- בינוני: ~400-800 bytes ממוצע
- Symmetric או קרוב לכך (bidirectional)

**תדירות תקשורת:**
- וידאו: 20-30 frames/second
- אודיו: ~50 packets/second
- משתנה לפי איכות ותנאי רשת
- רגיש מאוד ל-latency וגם ל-jitter

**פורטים נפוצים:**
- UDP: 3478-3497 (WebRTC/STUN)
- Zoom: UDP 8801-8810
- Teams: UDP 3478-3481
- TCP fallback: 443 (אם UDP חסום)

### פרוטוקולים בשימוש
- **WebRTC**: הסטנדרט המודרני (Chrome, Meet)
- **RTP/RTCP**: Real-Time Protocol
- **SRTP**: Secure RTP (encrypted)
- **UDP**: כברירת מחדל
- **TCP/TLS**: backup אם UDP לא זמין
- **STUN/TURN**: NAT traversal

### דפוסי התנהגות אופייניים
1. **Setup Phase**: 
   - STUN/TURN negotiation
   - Signaling (TCP/HTTPS)
2. **Media Phase**:
   - Separate audio + video streams
   - Adaptive bitrate לפי תנאי רשת
3. **Quality Adjustments**:
   - Dynamic resolution changes
   - Frame rate adjustments
   - Audio vs Video prioritization

**Bandwidth Usage:**
- Audio only: 30-100 Kbps
- Video SD: 500 Kbps - 1 Mbps
- Video HD: 1-3 Mbps
- Screen sharing: +500 Kbps

**Network Requirements:**
- Latency: < 150ms (audio), < 300ms (video)
- Bandwidth: Variable (500 Kbps - 3 Mbps)
- Packet Loss: < 3% (with FEC)
- Jitter: < 50ms

**Signature Pattern:**
- Bidirectional traffic (both upload and download)
- Constant stream with variations
- Multiple concurrent flows (audio, video, data)
- Adaptive behavior based on network

---

## 📊 טבלת השוואה מהירה

| תכונה | Streaming | Gaming | Video Calls |
|-------|-----------|--------|-------------|
| גודל Packet ממוצע | 1000-1500B | 50-200B | 400-800B |
| תדירות | 25-60 pps | 30-128 pps | 30-80 pps |
| כיווניות | Asymmetric (↓) | Symmetric | Symmetric |
| פרוטוקול עיקרי | TCP/QUIC | UDP | UDP/RTP |
| רגישות Latency | נמוכה | גבוהה מאוד | גבוהה |
| Bandwidth | גבוה | נמוך | בינוני |
| דפוס | Continuous burst | CBR | Variable adaptive |

---

## 🔍 מסקנות למערכת הסיווג

### Features חשובים לזיהוי:
1. **גודל Packet**: 
   - Gaming: קטנים (<200B)
   - Streaming: גדולים (>1000B)
   - Calls: בינוניים (400-800B)

2. **תדירות ושונות**:
   - Gaming: קבועה מאוד (low jitter)
   - Streaming: bursts עם הפסקות
   - Calls: קבועה עם וריאציות

3. **כיווניות**:
   - Streaming: הרבה download
   - Gaming: symmetric
   - Calls: symmetric

4. **פרוטוקול ופורטים**:
   - רמז ראשוני חזק
   - לא תמיד אמין (dynamic ports, encryption)

5. **דפוסים זמניים**:
   - Inter-arrival times
   - Burst patterns
   - Session duration

### אסטרטגיית סיווג מומלצת:
1. **Layer 1: Rule-Based** - פורטים ידועים וגדלים קיצוניים
2. **Layer 2: Statistical** - חישוב features מקבוצות packets
3. **Layer 3: ML** - Decision Tree על features מחושבים

---

**מקורות:**
- RFC 3550 (RTP)
- WebRTC Specifications
- Wireshark Traffic Analysis Documentation
- "Computer Networking: A Top-Down Approach" - Kurose & Ross
