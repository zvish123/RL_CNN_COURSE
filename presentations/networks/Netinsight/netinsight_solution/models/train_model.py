#!/usr/bin/env python3
"""
NetInsight - Model Training
אימון המודל על datasets שנוצרו
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from feature_extractor import FeatureExtractor
from classifier import HybridTrafficClassifier
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns


def load_all_datasets(datasets_dir='../datasets'):
    """
    טעינת כל ה-datasets וחילוץ features
    """
    print("=" * 60)
    print("Loading and Processing Datasets")
    print("=" * 60)
    
    pcap_files = [
        ('streaming.pcap', 'Streaming'),
        ('gaming.pcap', 'Gaming'),
        ('video_call.pcap', 'Video_Call'),
        ('web_browsing.pcap', 'Web_Browsing'),
        ('file_transfer.pcap', 'File_Transfer')
    ]
    
    extractor = FeatureExtractor()
    all_features = []
    
    for pcap_file, label in pcap_files:
        filepath = os.path.join(datasets_dir, pcap_file)
        
        if not os.path.exists(filepath):
            print(f"[!] {pcap_file} not found, skipping...")
            continue
        
        print(f"\n[*] Processing {pcap_file}...")
        df = extractor.extract_from_pcap(filepath)
        
        if df is not None and len(df) > 0:
            df['label'] = label
            all_features.append(df)
            print(f"    [✓] Extracted {len(df)} flows")
    
    # Combine all
    if not all_features:
        print("[!] No datasets found!")
        return None
    
    combined_df = pd.concat(all_features, ignore_index=True)
    print(f"\n[✓] Total flows: {len(combined_df)}")
    print(f"[✓] Total features: {len(combined_df.columns) - 1}")  # -1 for label
    
    # Show distribution
    print("\n[*] Class Distribution:")
    print(combined_df['label'].value_counts())
    
    return combined_df


def prepare_data(df):
    """
    הכנת הנתונים לאימון
    """
    print("\n" + "=" * 60)
    print("Preparing Data")
    print("=" * 60)
    
    # Separate features and labels
    X = df.drop('label', axis=1)
    y = df['label']
    
    # Handle missing values
    X = X.fillna(0)
    
    # Handle infinite values
    X = X.replace([np.inf, -np.inf], 0)
    
    print(f"[*] Features shape: {X.shape}")
    print(f"[*] Labels shape: {y.shape}")
    
    # Split to train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    print(f"\n[*] Train set: {len(X_train)} samples")
    print(f"[*] Test set: {len(X_test)} samples")
    
    return X_train, X_test, y_train, y_test


def train_and_evaluate(X_train, X_test, y_train, y_test, model_type='decision_tree'):
    """
    אימון והערכת המודל
    """
    print("\n" + "=" * 60)
    print("Training Hybrid Classifier")
    print("=" * 60)
    
    # Create and train classifier
    classifier = HybridTrafficClassifier()
    classifier.train_ml_model(X_train, y_train, model_type=model_type)
    
    # Evaluate
    results = classifier.evaluate(X_test, y_test)
    
    return classifier, results


def plot_results(results, output_dir='.'):
    """
    ויזואליזציה של תוצאות
    """
    print("\n" + "=" * 60)
    print("Generating Visualizations")
    print("=" * 60)
    
    # Confusion Matrix
    plt.figure(figsize=(10, 8))
    cm = results['confusion_matrix']
    classes = ['Streaming', 'Gaming', 'Video_Call', 'Web_Browsing', 'File_Transfer']
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=classes, yticklabels=classes)
    plt.title('Confusion Matrix', fontsize=16)
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()
    
    cm_file = os.path.join(output_dir, 'confusion_matrix.png')
    plt.savefig(cm_file, dpi=300, bbox_inches='tight')
    print(f"[✓] Confusion matrix saved to {cm_file}")
    plt.close()
    
    # Method distribution
    plt.figure(figsize=(8, 6))
    methods = list(results['methods_used'].keys())
    counts = list(results['methods_used'].values())
    colors = ['#00f5ff', '#0ff']
    
    plt.bar(methods, counts, color=colors)
    plt.title('Classification Method Distribution', fontsize=16)
    plt.ylabel('Number of Samples', fontsize=12)
    plt.xlabel('Method', fontsize=12)
    
    # Add percentages on bars
    total = sum(counts)
    for i, (method, count) in enumerate(zip(methods, counts)):
        percentage = count / total * 100
        plt.text(i, count + 5, f'{percentage:.1f}%', 
                ha='center', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    method_file = os.path.join(output_dir, 'method_distribution.png')
    plt.savefig(method_file, dpi=300, bbox_inches='tight')
    print(f"[✓] Method distribution saved to {method_file}")
    plt.close()
    
    # Accuracy by class
    from sklearn.metrics import classification_report
    report = classification_report(results['y_test'], results['y_pred'], 
                                   output_dict=True, zero_division=0)
    
    classes_to_plot = [c for c in classes if c in report]
    accuracies = [report[c]['f1-score'] for c in classes_to_plot]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(classes_to_plot, accuracies, color='#00f5ff')
    plt.title('F1-Score by Traffic Type', fontsize=16)
    plt.ylabel('F1-Score', fontsize=12)
    plt.xlabel('Traffic Type', fontsize=12)
    plt.ylim(0, 1.1)
    plt.xticks(rotation=45, ha='right')
    
    # Add values on bars
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{acc:.2f}', ha='center', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    f1_file = os.path.join(output_dir, 'f1_scores.png')
    plt.savefig(f1_file, dpi=300, bbox_inches='tight')
    print(f"[✓] F1 scores saved to {f1_file}")
    plt.close()


def generate_report(classifier, results, output_file='model_report.txt'):
    """
    יצירת דוח מפורט
    """
    print("\n" + "=" * 60)
    print("Generating Model Report")
    print("=" * 60)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("NetInsight Traffic Classifier - Model Report\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("## Model Architecture\n")
        f.write("-" * 80 + "\n")
        f.write("Hybrid Classification System:\n")
        f.write("  1. Layer 1: Rule-Based Classification\n")
        f.write("     - Fast decision based on port numbers and packet characteristics\n")
        f.write("     - Handles clear-cut cases with 100% confidence\n")
        f.write("  2. Layer 2: Machine Learning Classification\n")
        f.write("     - Decision Tree / Random Forest\n")
        f.write("     - Handles complex and ambiguous cases\n\n")
        
        f.write("## Performance Metrics\n")
        f.write("-" * 80 + "\n")
        f.write(f"Overall Accuracy: {results['accuracy']:.2%}\n\n")
        
        f.write("Classification Method Distribution:\n")
        total = sum(results['methods_used'].values())
        for method, count in results['methods_used'].items():
            percentage = count / total * 100
            f.write(f"  - {method}: {count} samples ({percentage:.1f}%)\n")
        
        f.write("\n## Per-Class Performance\n")
        f.write("-" * 80 + "\n")
        from sklearn.metrics import classification_report
        report = classification_report(results['y_test'], results['y_pred'], zero_division=0)
        f.write(report)
        
        f.write("\n## Feature Importance (Top 15)\n")
        f.write("-" * 80 + "\n")
        if hasattr(classifier.ml_model, 'feature_importances_'):
            importances = classifier.ml_model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            for i in range(min(15, len(indices))):
                idx = indices[i]
                feature_name = classifier.feature_names[idx]
                importance = importances[idx]
                f.write(f"{i+1:2d}. {feature_name:30s}: {importance:.4f}\n")
        
        f.write("\n## Confusion Matrix\n")
        f.write("-" * 80 + "\n")
        cm = results['confusion_matrix']
        classes = ['Streaming', 'Gaming', 'Video_Call', 'Web_Browsing', 'File_Transfer']
        
        # Header
        f.write(f"{'':15s}")
        for c in classes:
            f.write(f"{c:15s}")
        f.write("\n")
        
        # Rows
        for i, true_class in enumerate(classes):
            f.write(f"{true_class:15s}")
            for j, pred_class in enumerate(classes):
                f.write(f"{cm[i][j]:15d}")
            f.write("\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("End of Report\n")
        f.write("=" * 80 + "\n")
    
    print(f"[✓] Report saved to {output_file}")


def main():
    """
    פונקציה ראשית - תהליך האימון המלא
    """
    print("\n")
    print("█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + " " * 15 + "NetInsight Model Training" + " " * 18 + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)
    print("\n")
    
    # Step 1: Load datasets
    df = load_all_datasets()
    if df is None:
        print("\n[!] No data to train on. Run generate_datasets.py first!")
        return
    
    # Save combined features
    df.to_csv('combined_features.csv', index=False)
    print(f"\n[✓] Combined features saved to combined_features.csv")
    
    # Step 2: Prepare data
    X_train, X_test, y_train, y_test = prepare_data(df)
    
    # Step 3: Train and evaluate
    classifier, results = train_and_evaluate(X_train, X_test, y_train, y_test)
    
    # Step 4: Save model
    classifier.save_model('traffic_classifier.pkl')
    
    # Step 5: Generate visualizations
    plot_results(results)
    
    # Step 6: Generate report
    generate_report(classifier, results)
    
    # Summary
    print("\n" + "=" * 60)
    print("Training Complete! 🎉")
    print("=" * 60)
    print(f"✓ Model accuracy: {results['accuracy']:.2%}")
    print(f"✓ Model saved to: traffic_classifier.pkl")
    print(f"✓ Report saved to: model_report.txt")
    print(f"✓ Visualizations saved: confusion_matrix.png, method_distribution.png, f1_scores.png")
    print("\n[*] Next step: Run the UI with gradio_app.py or flask_app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
