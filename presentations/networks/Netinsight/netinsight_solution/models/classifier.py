#!/usr/bin/env python3
"""
NetInsight - Traffic Classifier
אלגוריתם סיווג היברידי: Rule-Based + Machine Learning

הגישה:
1. Layer 1: Rule-Based - זיהוי מהיר לפי פורטים וגדלים קיצוניים
2. Layer 2: ML-Based - Decision Tree למקרים מורכבים
"""

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os


class HybridTrafficClassifier:
    """
    מסווג תעבורת רשת היברידי
    """
    
    def __init__(self):
        self.ml_model = None
        self.feature_names = None
        self.classes = ['Streaming', 'Gaming', 'Video_Call', 'Web_Browsing', 'File_Transfer']
        
        # Rule-based thresholds (מתוך המחקר)
        self.rules = {
            'gaming': {
                'mean_packet_size': (50, 200),      # קטנים
                'packet_rate': (30, 150),            # תדירות גבוהה
                'symmetry': (0.3, 0.7),              # סימטרי
                'iat_cv': (0, 0.5)                   # קבוע
            },
            'streaming': {
                'mean_packet_size': (800, 1500),     # גדולים
                'download_ratio': (0.7, 1.0),        # בעיקר download
                'burst_count': (5, 1000),            # bursts
                'bandwidth': (100000, 10000000)      # bandwidth גבוה
            },
            'video_call': {
                'mean_packet_size': (300, 800),      # בינוניים
                'symmetry': (0.3, 0.7),              # סימטרי
                'packet_rate': (20, 100)             # בינוני
            },
            'file_transfer': {
                'mean_packet_size': (1000, 1500),    # גדולים
                'bandwidth': (1000000, 100000000),   # מאוד גבוה
                'burst_count': (10, 1000)            # burst רציף
            }
        }
    
    def rule_based_classify(self, features):
        """
        Layer 1: סיווג מבוסס כללים
        
        Args:
            features: dict של features
        
        Returns:
            class name או None אם לא בטוח
        """
        
        # --- Gaming Detection ---
        # Gaming: קטן + מהיר + סימטרי + קבוע
        if (self._in_range(features.get('mean_packet_size', 0), 
                          self.rules['gaming']['mean_packet_size']) and
            self._in_range(features.get('packet_rate', 0), 
                          self.rules['gaming']['packet_rate']) and
            self._in_range(features.get('symmetry', 0), 
                          self.rules['gaming']['symmetry'])):
            
            # Additional check: UDP protocol (most games use UDP)
            if features.get('protocol', '') == 'UDP':
                return 'Gaming'
        
        # --- Streaming Detection ---
        # Streaming: גדול + asymmetric + bursts + bandwidth גבוה
        if (self._in_range(features.get('mean_packet_size', 0), 
                          self.rules['streaming']['mean_packet_size']) and
            self._in_range(features.get('download_ratio', 0), 
                          self.rules['streaming']['download_ratio']) and
            features.get('bandwidth', 0) > self.rules['streaming']['bandwidth'][0]):
            return 'Streaming'
        
        # --- Video Call Detection ---
        # Video Call: בינוני + סימטרי + UDP
        if (self._in_range(features.get('mean_packet_size', 0), 
                          self.rules['video_call']['mean_packet_size']) and
            self._in_range(features.get('symmetry', 0), 
                          self.rules['video_call']['symmetry']) and
            features.get('protocol', '') == 'UDP'):
            return 'Video_Call'
        
        # --- File Transfer Detection ---
        # File Transfer: גדול מאוד + bandwidth גבוה + burst אחד ארוך
        if (features.get('bandwidth', 0) > self.rules['file_transfer']['bandwidth'][0] and
            features.get('mean_packet_size', 0) > 1000 and
            features.get('download_ratio', 0) > 0.8):
            return 'File_Transfer'
        
        # --- Port-based hints ---
        ports = [features.get('port1', 0), features.get('port2', 0)]
        
        # HTTP/HTTPS ports
        if 80 in ports or 443 in ports:
            # Could be streaming or browsing
            if features.get('flow_duration', 0) > 30:
                return 'Streaming'
            else:
                return 'Web_Browsing'
        
        # DNS port
        if 53 in ports:
            return 'Web_Browsing'
        
        # If no rule matched, return None (will use ML)
        return None
    
    def _in_range(self, value, range_tuple):
        """
        בדיקה אם ערך בטווח
        """
        return range_tuple[0] <= value <= range_tuple[1]
    
    def train_ml_model(self, X_train, y_train, model_type='decision_tree'):
        """
        Layer 2: אימון מודל ML
        
        Args:
            X_train: features (DataFrame)
            y_train: labels (Series)
            model_type: 'decision_tree' או 'random_forest'
        """
        print("\n" + "=" * 60)
        print("Training ML Model")
        print("=" * 60)
        
        # Select features (remove non-numeric)
        numeric_features = X_train.select_dtypes(include=[np.number]).columns
        X_train_numeric = X_train[numeric_features]
        self.feature_names = list(numeric_features)
        
        print(f"Features used: {len(self.feature_names)}")
        print(f"Training samples: {len(X_train)}")
        print(f"Classes: {np.unique(y_train)}")
        
        # Train model
        if model_type == 'decision_tree':
            print("\n[*] אימון Decision Tree...")
            self.ml_model = DecisionTreeClassifier(
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            )
        else:
            print("\n[*] אימון Random Forest...")
            self.ml_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42
            )
        
        self.ml_model.fit(X_train_numeric, y_train)
        
        # Feature importance
        if hasattr(self.ml_model, 'feature_importances_'):
            importances = self.ml_model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            print("\n[*] Top 10 Most Important Features:")
            for i in range(min(10, len(indices))):
                idx = indices[i]
                print(f"  {i+1}. {self.feature_names[idx]}: {importances[idx]:.4f}")
        
        print("\n[✓] Model trained successfully")
    
    def ml_classify(self, features):
        """
        Layer 2: סיווג עם ML
        
        Args:
            features: dict או DataFrame
        
        Returns:
            class name
        """
        if self.ml_model is None:
            raise ValueError("Model not trained. Call train_ml_model() first.")
        
        # Convert to DataFrame if dict
        if isinstance(features, dict):
            features_df = pd.DataFrame([features])
        else:
            features_df = features
        
        # Select only numeric features used in training
        features_numeric = features_df[self.feature_names]
        
        # Predict
        prediction = self.ml_model.predict(features_numeric)[0]
        
        return prediction
    
    def classify(self, features, use_rules=True):
        """
        הסיווג המלא: Rule-Based → ML
        
        Args:
            features: dict או DataFrame של features
            use_rules: האם להשתמש ב-rules לפני ML
        
        Returns:
            (class_name, confidence, method)
        """
        # Try rule-based first
        if use_rules:
            if isinstance(features, dict):
                rule_result = self.rule_based_classify(features)
            else:
                # If DataFrame, convert first row to dict
                rule_result = self.rule_based_classify(features.iloc[0].to_dict())
            
            if rule_result is not None:
                return rule_result, 1.0, 'rule-based'
        
        # If rule-based didn't work, use ML
        ml_result = self.ml_classify(features)
        
        # Get confidence from ML
        if isinstance(features, dict):
            features_df = pd.DataFrame([features])
        else:
            features_df = features
        
        features_numeric = features_df[self.feature_names]
        
        if hasattr(self.ml_model, 'predict_proba'):
            probabilities = self.ml_model.predict_proba(features_numeric)[0]
            confidence = max(probabilities)
        else:
            confidence = 0.8  # Default for models without probability
        
        return ml_result, confidence, 'ml-based'
    
    def evaluate(self, X_test, y_test):
        """
        הערכת המודל על test set
        
        Returns:
            dict עם מדדי ביצועים
        """
        print("\n" + "=" * 60)
        print("Model Evaluation")
        print("=" * 60)
        
        # Prepare data
        X_test_numeric = X_test[self.feature_names]
        
        # Predictions
        y_pred = []
        methods_used = {'rule-based': 0, 'ml-based': 0}
        
        for idx in range(len(X_test)):
            features = X_test.iloc[idx].to_dict()
            pred, conf, method = self.classify(features)
            y_pred.append(pred)
            methods_used[method] += 1
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n[*] Accuracy: {accuracy:.2%}")
        print(f"\n[*] Classification Method Distribution:")
        print(f"    Rule-based: {methods_used['rule-based']} ({methods_used['rule-based']/len(X_test)*100:.1f}%)")
        print(f"    ML-based: {methods_used['ml-based']} ({methods_used['ml-based']/len(X_test)*100:.1f}%)")
        
        # Classification report
        print("\n[*] Classification Report:")
        print(classification_report(y_test, y_pred, zero_division=0))
        
        # Confusion matrix
        print("\n[*] Confusion Matrix:")
        cm = confusion_matrix(y_test, y_pred, labels=self.classes)
        cm_df = pd.DataFrame(cm, index=self.classes, columns=self.classes)
        print(cm_df)
        
        return {
            'accuracy': accuracy,
            'y_pred': y_pred,
            'y_test': y_test,
            'methods_used': methods_used,
            'confusion_matrix': cm
        }
    
    def save_model(self, filepath='traffic_classifier.pkl'):
        """
        שמירת המודל לקובץ
        """
        model_data = {
            'ml_model': self.ml_model,
            'feature_names': self.feature_names,
            'classes': self.classes,
            'rules': self.rules
        }
        joblib.dump(model_data, filepath)
        print(f"\n[✓] Model saved to {filepath}")
    
    def load_model(self, filepath='traffic_classifier.pkl'):
        """
        טעינת מודל מקובץ
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file {filepath} not found")
        
        model_data = joblib.load(filepath)
        self.ml_model = model_data['ml_model']
        self.feature_names = model_data['feature_names']
        self.classes = model_data['classes']
        self.rules = model_data['rules']
        
        print(f"[✓] Model loaded from {filepath}")


def main():
    """
    דוגמה לשימוש
    """
    print("NetInsight Traffic Classifier")
    print("=" * 60)
    
    # Create classifier
    classifier = HybridTrafficClassifier()
    
    # Example: Test with sample features
    sample_features = {
        'protocol': 'UDP',
        'port1': 50000,
        'port2': 27015,
        'mean_packet_size': 120,
        'packet_rate': 64,
        'symmetry': 0.5,
        'iat_cv': 0.2,
        'bandwidth': 50000,
        'download_ratio': 0.5,
        'burst_count': 2
    }
    
    print("\n[*] Testing rule-based classification...")
    result = classifier.rule_based_classify(sample_features)
    print(f"Result: {result}")
    
    print("\n[✓] Classifier is ready")
    print("    - To train ML model: see train_model.py")
    print("    - To use in UI: see gradio_app.py")


if __name__ == "__main__":
    main()
