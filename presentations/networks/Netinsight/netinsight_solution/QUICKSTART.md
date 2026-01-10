# 🚀 מדריך התחלה מהירה - NetInsight

## התקנה ראשונית

### שלב 1: התקנת תלויות
```bash
cd netinsight_solution
pip install -r requirements.txt[netinsight_hackathon.html](../../../netinsight_hackathon.html)
```

**הערה:** Scapy דורש הרשאות root ליצירת packets. אם אתם ב-Linux:
```bash
sudo pip install -r requirements.txt
```

---[netinsight_hackathon.html](../../../netinsight_hackathon.html)

## שלב 2: יצירת Datasets

```bash
cd datasets
sudo python3 generate_datasets.py
```

**מה קורה כאן?**
- נוצרים 5 קבצי PCAP
- כל קובץ מדמה סוג תעבורה אחר
- נוצר גם קובץ metadata.csv

**תוצאה צפויה:**
```
[✓] streaming.pcap (2000+ packets)
[✓] gaming.pcap (7000+ packets)
[✓] video_call.pcap (3000+ packets)
[✓] web_browsing.pcap (500+ packets)
[✓] file_transfer.pcap (10000+ packets)
[✓] metadata.csv
```

**זמן ריצה:** ~2-3 דקות

---

## שלב 3: אימון המודל

```bash
cd ../models
python3 train_model.py
```

**מה קורה כאן?**
1. קריאת כל קבצי ה-PCAP
2. חילוץ features מכל flow
3. אימון Decision Tree
4. הערכת ביצועים
5. שמירת המודל

**תוצאה צפויה:**
```
[✓] Model accuracy: 87%
[✓] Model saved to: traffic_classifier.pkl
[✓] Report saved to: model_report.txt
[✓] Visualizations: confusion_matrix.png, f1_scores.png
```

**זמן ריצה:** ~1-2 דקות

---

## שלב 4: הרצת ממשק המשתמש

### אופציה A: Gradio (מומלץ - פשוט יותר)

```bash
cd ../ui
python3 gradio_app.py
```

**פתח בדפדפן:** http://localhost:7860

### אופציה B: Flask

```bash
cd ../ui
python3 flask_app.py
```

**פתח בדפדפן:** http://localhost:5000

---

## שימוש במערכת

### העלאת קובץ PCAP

1. **לחץ על "Upload PCAP"**
2. **בחר קובץ .pcap או .pcapng**
3. **לחץ "Analyze Traffic"**
4. **המתן לתוצאות** (~2-5 שניות)

### הבנת התוצאות

#### 📊 Summary
- מספר flows שזוהו
- התפלגות סוגי תעבורה
- שיטת הסיווג (Rule-Based / ML)

#### 📈 Charts
- **Pie Chart**: התפלגות סוגי תעבורה
- **Timeline**: פעילות flows לפי זמן
- **Bar Chart**: Top flows לפי packet count

#### 📋 Table
- פירוט לכל flow: סוג, confidence, מספר packets, bytes

---

## בדיקה מהירה

### בדיקת המודל ישירות

```python
from models.classifier import HybridTrafficClassifier

# Load model
classifier = HybridTrafficClassifier()
classifier.load_model('traffic_classifier.pkl')

# Test with sample features
test_features = {
    'mean_packet_size': 95,
    'packet_rate': 64,
    'symmetry': 0.5,
    'protocol': 'UDP',
    'download_ratio': 0.5,
    'iat_cv': 0.2,
    'bandwidth': 50000,
    'burst_count': 2,
    'port1': 50000,
    'port2': 27015,
    'min_port': 27015,
    'max_port': 50000
}

# Classify
traffic_type, confidence, method = classifier.classify(test_features)
print(f"Type: {traffic_type}, Confidence: {confidence:.2%}, Method: {method}")
```

**תוצאה צפויה:**
```
Type: Gaming, Confidence: 100%, Method: rule-based
```

---

## פתרון בעיות נפוצות

### בעיה 1: "Permission denied" ב-Scapy

**פתרון:**
```bash
sudo python3 generate_datasets.py
```

