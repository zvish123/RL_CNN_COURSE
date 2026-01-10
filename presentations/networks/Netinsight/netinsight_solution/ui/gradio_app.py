#!/usr/bin/env python3
"""
NetInsight - Gradio UI
ממשק משתמש אינטראקטיבי לניתוח תעבורת רשת
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scapy.all import rdpcap, IP, TCP, UDP
import numpy as np
from datetime import datetime
import io

try:
    from models.feature_extractor import FeatureExtractor
    from models.classifier import HybridTrafficClassifier
except:
    # Fallback for different import paths
    import sys
    sys.path.insert(0, '../models')
    from feature_extractor import FeatureExtractor
    from classifier import HybridTrafficClassifier


class NetInsightUI:
    """
    ממשק משתמש ל-NetInsight
    """
    
    def __init__(self):
        self.classifier = None
        self.extractor = FeatureExtractor()
        self.load_model()
        
        # Color scheme
        self.colors = {
            'Streaming': '#FF6B6B',
            'Gaming': '#4ECDC4',
            'Video_Call': '#45B7D1',
            'Web_Browsing': '#FFA07A',
            'File_Transfer': '#98D8C8'
        }
    
    def load_model(self):
        """
        טעינת המודל המאומן
        """
        model_path = '../models/traffic_classifier.pkl'
        
        if os.path.exists(model_path):
            try:
                self.classifier = HybridTrafficClassifier()
                self.classifier.load_model(model_path)
                print("[✓] Model loaded successfully")
            except Exception as e:
                print(f"[!] Error loading model: {e}")
                self.classifier = None
        else:
            print("[!] Model not found. Train the model first.")
            self.classifier = None
    
    def analyze_pcap(self, pcap_file):
        """
        ניתוח קובץ PCAP והצגת תוצאות
        
        Returns:
            - Classification results (text)
            - Traffic distribution chart
            - Timeline chart
            - Statistics table
        """
        if pcap_file is None:
            return "Please upload a PCAP file", None, None, None
        
        if self.classifier is None:
            return "Model not loaded. Please train the model first.", None, None, None
        
        try:
            # Extract features
            print(f"[*] Analyzing {pcap_file.name}...")
            features_df = self.extractor.extract_from_pcap(pcap_file.name)
            
            if features_df is None or len(features_df) == 0:
                return "No flows found in PCAP file", None, None, None
            
            # Classify each flow
            results = []
            for idx in range(len(features_df)):
                flow_features = features_df.iloc[idx].to_dict()
                
                traffic_type, confidence, method = self.classifier.classify(flow_features)
                
                results.append({
                    'flow_id': idx + 1,
                    'traffic_type': traffic_type,
                    'confidence': confidence,
                    'method': method,
                    'packets': flow_features.get('packet_count', 0),
                    'bytes': flow_features.get('total_bytes', 0),
                    'duration': flow_features.get('flow_duration', 0)
                })
            
            results_df = pd.DataFrame(results)
            
            # Generate outputs
            summary_text = self._generate_summary(results_df)
            pie_chart = self._create_pie_chart(results_df)
            timeline_chart = self._create_timeline_chart(features_df, results_df)
            stats_table = self._create_stats_table(results_df)
            
            return summary_text, pie_chart, timeline_chart, stats_table
            
        except Exception as e:
            return f"Error analyzing PCAP: {str(e)}", None, None, None
    
    def _generate_summary(self, results_df):
        """
        יצירת סיכום טקסטואלי
        """
        total_flows = len(results_df)
        traffic_counts = results_df['traffic_type'].value_counts()
        
        summary = f"# 📊 Analysis Results\n\n"
        summary += f"**Total Flows Detected:** {total_flows}\n\n"
        
        summary += "## Traffic Type Distribution:\n"
        for traffic_type, count in traffic_counts.items():
            percentage = (count / total_flows) * 100
            emoji = self._get_emoji(traffic_type)
            summary += f"- {emoji} **{traffic_type}**: {count} flows ({percentage:.1f}%)\n"
        
        summary += f"\n## Classification Methods:\n"
        method_counts = results_df['method'].value_counts()
        for method, count in method_counts.items():
            percentage = (count / total_flows) * 100
            summary += f"- **{method}**: {count} flows ({percentage:.1f}%)\n"
        
        summary += f"\n## Average Confidence: {results_df['confidence'].mean():.2%}\n"
        
        return summary
    
    def _get_emoji(self, traffic_type):
        """
        בחירת אימוג'י לסוג תעבורה
        """
        emojis = {
            'Streaming': '📹',
            'Gaming': '🎮',
            'Video_Call': '📞',
            'Web_Browsing': '🌐',
            'File_Transfer': '📁'
        }
        return emojis.get(traffic_type, '📊')
    
    def _create_pie_chart(self, results_df):
        """
        יצירת pie chart של התפלגות תעבורה
        """
        traffic_counts = results_df['traffic_type'].value_counts()
        
        colors = [self.colors.get(t, '#CCCCCC') for t in traffic_counts.index]
        
        fig = go.Figure(data=[go.Pie(
            labels=traffic_counts.index,
            values=traffic_counts.values,
            hole=0.4,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textfont=dict(size=14)
        )])
        
        fig.update_layout(
            title="Traffic Distribution",
            title_font=dict(size=20),
            height=500,
            showlegend=True
        )
        
        return fig
    
    def _create_timeline_chart(self, features_df, results_df):
        """
        יצירת timeline של פעילות רשת
        """
        # Combine features and results
        combined = features_df.copy()
        combined['traffic_type'] = results_df['traffic_type'].values
        
        # Sort by packet count for better visualization
        combined = combined.sort_values('packet_count', ascending=False).head(20)
        
        fig = go.Figure()
        
        for traffic_type in combined['traffic_type'].unique():
            df_type = combined[combined['traffic_type'] == traffic_type]
            
            fig.add_trace(go.Bar(
                name=traffic_type,
                x=list(range(len(df_type))),
                y=df_type['packet_count'],
                marker_color=self.colors.get(traffic_type, '#CCCCCC')
            ))
        
        fig.update_layout(
            title="Top 20 Flows by Packet Count",
            xaxis_title="Flow Index",
            yaxis_title="Packet Count",
            height=400,
            barmode='group',
            showlegend=True
        )
        
        return fig
    
    def _create_stats_table(self, results_df):
        """
        יצירת טבלת סטטיסטיקות
        """
        stats = []
        
        for traffic_type in results_df['traffic_type'].unique():
            df_type = results_df[results_df['traffic_type'] == traffic_type]
            
            stats.append({
                'Traffic Type': traffic_type,
                'Flows': len(df_type),
                'Total Packets': int(df_type['packets'].sum()),
                'Total Bytes': f"{df_type['bytes'].sum() / 1024 / 1024:.2f} MB",
                'Avg Confidence': f"{df_type['confidence'].mean():.2%}"
            })
        
        stats_df = pd.DataFrame(stats)
        return stats_df
    
    def create_demo_interface(self):
        """
        יצירת ממשק Gradio
        """
        
        with gr.Blocks(title="NetInsight - Network Traffic Analyzer", theme=gr.themes.Soft()) as demo:
            
            # Header
            gr.Markdown("""
            # 🔍 NetInsight - Network Traffic Analyzer
            ### Real-time Network Traffic Classification System
            
            Upload a PCAP file to analyze and classify network traffic using our hybrid AI system.
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    # Input section
                    gr.Markdown("## 📤 Upload PCAP File")
                    pcap_input = gr.File(
                        label="Select PCAP file",
                        file_types=[".pcap", ".pcapng"]
                    )
                    
                    analyze_btn = gr.Button(
                        "🚀 Analyze Traffic",
                        variant="primary",
                        size="lg"
                    )
                    
                    gr.Markdown("""
                    ---
                    ### Supported Traffic Types:
                    - 📹 **Video Streaming** (YouTube, Netflix)
                    - 🎮 **Gaming** (Fortnite, Valorant)
                    - 📞 **Video Calls** (Zoom, Teams)
                    - 🌐 **Web Browsing** (HTTP/HTTPS)
                    - 📁 **File Transfer** (FTP, Cloud)
                    """)
                
                with gr.Column(scale=2):
                    # Results section
                    gr.Markdown("## 📊 Analysis Results")
                    
                    summary_output = gr.Markdown(
                        value="Upload a PCAP file to see results..."
                    )
            
            # Charts section
            with gr.Row():
                with gr.Column():
                    pie_output = gr.Plot(label="Traffic Distribution")
                
                with gr.Column():
                    timeline_output = gr.Plot(label="Flow Activity Timeline")
            
            # Statistics table
            gr.Markdown("## 📈 Detailed Statistics")
            stats_output = gr.Dataframe(
                label="Statistics by Traffic Type",
                wrap=True
            )
            
            # Footer
            gr.Markdown("""
            ---
            ### 🎯 How It Works:
            1. **Layer 1: Rule-Based** - Quick classification using port numbers and packet characteristics
            2. **Layer 2: ML-Based** - Advanced Decision Tree for complex patterns
            3. **Hybrid Approach** - Combines both methods for optimal accuracy (~85-90%)
            
            ### 🛠️ Technologies:
            `Scapy` • `scikit-learn` • `Gradio` • `Plotly` • `pandas`
            
            ---
            **NetInsight** | Blich High School Cyber Track | 2025
            """)
            
            # Connect the button to the analysis function
            analyze_btn.click(
                fn=self.analyze_pcap,
                inputs=[pcap_input],
                outputs=[summary_output, pie_output, timeline_output, stats_output]
            )
        
        return demo


def main():
    """
    הרצת הממשק
    """
    print("=" * 60)
    print("NetInsight - Gradio UI")
    print("=" * 60)
    
    # Create UI instance
    ui = NetInsightUI()
    
    if ui.classifier is None:
        print("\n[!] Warning: Model not loaded!")
        print("[!] Please train the model first:")
        print("    cd models && python3 train_model.py")
        print("\n[*] Starting UI anyway (for demonstration)...\n")
    else:
        print("\n[✓] Model loaded successfully")
        print("[✓] UI is ready!\n")
    
    # Create and launch interface
    demo = ui.create_demo_interface()
    
    print("[*] Launching Gradio interface...")
    print("[*] Open your browser at: http://localhost:7860")
    print("=" * 60)
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Set to True to create public link
        show_error=True
    )


if __name__ == "__main__":
    main()
