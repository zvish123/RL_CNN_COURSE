import socket
import threading
import random
import time


def caesar_cipher(text, shift):
    """הצפנת/פענוח קיסר"""
    result = ""
    for char in text:
        if char.isalpha():
            # שמירה על אותיות גדולות/קטנות
            start = ord('A') if char.isupper() else ord('a')
            # הזזה במעגל (modulo 26)
            shifted = chr((ord(char) - start + shift) % 26 + start)
            result += shifted
        elif char.isdigit():
            # הזזה גם למספרים (0-9)
            shifted = chr((ord(char) - ord('0') + shift) % 10 + ord('0'))
            result += shifted
        else:
            # שאר התווים נשארים ללא שינוי
            result += char
    return result


# הדגל המקורי
ORIGINAL_FLAG_PART2 = "sc4nn3r_m4st3r}"

# הצפנה עם הזזה של 5 (כדי לקבל את המוצפן)
ENCRYPTED_FLAG_PART2 = caesar_cipher(ORIGINAL_FLAG_PART2, 5)

print(f"Debug - Original: {ORIGINAL_FLAG_PART2}")
print(f"Debug - Encrypted with +5: {ENCRYPTED_FLAG_PART2}")
print(f"Debug - To decrypt, use shift of -5")

# תגובות לפורטים שונים
PORT_RESPONSES = {
    8001: "HTTP/1.1 404 Not Found - Nothing here",
    8005: "SSH-2.0-OpenSSH_8.2 - Access Denied",
    8010: "MySQL Server 8.0 - Authentication Required",
    8015: "Redis 6.0 - NOAUTH Authentication required",
    8020: "MongoDB 4.4 - Connection refused",
    8025: "PostgreSQL 13.0 - Password authentication failed",
    8030: "Nginx 1.18 - 403 Forbidden",
    8035: "Apache 2.4 - Server Status: Running",
    8040: "FTP Server - Login Required",
    8042: "🔐 SECRET_PART_1: FLAG{h1dd3n_p0rt_",  # חלק ראשון של הדגל
    8045: "Elasticsearch 7.10 - Cluster Status: Green",
    8050: "Jenkins 2.289 - Build Server Active",
    8055: "Docker Registry - Authentication Required",
    8060: "Prometheus 2.30 - Metrics Server",
    8065: "Grafana 8.0 - Login Page",
    8070: "RabbitMQ 3.9 - Management Console",
    8073: "💡 HINT: The encrypted data uses Caesar Cipher. Try ROT with negative shift...",  # רמז!
    8075: "Memcached 1.6 - Stats Available",
    8077: f"🔐 SECRET_PART_2_ENCRYPTED: {ENCRYPTED_FLAG_PART2}",  # חלק שני מוצפן!
    8080: "Tomcat 9.0 - Web Application Server",
    8085: "Nexus Repository - Artifact Storage",
    8090: "GitLab 14.0 - Source Control",
    8095: "SonarQube 9.0 - Code Quality Analysis",
    8100: "Consul 1.10 - Service Discovery"
}


class PortServer:
    def __init__(self, port, response):
        self.port = port
        self.response = response
        self.running = False

    def handle_client(self, client_socket, address):
        try:
            # קבלת בקשה מהלקוח
            request = client_socket.recv(1024).decode('utf-8', errors='ignore')

            # שליחת תגובה
            client_socket.send(self.response.encode('utf-8'))

            # סימולציה של זמן עיבוד
            time.sleep(0.1)

        except Exception as e:
            pass
        finally:
            client_socket.close()

    def start(self):
        self.running = True
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_socket.bind(('127.0.0.1', self.port))
            server_socket.listen(5)
            server_socket.settimeout(1.0)

            print(f"✅ Server listening on port {self.port}")

            while self.running:
                try:
                    client_socket, address = server_socket.accept()
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"❌ Error on port {self.port}: {e}")
                    break

        except Exception as e:
            print(f"❌ Failed to start server on port {self.port}: {e}")
        finally:
            server_socket.close()


def main():
    print("=" * 70)
    print("🚀 PORT SCANNER CHALLENGE SERVER - CAESAR CIPHER EDITION")
    print("=" * 70)
    print("\n📡 Starting multiple port servers...")
    print(f"🎯 Total ports to scan: {len(PORT_RESPONSES)}")
    print(f"🔐 Hidden flag parts on ports: 8042 (clear) and 8077 (encrypted)")
    print(f"💡 Decryption hint on port: 8073")
    print(f"\n🔑 Cipher info: Caesar Cipher with shift of -5 to decrypt")
    print(f"📝 Encrypted part 2: {ENCRYPTED_FLAG_PART2}")
    print(f"📝 Decrypted part 2: {ORIGINAL_FLAG_PART2}")
    print(f"🏁 Complete flag: FLAG{{h1dd3n_p0rt_{ORIGINAL_FLAG_PART2}")
    print("\n⚠️  Press Ctrl+C to stop all servers\n")

    servers = []
    threads = []

    # יצירה והפעלה של שרתים לכל פורט
    for port, response in PORT_RESPONSES.items():
        server = PortServer(port, response)
        servers.append(server)

        thread = threading.Thread(target=server.start)
        thread.daemon = True
        thread.start()
        threads.append(thread)

        time.sleep(0.05)

    print("\n" + "=" * 70)
    print("✅ All servers are running!")
    print("=" * 70)
    print("\n💡 Now run your port scanner to find the hidden flag parts!")
    print("🔍 Scan range: 8000-8100")
    print("\n📝 Instructions:")
    print("   1. Run your Python scanner script")
    print("   2. Find port 8042 - contains clear part 1")
    print("   3. Find port 8077 - contains encrypted part 2")
    print("   4. Find port 8073 - contains decryption hint")
    print("   5. Decrypt part 2 using Caesar Cipher (shift -5)")
    print("   6. Combine both parts and submit the complete flag")
    print("\n" + "=" * 70)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down all servers...")
        for server in servers:
            server.running = False
        print("✅ All servers stopped. Goodbye!")


if __name__ == "__main__":
    main()