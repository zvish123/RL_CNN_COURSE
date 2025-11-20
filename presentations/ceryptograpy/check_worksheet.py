"""
בודק תרגילים - רשימות דו-ממדיות
===============================
סקריפט לבדיקה אוטומטית של תרגילי דף העבודה
קורא קובץ JSON של תלמיד ובודק את התשובות

שימוש:
python check_worksheet.py <student_file.json>

או להרצה אינטראקטיבית:
python check_worksheet.py
"""

import json
import sys
import os
from typing import Dict, Any, List, Tuple
import re


class WorksheetChecker:
    """בודק תרגילי דף עבודה - רשימות דו-ממדיות"""
    
    def __init__(self):
        self.total_score = 0
        self.max_score = 100
        self.results = []
        
    def load_student_work(self, filepath: str) -> Dict[str, Any]:
        """טוען קובץ JSON של תלמיד"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ שגיאה: הקובץ {filepath} לא נמצא")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"❌ שגיאה: הקובץ {filepath} אינו קובץ JSON תקין")
            sys.exit(1)
    
    def check_exercise_1(self, answers: Dict[str, str]) -> Tuple[int, str]:
        """בדיקת תרגיל 1: הבנת המבנה (10 נקודות)"""
        score = 0
        feedback = "תרגיל 1 - הבנת המבנה:\n"
        
        # תשובות נכונות
        correct_answers = {
            'table_input_1': '30',    # data[0][2]
            'table_input_2': '100',   # data[2][1]
            'table_input_3': '3',     # len(data) - מספר שורות
            'table_input_4': '4',     # len(data[0]) - מספר עמודות
        }
        
        # בדיקת שאלות א
        for i in range(1, 5):
            key = f'table_input_{i}'
            student_answer = answers.get(key, '').strip()
            correct = correct_answers.get(key, '')
            
            if student_answer == correct:
                score += 2
                feedback += f"  ✅ שאלה א.{i}: נכון ({correct})\n"
            else:
                feedback += f"  ❌ שאלה א.{i}: שגוי. התשובה: '{student_answer}', נכון: '{correct}'\n"
        
        # בדיקת שאלה ב - הפקודה שמדפיסה 110
        answer_b = answers.get('answer_1', '').strip()
        if 'data[2][2]' in answer_b or 'print(data[2][2])' in answer_b:
            score += 2
            feedback += f"  ✅ שאלה ב: נכון - data[2][2]\n"
        else:
            feedback += f"  ❌ שאלה ב: לא מצאתי data[2][2] בתשובה\n"
            feedback += f"     התשובה שלך: {answer_b[:100]}\n"
        
        return score, feedback
    
    def check_exercise_2(self, answers: Dict[str, str]) -> Tuple[int, str]:
        """בדיקת תרגיל 2: משחק טיק-טק-טו (15 נקודות)"""
        score = 0
        feedback = "תרגיל 2 - משחק טיק-טק-טו:\n"
        
        # שאלה א - בדיקת שלושה X-ים בשורה הראשונה
        answer_a = answers.get('answer_2', '').lower()
        has_loop_or_condition = any(keyword in answer_a for keyword in ['if', 'for', 'and', '=='])
        has_row_zero = 'board[0]' in answer_a or '[0][' in answer_a
        
        if has_loop_or_condition and has_row_zero:
            score += 7
            feedback += "  ✅ שאלה א: יש לוגיקה של בדיקת שורה ראשונה (7/7)\n"
        elif has_row_zero:
            score += 4
            feedback += "  🟡 שאלה א: יש גישה לשורה ראשונה אבל חסר תנאי (4/7)\n"
        else:
            feedback += "  ❌ שאלה א: לא מצאתי פתרון מתאים (0/7)\n"
        
        # שאלה ב - ספירת תאים ריקים
        answer_b = answers.get('answer_3', '').lower()
        has_counter = 'count' in answer_b or 'sum' in answer_b or 'סופר' in answer_b
        has_nested_loops = answer_b.count('for') >= 2
        has_empty_check = "' '" in answer_b or '""' in answer_b or 'ריק' in answer_b
        
        points_b = 0
        if has_nested_loops:
            points_b += 3
        if has_counter:
            points_b += 3
        if has_empty_check:
            points_b += 2
        
        score += points_b
        feedback += f"  {'✅' if points_b >= 6 else '🟡' if points_b >= 3 else '❌'} שאלה ב: ({points_b}/8)\n"
        if points_b < 8:
            if not has_nested_loops:
                feedback += "     💡 חסרות לולאות מקוננות\n"
            if not has_counter:
                feedback += "     💡 חסר משתנה ספירה\n"
            if not has_empty_check:
                feedback += "     💡 חסרה בדיקת תא ריק\n"
        
        return score, feedback
    
    def check_exercise_3(self, answers: Dict[str, str]) -> Tuple[int, str]:
        """בדיקת תרגיל 3: מטריצה קסומה (20 נקודות)"""
        score = 0
        feedback = "תרגיל 3 - מטריצה קסומה:\n"
        
        answer = answers.get('answer_4', '').lower()
        
        # בדיקות קוד
        checks = {
            'פונקציה': ('def' in answer and 'is_magic_square' in answer, 3),
            'סכום שורות': (any(word in answer for word in ['sum', 'row', 'שורה']), 4),
            'סכום עמודות': (any(word in answer for word in ['col', 'עמוד']), 4),
            'אלכסון ראשי': (any(word in answer for word in ['diagonal', 'אלכסון', '[i][i]']), 4),
            'אלכסון משני': (('[len(' in answer or '[2]' in answer) and 'diagonal' in answer or 'משני' in answer, 3),
            'החזרת ערך': ('return' in answer, 2)
        }
        
        for check_name, (condition, points) in checks.items():
            if condition:
                score += points
                feedback += f"  ✅ {check_name}: {points}/{points}\n"
            else:
                feedback += f"  ❌ {check_name}: 0/{points}\n"
        
        return score, feedback
    
    def check_exercise_4(self, answers: Dict[str, str]) -> Tuple[int, str]:
        """בדיקת תרגיל 4: מציאת שכנים (15 נקודות)"""
        score = 0
        feedback = "תרגיל 4 - מציאת שכנים:\n"
        
        answer = answers.get('answer_5', '').lower()
        
        checks = {
            'פונקציה': ('def' in answer and 'find_neighbors' in answer, 3),
            'רשימת תוצאות': ('[]' in answer or 'list' in answer or 'רשימה' in answer, 2),
            'שכן עליון': ('row-1' in answer or '[i-1]' in answer or 'מעלה' in answer, 2),
            'שכן תחתון': ('row+1' in answer or '[i+1]' in answer or 'מטה' in answer, 2),
            'שכן שמאלי': ('col-1' in answer or '[j-1]' in answer or 'שמאל' in answer, 2),
            'שכן ימני': ('col+1' in answer or '[j+1]' in answer or 'ימין' in answer, 2),
            'בדיקת גבולות': (any(word in answer for word in ['if', '>=', '<=', '<', '>', 'len', 'גבול']), 2)
        }
        
        for check_name, (condition, points) in checks.items():
            if condition:
                score += points
                feedback += f"  ✅ {check_name}: {points}/{points}\n"
            else:
                feedback += f"  ❌ {check_name}: 0/{points}\n"
        
        return score, feedback
    
    def check_exercise_5(self, answers: Dict[str, str]) -> Tuple[int, str]:
        """בדיקת תרגיל 5: סיבוב מטריצה (25 נקודות)"""
        score = 0
        feedback = "תרגיל 5 - סיבוב מטריצה:\n"
        
        answer = answers.get('answer_6', '').lower()
        
        checks = {
            'פונקציה': ('def' in answer and 'rotate' in answer, 4),
            'מטריצה חדשה': ('[]' in answer and ('new' in answer or 'חדש' in answer or 'result' in answer), 4),
            'לולאות מקוננות': (answer.count('for') >= 2, 5),
            'הבנת טרנספורמציה': (any(word in answer for word in ['len-', '-1', 'reversed', 'הפוך']), 7),
            'החזרת תוצאה': ('return' in answer, 3),
            'אינדקסים נכונים': ('[j][' in answer or 'transpose' in answer, 2)
        }
        
        for check_name, (condition, points) in checks.items():
            if condition:
                score += points
                feedback += f"  ✅ {check_name}: {points}/{points}\n"
            else:
                feedback += f"  ❌ {check_name}: 0/{points}\n"
        
        return score, feedback
    
    def check_exercise_6(self, answers: Dict[str, str]) -> Tuple[int, str]:
        """בדיקת תרגיל 6 בונוס: מסלול במבוך (15 נקודות)"""
        score = 0
        feedback = "תרגיל 6 - מסלול במבוך (בונוס):\n"
        
        answer = answers.get('answer_7', '').lower()
        
        if not answer or len(answer.strip()) < 50:
            feedback += "  ⚪ לא נמצא פתרון\n"
            return 0, feedback
        
        checks = {
            'פונקציה': ('def' in answer and 'can_reach' in answer, 3),
            'רקורסיה או מחסנית': (any(word in answer for word in ['recursion', 'stack', 'queue', 'רקורסי', 'visited']), 5),
            'בדיקת גבולות': (any(word in answer for word in ['if', '>=', '<=', 'len', 'גבול']), 2),
            'סימון ביקור': ('visited' in answer or 'ביקור' in answer or 'seen' in answer, 3),
            'בדיקת קירות': ('== 1' in answer or '!= 0' in answer or 'קיר' in answer, 2)
        }
        
        for check_name, (condition, points) in checks.items():
            if condition:
                score += points
                feedback += f"  ✅ {check_name}: {points}/{points}\n"
            else:
                feedback += f"  ❌ {check_name}: 0/{points}\n"
        
        return score, feedback
    
    def check_exercise_7(self, answers: Dict[str, str]) -> Tuple[int, str]:
        """בדיקת תרגיל 7 אתגר: משחק 2048 (20 נקודות בונוס)"""
        score = 0
        feedback = "תרגיל 7 - משחק 2048 (אתגר מיוחד):\n"
        
        answer = answers.get('answer_8', '').lower()
        
        if not answer or len(answer.strip()) < 50:
            feedback += "  ⚪ לא נמצא פתרון\n"
            return 0, feedback
        
        checks = {
            'פונקציה': ('def' in answer and 'move_left' in answer, 3),
            'הזזת אפסים': (any(word in answer for word in ['!= 0', '> 0', 'remove', 'filter', 'אפס']), 5),
            'איחוד מספרים': (any(word in answer for word in ['*2', '* 2', '+', 'merge', 'איחוד']), 6),
            'שמירת סדר': (any(word in answer for word in ['append', 'insert', 'סדר']), 3),
            'טיפול באפסים בסוף': (any(word in answer for word in ['zeros', 'len', 'fill', 'אפס']), 3)
        }
        
        for check_name, (condition, points) in checks.items():
            if condition:
                score += points
                feedback += f"  ✅ {check_name}: {points}/{points}\n"
            else:
                feedback += f"  ❌ {check_name}: 0/{points}\n"
        
        return score, feedback
    
    def generate_report(self, student_data: Dict[str, Any]) -> str:
        """יוצר דוח מסכם"""
        student_name = student_data.get('studentInfo', {}).get('name', 'לא צוין')
        timestamp = student_data.get('timestamp', 'לא ידוע')
        
        report = f"""
{'='*60}
דוח בדיקה אוטומטית - רשימות דו-ממדיות
{'='*60}

