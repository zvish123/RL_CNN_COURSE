# NetInsight - פתרון מלא להאקתון ניתוח תעבורת רשת

## 🎯 סקירה כללית
פתרון מקיף למערכת ניתוח וסיווג תעבורת רשת בזמן אמת, כולל:
- יצירת datasets סימולטיביים
- אלגוריתם סיווג היברידי (Rule-Based + ML)
- ממשק משתמש אינטראקטיבי עם Gradio

## 📁 מבנה הפרויקט
```
netinsight_solution/
├── docs/                    # שלב 1: מסמכי מחקר
│   └── research_report.md
├── datasets/                # שלב 2: קבצי PCAP ו-CSV
│   ├── generate_datasets.py
│   └── [קבצי PCAP שנוצרו]
├── models/                  # שלב 3: אלגוריתם הסיווג
│   ├── classifier.py
│   ├── feature_extractor.py
│   └── train_model.py
├── ui/                      # שלב 4: ממשק משתמש
│   ├── gradio_app.py
│   └── flask_app.py
├── requirements.txt
└── README.md
```

## 🚀 הרצה מהירה

### 1. התקנת תלויות
```bash
pip install -r requirements.txt
```

### 2. יצירת Datasets (שלב 2)
```bash
cd datasets
sudo python3 generate_datasets.py
```

### 3. אימון המודל (שלב 3)
```bash
cd models
python3 train_model.py
```

### 4. הרצת ממשק המשתמש (שלב 4)
```bash
# Gradio (מומלץ - פשוט יותר)
cd ui
python3 gradio_app.py

# או Flask
python3 flask_app.py
```

## 🧠 הגישה האלגוריתמית

### סיווג היברידי (Hybrid Classification)
המערכת משלבת שתי גישות:

1. **Rule-Based Layer** - זיהוי מהיר לפי:
   - פורטים ידועים (80=HTTP, 443=HTTPS, 53=DNS)
   - גודלי packets אופייניים
   - תדירות תקשורת

2. **ML Layer** - למקרים מורכבים:
   - Decision Tree Classifier
   - Features: packet size stats, inter-arrival times, protocol distribution
   - דיוק: ~85-90%

## 📊 סוגי תעבורה נתמכים
- 🌐 Web Browsing (HTTP/HTTPS)
- 📹 Video Streaming (YouTube, Netflix)
- 🎮 Gaming (Real-time gaming traffic)
- 💬 Video Calls (Zoom, Teams)
- 📁 File Transfer (FTP, Cloud Sync)

## 🏆 תוצרים לכל שלב
- ✅ שלב 1: מסמך מחקר מפורט (docs/research_report.md)
- ✅ שלב 2: 5 קבצי PCAP + CSV metadata
- ✅ שלב 3: מודל ML מאומן + דוח ביצועים
- ✅ שלב 4: ממשק Gradio אינטראקטיבי
- ✅ שלב 5: מצגת והדגמה

## 🛠️ טכנולוגיות בשימוש
- **Scapy**: מניפולציה ויצירת packets
- **pandas**: עיבוד נתונים
- **scikit-learn**: אלגוריתמי ML
- **Gradio**: ממשק משתמש אינטראקטיבי
- **matplotlib/plotly**: ויזואליזציה

## 📈 ביצועים
- דיוק סיווג: 85-90%
- זמן עיבוד: ~0.1 שניות לכל flow
- תמיכה ב-real-time analysis

## 👥 פותח על ידי
צוות NetInsight | תיכון בליך | מגמת סייבר 2025
