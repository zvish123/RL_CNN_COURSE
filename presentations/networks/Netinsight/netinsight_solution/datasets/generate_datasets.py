#!/usr/bin/env python3
"""
NetInsight - Dataset Generator
שלב 2: יצירת קבצי PCAP סימולטיביים לסוגי תעבורה שונים

משתמש ב-Scapy ליצירת תעבורת רשת מציאותית.
"""

from scapy.all import *
import random
import time
import pandas as pd
from datetime import datetime
import os

class TrafficGenerator:
    """
    מחלקה ליצירת סוגי תעבורה שונים
    """
    
    def __init__(self, src_ip="192.168.1.100", dst_ip="8.8.8.8"):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.packets = []
        
    def generate_streaming_traffic(self, duration=60, output_file="streaming.pcap"):
        """
        יצירת תעבורת Video Streaming (YouTube/Netflix style)
        
        מאפיינים:
        - Packets גדולים (1000-1500 bytes)
        - תדירות קבועה (~30 fps)
        - בעיקר download (asymmetric)
        - HTTP/HTTPS over TCP
        """
        print("[*] יוצר תעבורת Video Streaming...")
        packets = []
        
        # Simulate streaming session
        src_port = random.randint(50000, 60000)
        dst_port = 443  # HTTPS
        
        start_time = time.time()
        packet_count = 0
        
        # Phase 1: Initial burst (buffering)
        print("  [Phase 1] Initial buffering...")
        for i in range(50):
            # Large data packets (simulating video segments)
            payload_size = random.randint(1200, 1460)
            payload = Raw(load='X' * payload_size)
            
            pkt = IP(src=self.dst_ip, dst=self.src_ip) / \
                  TCP(sport=dst_port, dport=src_port, flags='PA') / \
                  payload
            
            packets.append(pkt)
            packet_count += 1
        
        # Phase 2: Steady streaming
        print("  [Phase 2] Steady streaming...")
        frames_per_second = 30
        bytes_per_frame = random.randint(40000, 80000)  # 40-80KB per frame
        
        elapsed = 0
        while elapsed < duration:
            # Simulate video frame as multiple packets
            packets_per_frame = bytes_per_frame // 1460
            
            for _ in range(packets_per_frame):
                payload_size = random.randint(1400, 1460)
                payload = Raw(load='V' * payload_size)
                
                pkt = IP(src=self.dst_ip, dst=self.src_ip) / \
                      TCP(sport=dst_port, dport=src_port, flags='PA') / \
                      payload
                
                packets.append(pkt)
                packet_count += 1
            
            # Small ACK packets (upload)
            ack_pkt = IP(src=self.src_ip, dst=self.dst_ip) / \
                      TCP(sport=src_port, dport=dst_port, flags='A')
            packets.append(ack_pkt)
            
            # Wait for next frame
            time.sleep(1.0 / frames_per_second)
            elapsed = time.time() - start_time
        
        # Save to PCAP
        wrpcap(output_file, packets)
        print(f"  [✓] נוצרו {len(packets)} packets ונשמרו ב-{output_file}")
        
        return packets
    
    def generate_gaming_traffic(self, duration=60, output_file="gaming.pcap"):
        """
        יצירת תעבורת Gaming (Fortnite/Valorant style)
        
        מאפיינים:
        - Packets קטנים (50-200 bytes)
        - תדירות גבוהה וקבועה (60 Hz)
        - Symmetric (bidirectional)
        - UDP
        """
        print("[*] יוצר תעבורת Gaming...")
        packets = []
        
        # Game server simulation
        src_port = random.randint(50000, 60000)
        dst_port = random.randint(27000, 27100)  # Typical game ports
        
        tick_rate = 64  # Updates per second
        tick_interval = 1.0 / tick_rate
        
        start_time = time.time()
        packet_count = 0
        
        print(f"  [Tick Rate: {tick_rate} Hz]")
        
        elapsed = 0
        while elapsed < duration:
            # Client -> Server (player actions)
            client_payload_size = random.randint(50, 150)
            client_payload = Raw(load='C' * client_payload_size)
            
            client_pkt = IP(src=self.src_ip, dst=self.dst_ip) / \
                        UDP(sport=src_port, dport=dst_port) / \
                        client_payload
            
            packets.append(client_pkt)
            packet_count += 1
            
            # Server -> Client (world state updates)
            server_payload_size = random.randint(80, 200)
            server_payload = Raw(load='S' * server_payload_size)
            
            server_pkt = IP(src=self.dst_ip, dst=self.src_ip) / \
                        UDP(sport=dst_port, dport=src_port) / \
                        server_payload
            
            packets.append(server_pkt)
            packet_count += 1
            
            time.sleep(tick_interval)
            elapsed = time.time() - start_time
        
        # Save to PCAP
        wrpcap(output_file, packets)
        print(f"  [✓] נוצרו {len(packets)} packets ונשמרו ב-{output_file}")
        
        return packets
    
    def generate_video_call_traffic(self, duration=60, output_file="video_call.pcap"):
        """
        יצירת תעבורת Video Calls (Zoom/Teams style)
        
        מאפיינים:
        - Packets בינוניים (300-800 bytes)
        - תדירות משתנה (adaptive)
        - Symmetric
        - UDP/RTP
        """
        print("[*] יוצר תעבורת Video Call...")
        packets = []
        
        # WebRTC ports
        src_port = random.randint(50000, 60000)
        dst_port = random.randint(3478, 3497)
        
        # Separate streams for audio and video
        audio_rate = 50  # packets per second
        video_rate = 30  # fps
        
        start_time = time.time()
        packet_count = 0
        
        print("  [Streams: Audio + Video]")
        
        elapsed = 0
        frame_counter = 0
        
        while elapsed < duration:
            # Audio stream (more frequent, smaller packets)
            if frame_counter % 2 == 0:  # Every other iteration
                # Upload audio
                audio_size = random.randint(60, 120)
                audio_payload = Raw(load='A' * audio_size)
                
                audio_up = IP(src=self.src_ip, dst=self.dst_ip) / \
                          UDP(sport=src_port, dport=dst_port) / \
                          audio_payload
                packets.append(audio_up)
                
                # Download audio
                audio_down = IP(src=self.dst_ip, dst=self.src_ip) / \
                            UDP(sport=dst_port, dport=src_port) / \
                            audio_payload
                packets.append(audio_down)
                packet_count += 2
            
            # Video stream (less frequent, larger packets)
            # Adaptive quality - varies packet size
            quality_factor = random.uniform(0.7, 1.0)
            video_size = int(random.randint(400, 1200) * quality_factor)
            video_payload = Raw(load='V' * video_size)
            
            # Upload video
            video_up = IP(src=self.src_ip, dst=self.dst_ip) / \
                      UDP(sport=src_port, dport=dst_port) / \
                      video_payload
            packets.append(video_up)
            
            # Download video
            video_down = IP(src=self.dst_ip, dst=self.src_ip) / \
                        UDP(sport=dst_port, dport=src_port) / \
                        video_payload
            packets.append(video_down)
            packet_count += 2
            
            frame_counter += 1
            time.sleep(1.0 / video_rate)
            elapsed = time.time() - start_time
        
        # Save to PCAP
        wrpcap(output_file, packets)
        print(f"  [✓] נוצרו {len(packets)} packets ונשמרו ב-{output_file}")
        
        return packets
    
    def generate_web_browsing(self, duration=30, output_file="web_browsing.pcap"):
        """
        יצירת תעבורת Web Browsing
        
        מאפיינים:
        - Bursts של requests
        - תגובות גדולות (HTML, CSS, JS, images)
        - TCP/HTTP(S)
        """
        print("[*] יוצר תעבורת Web Browsing...")
        packets = []
        
        # Simulate multiple page loads
        num_pages = 5
        
        for page in range(num_pages):
            print(f"  [Page {page + 1}/{num_pages}] Loading...")
            
            src_port = random.randint(50000, 60000)
            dst_port = 443  # HTTPS
            
            # Initial request (small)
            request = IP(src=self.src_ip, dst=self.dst_ip) / \
                     TCP(sport=src_port, dport=dst_port, flags='PA') / \
                     Raw(load='GET / HTTP/1.1\r\n' * 10)
            packets.append(request)
            
            # Response - HTML (medium)
            html_size = random.randint(5000, 20000)
            html_response = IP(src=self.dst_ip, dst=self.src_ip) / \
                          TCP(sport=dst_port, dport=src_port, flags='PA') / \
                          Raw(load='<html>' * (html_size // 6))
            packets.append(html_response)
            
            # Multiple resources (CSS, JS, images)
            num_resources = random.randint(10, 30)
            for res in range(num_resources):
                res_size = random.randint(1000, 50000)
                resource = IP(src=self.dst_ip, dst=self.src_ip) / \
                          TCP(sport=dst_port, dport=src_port, flags='PA') / \
                          Raw(load='R' * min(res_size, 1400))
                packets.append(resource)
                
                # Small ACKs
                if res % 5 == 0:
                    ack = IP(src=self.src_ip, dst=self.dst_ip) / \
                         TCP(sport=src_port, dport=dst_port, flags='A')
                    packets.append(ack)
            
            # Wait before next page
            time.sleep(random.uniform(3, 8))
        
        # Save to PCAP
        wrpcap(output_file, packets)
        print(f"  [✓] נוצרו {len(packets)} packets ונשמרו ב-{output_file}")
        
        return packets
    
    def generate_file_transfer(self, duration=30, output_file="file_transfer.pcap"):
        """
        יצירת תעבורת File Transfer (FTP/Cloud Sync style)
        
        מאפיינים:
        - Burst ארוך של packets גדולים
        - קצב גבוה
        - Mostly download
        """
        print("[*] יוצר תעבורת File Transfer...")
        packets = []
        
        src_port = random.randint(50000, 60000)
        dst_port = 21  # FTP data port
        
        # Simulate large file download
        file_size = 10 * 1024 * 1024  # 10 MB
        packet_size = 1460
        num_packets = file_size // packet_size
        
        print(f"  [Downloading 10MB file...]")
        
        for i in range(num_packets):
            payload = Raw(load='F' * packet_size)
            pkt = IP(src=self.dst_ip, dst=self.src_ip) / \
                  TCP(sport=dst_port, dport=src_port, flags='PA') / \
                  payload
            packets.append(pkt)
            
            # ACK every 10 packets
            if i % 10 == 0:
                ack = IP(src=self.src_ip, dst=self.dst_ip) / \
                     TCP(sport=src_port, dport=dst_port, flags='A')
                packets.append(ack)
            
            if i % 1000 == 0:
                print(f"    Progress: {i}/{num_packets} packets")
        
        # Save to PCAP
        wrpcap(output_file, packets)
        print(f"  [✓] נוצרו {len(packets)} packets ונשמרו ב-{output_file}")
        
        return packets


def extract_metadata_from_pcap(pcap_file, traffic_type):
    """
    חילוץ metadata מקובץ PCAP ליצירת CSV
    """
    print(f"[*] מחלץ metadata מ-{pcap_file}...")
    
    packets = rdpcap(pcap_file)
    
    flows = {}
    
    for pkt in packets:
        if IP in pkt:
            # Create flow identifier
            if TCP in pkt:
                protocol = "TCP"
                sport = pkt[TCP].sport
                dport = pkt[TCP].dport
            elif UDP in pkt:
                protocol = "UDP"
                sport = pkt[UDP].sport
                dport = pkt[UDP].dport
            else:
                continue
            
            flow_id = f"{pkt[IP].src}:{sport}->{pkt[IP].dst}:{dport}"
            
            if flow_id not in flows:
                flows[flow_id] = {
                    'src_ip': pkt[IP].src,
                    'dst_ip': pkt[IP].dst,
                    'src_port': sport,
                    'dst_port': dport,
                    'protocol': protocol,
                    'packet_count': 0,
                    'total_bytes': 0,
                    'packet_sizes': [],
                    'traffic_type': traffic_type
                }
            
            flows[flow_id]['packet_count'] += 1
            flows[flow_id]['total_bytes'] += len(pkt)
            flows[flow_id]['packet_sizes'].append(len(pkt))
    
    # Convert to DataFrame
    data = []
    for flow_id, flow_data in flows.items():
        sizes = flow_data['packet_sizes']
        data.append({
            'flow_id': flow_id,
            'src_ip': flow_data['src_ip'],
            'dst_ip': flow_data['dst_ip'],
            'src_port': flow_data['src_port'],
            'dst_port': flow_data['dst_port'],
            'protocol': flow_data['protocol'],
            'packet_count': flow_data['packet_count'],
            'total_bytes': flow_data['total_bytes'],
            'avg_packet_size': sum(sizes) / len(sizes) if sizes else 0,
            'min_packet_size': min(sizes) if sizes else 0,
            'max_packet_size': max(sizes) if sizes else 0,
            'traffic_type': flow_data['traffic_type']
        })
    
    df = pd.DataFrame(data)
    return df


def main():
    """
    פונקציה ראשית - יוצרת את כל ה-datasets
    """
    print("=" * 60)
    print("NetInsight Dataset Generator")
    print("=" * 60)
    print()
    
    generator = TrafficGenerator()
    
    # Create output directory
    os.makedirs("datasets", exist_ok=True)
    os.chdir("datasets")
    
    # Generate all traffic types
    datasets = []
    
    print("\n[1/5] Streaming Traffic")
    print("-" * 60)
    generator.generate_streaming_traffic(duration=60, output_file="streaming.pcap")
    datasets.append(("streaming.pcap", "Streaming"))
    
    print("\n[2/5] Gaming Traffic")
    print("-" * 60)
    generator.generate_gaming_traffic(duration=60, output_file="gaming.pcap")
    datasets.append(("gaming.pcap", "Gaming"))
    
    print("\n[3/5] Video Call Traffic")
    print("-" * 60)
    generator.generate_video_call_traffic(duration=60, output_file="video_call.pcap")
    datasets.append(("video_call.pcap", "Video_Call"))
    
    print("\n[4/5] Web Browsing Traffic")
    print("-" * 60)
    generator.generate_web_browsing(duration=30, output_file="web_browsing.pcap")
    datasets.append(("web_browsing.pcap", "Web_Browsing"))
    
    print("\n[5/5] File Transfer Traffic")
    print("-" * 60)
    generator.generate_file_transfer(duration=30, output_file="file_transfer.pcap")
    datasets.append(("file_transfer.pcap", "File_Transfer"))
    
    # Extract metadata to CSV
    print("\n" + "=" * 60)
    print("Extracting Metadata to CSV")
    print("=" * 60)
    
    all_flows = []
    for pcap_file, traffic_type in datasets:
        df = extract_metadata_from_pcap(pcap_file, traffic_type)
        all_flows.append(df)
    
    # Combine all flows
    combined_df = pd.concat(all_flows, ignore_index=True)
    combined_df.to_csv("metadata.csv", index=False)
    
    print(f"\n[✓] נוצר קובץ metadata.csv עם {len(combined_df)} flows")
    print(f"[✓] סך הכל {len(datasets)} קבצי PCAP")
    
    # Print summary statistics
    print("\n" + "=" * 60)
    print("Summary Statistics")
    print("=" * 60)
    print(combined_df.groupby('traffic_type').agg({
        'packet_count': 'sum',
        'total_bytes': 'sum',
        'avg_packet_size': 'mean'
    }).round(2))
    
    print("\n[✓] הושלם בהצלחה!")
    print("=" * 60)


if __name__ == "__main__":
    # Check if running with sudo (needed for raw sockets)
    if os.geteuid() != 0:
        print("[!] התוכנית דורשת הרשאות root")
        print("[!] הרץ עם: sudo python3 generate_datasets.py")
        exit(1)
    
    main()