שם התלמיד/ה: {student_name}
תאריך הגשה: {timestamp.split('T')[0] if 'T' in timestamp else timestamp}

{'='*60}

"""
        
        # הוסף כל תוצאה
        for result in self.results:
            report += result + "\n"
        
        # סיכום
        percentage = (self.total_score / self.max_score) * 100
        report += f"\n{'='*60}\n"
        report += f"ציון כולל: {self.total_score}/{self.max_score} ({percentage:.1f}%)\n"
        
        # הערכה
        if percentage >= 90:
            grade = "מצוין! 🌟"
        elif percentage >= 80:
            grade = "טוב מאוד! 👍"
        elif percentage >= 70:
            grade = "טוב 👌"
        elif percentage >= 60:
            grade = "עבודה סבירה"
        else:
            grade = "יש מקום לשיפור"
        
        report += f"הערכה: {grade}\n"
        report += f"{'='*60}\n"
        
        # הערות כלליות
        report += "\nהערות כלליות:\n"
        report += "✅ = הפתרון נכון או קרוב מאוד\n"
        report += "🟡 = הפתרון חלקי\n"
        report += "❌ = הפתרון חסר או שגוי\n"
        report += "⚪ = לא הוגש\n"
        report += "💡 = טיפ לשיפור\n"
        
        return report
    
    def check_all(self, filepath: str) -> str:
        """בודק את כל התרגילים ומחזיר דוח"""
        student_data = self.load_student_work(filepath)
        answers = student_data.get('answers', {})
        
        print(f"\n🔍 בודק את עבודת: {student_data.get('studentInfo', {}).get('name', 'לא צוין')}\n")
        
        # בדוק כל תרגיל
        exercises = [
            (self.check_exercise_1, "תרגיל 1"),
            (self.check_exercise_2, "תרגיל 2"),
            (self.check_exercise_3, "תרגיל 3"),
            (self.check_exercise_4, "תרגיל 4"),
            (self.check_exercise_5, "תרגיל 5"),
            (self.check_exercise_6, "תרגיל 6 (בונוס)"),
            (self.check_exercise_7, "תרגיל 7 (אתגר)")
        ]
        
        for check_func, name in exercises:
            print(f"בודק {name}...")
            score, feedback = check_func(answers)
            self.total_score += score
            self.results.append(feedback)
        
        # צור דוח
        report = self.generate_report(student_data)
        
        return report


def main():
    """פונקציה ראשית"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║   בודק תרגילים אוטומטי - רשימות דו-ממדיות בפייתון      ║
║                      צבי שירן                             ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # קבל שם קובץ
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        print("הכנס את שם קובץ ה-JSON של התלמיד:")
        filepath = input("> ").strip()
    
    if not os.path.exists(filepath):
        print(f"\n❌ הקובץ '{filepath}' לא נמצא")
        print("וודא שהקובץ נמצא בתיקיה הנוכחית או הכנס נתיב מלא")
        return
    
    # בדוק את העבודה
    checker = WorksheetChecker()
    report = checker.check_all(filepath)
    
    # הדפס דוח
    print("\n" + report)
    
    # שמור דוח לקובץ
    student_name = checker.load_student_work(filepath).get('studentInfo', {}).get('name', 'student')
    safe_name = re.sub(r'[^a-zA-Z0-9א-ת]', '_', student_name)
    report_filename = f"report_{safe_name}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n💾 הדוח נשמר לקובץ: {report_filename}")
    print("\n✅ הבדיקה הושלמה!")


if __name__ == "__main__":
    main()