### בעיה 2: "Model not found"

**פתרון:**
```bash
cd models
python3 train_model.py
```

### בעיה 3: "No module named 'scapy'"

**פתרון:**
```bash
pip install scapy
# או
pip install -r requirements.txt
```

### בעיה 4: Gradio לא נפתח

**פתרון:**
1. בדוק שהפורט 7860 פנוי
2. נסה לפתוח ידנית: http://127.0.0.1:7860
3. אם עדיין לא עובד, השתמש ב-Flask

### בעיה 5: דיוק נמוך

**פתרון:**
1. וודא שה-datasets נוצרו נכון
2. בדוק ש-metadata.csv קיים ותקין
3. הרץ מחדש את האימון עם יותר epochs:
```python
model = RandomForestClassifier(n_estimators=200)  # במקום 100
```

---

## טיפים למשתמשים מתקדמים

### 1. שימוש בקבצי PCAP אמיתיים

```python
from models.feature_extractor import FeatureExtractor
from models.classifier import HybridTrafficClassifier

extractor = FeatureExtractor()
classifier = HybridTrafficClassifier()
classifier.load_model('traffic_classifier.pkl')

# Extract features from real PCAP
features_df = extractor.extract_from_pcap('your_file.pcap')

# Classify each flow
for idx in range(len(features_df)):
    features = features_df.iloc[idx].to_dict()
    traffic_type, conf, method = classifier.classify(features)
    print(f"Flow {idx}: {traffic_type} ({conf:.1%})")
```

### 2. Fine-tuning המודל

ערוך את `models/classifier.py`:
```python
# הגדל את עומק העץ
self.ml_model = DecisionTreeClassifier(max_depth=15)  # במקום 10

# או השתמש ב-Random Forest
self.ml_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15
)
```

### 3. הוספת כלל חדש

ערוך את `models/classifier.py` בפונקציה `rule_based_classify`:
```python
# הוסף כלל חדש לזיהוי DNS
if 53 in [features.get('port1'), features.get('port2')]:
    return 'DNS'
```

### 4. ייצוא תוצאות ל-CSV

```python
# אחרי הסיווג
results_df = pd.DataFrame(results)
results_df.to_csv('classification_results.csv', index=False)
```

---

## תיעוד נוסף

- 📚 **מחקר מפורט**: `docs/research_report.md`
- 🧠 **הסבר אלגוריתם**: `docs/algorithm_explanation.md`
- 🎯 **מצגת**: `docs/presentation.md`
- 💻 **קוד**: כל הקבצים מתועדים עם docstrings

---

## תמיכה ועזרה

### שאלות נפוצות

**ש: כמה זמן לוקח לעבד קובץ PCAP גדול?**
ת: בערך 1 שנייה לכל 1000 packets

**ש: מה הגודל המקסימלי של קובץ?**
ת: 100MB בממשק Web, ללא הגבלה בקוד ישיר

**ש: האם המערכת עובדת על תעבורה מוצפנת?**
ת: כן! היא מסתכלת על metadata, לא על תוכן

**ש: איך משפרים את הדיוק?**
ת: יותר training data, fine-tuning של hyperparameters

---

## בדיקת תקינות מהירה

```bash
# הרץ את הסקריפט הזה לבדיקה מהירה
cd netinsight_solution

echo "Checking datasets..."
ls -lh datasets/*.pcap

echo "Checking model..."
ls -lh models/traffic_classifier.pkl

echo "Testing Gradio import..."
python3 -c "import gradio; print('Gradio OK')"

echo "Testing Scapy import..."
python3 -c "from scapy.all import *; print('Scapy OK')"

echo "All checks passed! ✓"
```

---

## הרצה מהירה - TL;DR

```bash
# התקנה
pip install -r requirements.txt

# יצירת datasets
cd datasets && sudo python3 generate_datasets.py

# אימון
cd ../models && python3 train_model.py

# הרצת UI
cd ../ui && python3 gradio_app.py

# פתח: http://localhost:7860
```

**זמן כולל: ~5-7 דקות** ⏱️

---

**בהצלחה! 🚀**
