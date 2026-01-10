#!/usr/bin/env python3
"""
NetInsight - Feature Extractor
חילוץ features מקבצי PCAP לצורך סיווג תעבורה
"""

from scapy.all import *
import numpy as np
import pandas as pd
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')


class FeatureExtractor:
    """
    מחלקה לחילוץ features סטטיסטיים מתעבורת רשת
    """
    
    def __init__(self):
        self.features = []
    
    def extract_from_pcap(self, pcap_file, max_packets=None):
        """
        חילוץ features מקובץ PCAP
        
        Args:
            pcap_file: נתיב לקובץ PCAP
            max_packets: מספר מקסימלי של packets לעיבוד (None = הכל)
        
        Returns:
            DataFrame עם features
        """
        print(f"[*] קורא {pcap_file}...")
        
        try:
            packets = rdpcap(pcap_file)
            if max_packets:
                packets = packets[:max_packets]
        except Exception as e:
            print(f"[!] שגיאה בקריאת הקובץ: {e}")
            return None
        
        print(f"[*] עיבוד {len(packets)} packets...")
        
        # Group packets by flows
        flows = self._group_packets_to_flows(packets)
        
        print(f"[*] זוהו {len(flows)} flows")
        
        # Extract features for each flow
        features_list = []
        for flow_id, flow_packets in flows.items():
            features = self._extract_flow_features(flow_id, flow_packets)
            features_list.append(features)
        
        df = pd.DataFrame(features_list)
        return df
    
    def _group_packets_to_flows(self, packets):
        """
        קיבוץ packets ל-flows (connections)
        Flow = צמד של IP:Port ייחודי
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
            
            # Create bidirectional flow ID (normalized)
            flow_id = self._create_flow_id(src_ip, dst_ip, src_port, dst_port, protocol)
            flows[flow_id].append(pkt)
        
        return flows
    
    def _create_flow_id(self, src_ip, dst_ip, src_port, dst_port, protocol):
        """
        יצירת flow ID בידירקציונלי (מנורמל)
        """
        # Sort to make it bidirectional
        if (src_ip, src_port) < (dst_ip, dst_port):
            return f"{src_ip}:{src_port}<->{dst_ip}:{dst_port}:{protocol}"
        else:
            return f"{dst_ip}:{dst_port}<->{src_ip}:{src_port}:{protocol}"
    
    def _extract_flow_features(self, flow_id, packets):
        """
        חילוץ features מ-flow בודד
        
        Features שנחלץ:
        1. Packet size statistics (min, max, mean, std)
        2. Inter-arrival times (IAT) statistics
        3. Protocol and port information
        4. Flow duration
        5. Packet rate
        6. Bidirectional statistics (upload/download ratio)
        7. Burst patterns
        """
        features = {}
        
        # Parse flow ID
        parts = flow_id.split(':')
        protocol = parts[-1]
        features['protocol'] = protocol
        
        # Extract ports
        try:
            port1 = int(parts[1].split('<')[0])
            port2 = int(parts[3].split('<')[0])
            features['port1'] = port1
            features['port2'] = port2
            features['min_port'] = min(port1, port2)
            features['max_port'] = max(port1, port2)
        except:
            features['port1'] = 0
            features['port2'] = 0
            features['min_port'] = 0
            features['max_port'] = 0
        
        # Packet count
        features['packet_count'] = len(packets)
        
        # Packet sizes
        sizes = [len(pkt) for pkt in packets]
        features['total_bytes'] = sum(sizes)
        features['min_packet_size'] = min(sizes) if sizes else 0
        features['max_packet_size'] = max(sizes) if sizes else 0
        features['mean_packet_size'] = np.mean(sizes) if sizes else 0
        features['std_packet_size'] = np.std(sizes) if len(sizes) > 1 else 0
        features['median_packet_size'] = np.median(sizes) if sizes else 0
        
        # Packet size categories
        small_packets = sum(1 for s in sizes if s < 200)
        medium_packets = sum(1 for s in sizes if 200 <= s < 800)
        large_packets = sum(1 for s in sizes if s >= 800)
        
        features['small_packets_ratio'] = small_packets / len(sizes) if sizes else 0
        features['medium_packets_ratio'] = medium_packets / len(sizes) if sizes else 0
        features['large_packets_ratio'] = large_packets / len(sizes) if sizes else 0
        
        # Time-based features
        if len(packets) > 1:
            timestamps = [float(pkt.time) for pkt in packets]
            
            # Flow duration
            features['flow_duration'] = timestamps[-1] - timestamps[0]
            
            # Inter-arrival times (IAT)
            iats = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
            
            features['mean_iat'] = np.mean(iats) if iats else 0
            features['std_iat'] = np.std(iats) if len(iats) > 1 else 0
            features['min_iat'] = min(iats) if iats else 0
            features['max_iat'] = max(iats) if iats else 0
            
            # Packet rate (packets per second)
            features['packet_rate'] = len(packets) / features['flow_duration'] if features['flow_duration'] > 0 else 0
            
            # Bandwidth (bytes per second)
            features['bandwidth'] = features['total_bytes'] / features['flow_duration'] if features['flow_duration'] > 0 else 0
            
            # IAT regularity (coefficient of variation)
            # קבוע = Gaming, משתנה = Streaming/Browsing
            features['iat_cv'] = (features['std_iat'] / features['mean_iat']) if features['mean_iat'] > 0 else 0
            
        else:
            features['flow_duration'] = 0
            features['mean_iat'] = 0
            features['std_iat'] = 0
            features['min_iat'] = 0
            features['max_iat'] = 0
            features['packet_rate'] = 0
            features['bandwidth'] = 0
            features['iat_cv'] = 0
        
        # Bidirectional analysis
        src_ip = packets[0][IP].src if IP in packets[0] else None
        
        upload_bytes = 0
        download_bytes = 0
        upload_packets = 0
        download_packets = 0
        
        for pkt in packets:
            if IP in pkt:
                if pkt[IP].src == src_ip:
                    upload_bytes += len(pkt)
                    upload_packets += 1
                else:
                    download_bytes += len(pkt)
                    download_packets += 1
        
        total = upload_bytes + download_bytes
        features['upload_ratio'] = upload_bytes / total if total > 0 else 0
        features['download_ratio'] = download_bytes / total if total > 0 else 0
        features['upload_packet_ratio'] = upload_packets / len(packets) if len(packets) > 0 else 0
        features['download_packet_ratio'] = download_packets / len(packets) if len(packets) > 0 else 0
        
        # Symmetry measure (0 = asymmetric, 0.5 = symmetric)
        features['symmetry'] = 1 - abs(features['upload_ratio'] - features['download_ratio'])
        
        # Burst detection
        # Burst = קבוצת packets צפופה בזמן
        if len(packets) > 10:
            burst_threshold = 0.1  # 100ms
            burst_count = 0
            current_burst_size = 1
            max_burst_size = 1
            
            for i in range(1, len(packets)):
                time_diff = float(packets[i].time) - float(packets[i-1].time)
                if time_diff < burst_threshold:
                    current_burst_size += 1
                    max_burst_size = max(max_burst_size, current_burst_size)
                else:
                    if current_burst_size > 5:
                        burst_count += 1
                    current_burst_size = 1
            
            features['burst_count'] = burst_count
            features['max_burst_size'] = max_burst_size
        else:
            features['burst_count'] = 0
            features['max_burst_size'] = 0
        
        return features
    
    def extract_features_summary(self, features_df):
        """
        הצגת סיכום features שנחלצו
        """
        print("\n" + "=" * 60)
        print("Feature Extraction Summary")
        print("=" * 60)
        print(f"Total flows: {len(features_df)}")
        print(f"Total features: {len(features_df.columns)}")
        print("\nFeature list:")
        for i, col in enumerate(features_df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        print("\nSample statistics:")
        print(features_df.describe().round(2))


def main():
    """
    דוגמה לשימוש
    """
    extractor = FeatureExtractor()
    
    # Example: Extract features from a PCAP file
    pcap_file = "streaming.pcap"
    
    if os.path.exists(pcap_file):
        df = extractor.extract_from_pcap(pcap_file)
        
        if df is not None:
            print(f"\n[✓] נחלצו features מ-{len(df)} flows")
            extractor.extract_features_summary(df)
            
            # Save to CSV
            output_file = pcap_file.replace('.pcap', '_features.csv')
            df.to_csv(output_file, index=False)
            print(f"\n[✓] נשמר ב-{output_file}")
    else:
        print(f"[!] קובץ {pcap_file} לא נמצא")
        print("[!] הרץ קודם: python3 generate_datasets.py")


if __name__ == "__main__":
    main()
