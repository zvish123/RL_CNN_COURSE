#!/usr/bin/env python3
"""
NetInsight - Flask UI
ממשק משתמש web-based עם Flask
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

import pandas as pd
import json
from werkzeug.utils import secure_filename

try:
    from models.feature_extractor import FeatureExtractor
    from models.classifier import HybridTrafficClassifier
except:
    sys.path.insert(0, '../models')
    from feature_extractor import FeatureExtractor
    from classifier import HybridTrafficClassifier

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variables
classifier = None
extractor = FeatureExtractor()


def load_model():
    """
    טעינת המודל
    """
    global classifier
    model_path = '../models/traffic_classifier.pkl'
    
    if os.path.exists(model_path):
        try:
            classifier = HybridTrafficClassifier()
            classifier.load_model(model_path)
            print("[✓] Model loaded successfully")
            return True
        except Exception as e:
            print(f"[!] Error loading model: {e}")
            return False
    else:
        print("[!] Model not found")
        return False


@app.route('/')
def index():
    """
    דף הבית
    """
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_pcap():
    """
    API endpoint לניתוח PCAP
    """
    global classifier, extractor
    
    if classifier is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    if 'pcap_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['pcap_file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract features
        features_df = extractor.extract_from_pcap(filepath)
        
        if features_df is None or len(features_df) == 0:
            return jsonify({'error': 'No flows found in PCAP'}), 400
        
        # Classify flows
        results = []
        traffic_distribution = {}
        
        for idx in range(len(features_df)):
            flow_features = features_df.iloc[idx].to_dict()
            traffic_type, confidence, method = classifier.classify(flow_features)
            
            results.append({
                'flow_id': idx + 1,
                'traffic_type': traffic_type,
                'confidence': float(confidence),
                'method': method,
                'packets': int(flow_features.get('packet_count', 0)),
                'bytes': int(flow_features.get('total_bytes', 0)),
                'duration': float(flow_features.get('flow_duration', 0))
            })
            
            # Update distribution
            traffic_distribution[traffic_type] = traffic_distribution.get(traffic_type, 0) + 1
        
        # Calculate statistics
        total_flows = len(results)
        total_packets = sum(r['packets'] for r in results)
        total_bytes = sum(r['bytes'] for r in results)
        
        response = {
            'success': True,
            'summary': {
                'total_flows': total_flows,
                'total_packets': total_packets,
                'total_bytes': total_bytes,
                'traffic_distribution': traffic_distribution
            },
            'flows': results[:50]  # Limit to first 50 flows for UI
        }
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status')
def status():
    """
    בדיקת סטטוס המערכת
    """
    return jsonify({
        'model_loaded': classifier is not None,
        'status': 'ready' if classifier else 'model not loaded'
    })


# HTML Template (embedded)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NetInsight - Network Traffic Analyzer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #fff;
            min-height: 100vh;
            padding: 2rem;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .header h1 {
            font-size: 3rem;
            background: linear-gradient(45deg, #00f5ff, #0ff);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        
        .upload-section {
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(0, 212, 255, 0.3);
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .file-input {
            display: none;
        }
        
        .upload-btn {
            background: linear-gradient(45deg, #00f5ff, #0ff);
            color: #0f0c29;
            padding: 1rem 3rem;
            font-size: 1.2rem;
            font-weight: 700;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .upload-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(0, 245, 255, 0.5);
        }
        
        .results-section {
            display: none;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(0, 212, 255, 0.3);
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: #00f5ff;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: #aaa;
        }
        
        .flows-table {
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(0, 212, 255, 0.3);
            border-radius: 10px;
            padding: 1.5rem;
            overflow-x: auto;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th, td {
            padding: 1rem;
            text-align: right;
            border-bottom: 1px solid rgba(0, 212, 255, 0.2);
        }
        
        th {
            background: rgba(0, 245, 255, 0.1);
            color: #00f5ff;
            font-weight: 700;
        }
        
        .loading {
            text-align: center;
            padding: 2rem;
            display: none;
        }
        
        .spinner {
            border: 4px solid rgba(255, 255, 255, 0.1);
            border-top: 4px solid #00f5ff;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 NetInsight</h1>
            <p>Network Traffic Analyzer</p>
        </div>
        
        <div class="upload-section">
            <h2>העלה קובץ PCAP לניתוח</h2>
            <p style="margin: 1rem 0;">בחר קובץ PCAP והמערכת תנתח אוטומטית את התעבורה</p>
            <input type="file" id="pcapFile" class="file-input" accept=".pcap,.pcapng">
            <button class="upload-btn" onclick="document.getElementById('pcapFile').click()">
                📤 בחר קובץ PCAP
            </button>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="margin-top: 1rem;">מנתח קובץ...</p>
        </div>
        
        <div class="results-section" id="results">
            <h2 style="margin-bottom: 1rem;">תוצאות ניתוח</h2>
            
            <div class="stats-grid" id="stats"></div>
            
            <div class="flows-table">
                <h3 style="margin-bottom: 1rem;">Flows מזוהים (50 ראשונים)</h3>
                <table id="flowsTable">
                    <thead>
                        <tr>
                            <th>Flow ID</th>
                            <th>סוג תעבורה</th>
                            <th>Confidence</th>
                            <th>שיטה</th>
                            <th>Packets</th>
                            <th>Bytes</th>
                        </tr>
                    </thead>
                    <tbody id="flowsBody"></tbody>
                </table>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('pcapFile').addEventListener('change', async function(e) {
            const file = e.target.files[0];
            if (!file) return;
            
            const formData = new FormData();
            formData.append('pcap_file', file);
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    displayResults(data);
                } else {
                    alert('שגיאה: ' + data.error);
                }
            } catch (error) {
                alert('שגיאה בניתוח הקובץ: ' + error);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });
        
        function displayResults(data) {
            const { summary, flows } = data;
            
            // Display stats
            const statsHtml = `
                <div class="stat-card">
                    <div class="stat-value">${summary.total_flows}</div>
                    <div class="stat-label">Total Flows</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${summary.total_packets.toLocaleString()}</div>
                    <div class="stat-label">Total Packets</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${(summary.total_bytes / 1024 / 1024).toFixed(2)} MB</div>
                    <div class="stat-label">Total Data</div>
                </div>
            `;
            document.getElementById('stats').innerHTML = statsHtml;
            
            // Display flows table
            const flowsHtml = flows.map(flow => `
                <tr>
                    <td>${flow.flow_id}</td>
                    <td>${flow.traffic_type}</td>
                    <td>${(flow.confidence * 100).toFixed(1)}%</td>
                    <td>${flow.method}</td>
                    <td>${flow.packets}</td>
                    <td>${flow.bytes.toLocaleString()}</td>
                </tr>
            `).join('');
            document.getElementById('flowsBody').innerHTML = flowsHtml;
            
            // Show results
            document.getElementById('results').style.display = 'block';
        }
    </script>
</body>
</html>
"""


# Create templates directory and save HTML
def create_template():
    """
    יצירת template HTML
    """
    os.makedirs('templates', exist_ok=True)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(HTML_TEMPLATE)


def main():
    """
    הרצת האפליקציה
    """
    print("=" * 60)
    print("NetInsight - Flask UI")
    print("=" * 60)
    
    # Load model
    if load_model():
        print("[✓] Model loaded successfully")
    else:
        print("[!] Warning: Model not loaded!")
        print("[!] Train the model first: cd models && python3 train_model.py")
    
    # Create HTML template
    create_template()
    print("[✓] HTML template created")
    
    print("\n[*] Starting Flask server...")
    print("[*] Open your browser at: http://localhost:5000")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )


if __name__ == "__main__":
    main()
