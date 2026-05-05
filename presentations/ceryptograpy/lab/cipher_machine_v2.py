"""
מכונת הצפנה v2 — צד המורה
הרץ: python cipher_machine_v2.py
"""

import random, json, http.server, urllib.parse, threading, os
from datetime import datetime

SECRET_DICTIONARY = [
    "apple","bridge","castle","dragon","eagle","falcon","garden",
    "hammer","island","jungle","kernel","lancer","marble","nature",
    "needle","object","oyster","puzzle","quartz","raven","ribbon",
    "saddle","tunnel","knight","lemon","mango","narrow","ocean",
    "orange","palace","panda","paper","parrot","patrol","pencil",
    "pepper","phantom","photo","pillar","pirate","pixel","planet",
    "plasma","player","pocket","pollen","portal","rabbit","rocket",
    "river","shadow","shield","signal","silver","simple","skeleton",
    "solar","spark","spider","spiral","spring","stable","stamp",
    "station","storm","stream","street","strong","table","tiger",
    "trumpet","valley","violin","voltage","vulture","walnut","warrior",
    "winter","wonder","xylophone","xerox","yellow","yogurt","zephyr",
    "zebra","zombie","quantum","jigsaw","sphinx","kingdom","lantern",
    "falcon","breeze","forest","glimmer","harbor","impact","jaguar",
    "magnet","nexus",
]

# ── לוג שאילתות ──────────────────────────────────────────────────
query_log = []
log_lock  = threading.Lock()

# ── טעינת דף הלקוח — תיקון encoding ל-Windows ──────────────────
def _load_client_html():
    client_path = os.path.join(os.path.dirname(__file__), 'cipher_client.html')
    if os.path.exists(client_path):
        with open(client_path, encoding='utf-8') as f:   # <── תיקון עיקרי
            return f.read()
    return "<h1>cipher_client.html not found — place it next to cipher_machine_v2.py</h1>"

CLIENT_HTML = _load_client_html()


def encrypt(text, dictionary):
    result = []
    for char in text.lower():
        if char == ' ':
            wi = random.randint(0, len(dictionary) - 1)
            result.append((wi, len(dictionary[wi])))
            continue
        if not char.isalpha():
            continue
        candidates = [
            (wi, li)
            for wi, word in enumerate(dictionary)
            for li, letter in enumerate(word)
            if letter == char
        ]
        result.append(random.choice(candidates) if candidates else None)
    return result


def format_output(pairs):
    return " ".join(
        "[?]" if p is None else f"[{p[0]},{p[1]}]"
        for p in pairs
    )


class CipherHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        path   = parsed.path

        if path == '/':
            self._serve_html(CLIENT_HTML)

        elif path == '/encrypt':
            text = params.get('text', [''])[0][:200]
            team = params.get('team', ['אנונימי'])[0][:30]
            if not text:
                self._json({'error': 'empty'}, 400)
                return

            pairs  = encrypt(text, SECRET_DICTIONARY)
            result = format_output(pairs)

            entry = {
                'id':        len(query_log) + 1,
                'team':      team,
                'plaintext': text,
                'encrypted': result,
                'time':      datetime.now().strftime('%H:%M:%S'),
            }
            with log_lock:
                query_log.append(entry)

            print(f"  [{team}] '{text}' -> {result}")
            self._json({'encrypted': result, 'id': entry['id']})

        elif path == '/log':
            since = int(params.get('since', ['0'])[0])
            with log_lock:
                new_entries = [e for e in query_log if e['id'] > since]
            self._json({'entries': new_entries, 'total': len(query_log)})

        elif path == '/status':
            self._json({'ok': True, 'total': len(query_log)})

        else:
            self.send_response(404)
            self.end_headers()

    def _serve_html(self, html):
        body = html.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type',  'text/html; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type',  'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass   # suppress default logs


def run(port=8000):
    print("""
+--------------------------------------------------+
|       מכונת הצפנה v2 - צד המורה                 |
+--------------------------------------------------+
|  קבוצות:  http://localhost:8000                  |
|  דשבורד:  teacher_dashboard_v2.html             |
|                                                  |
|  endpoints:                                      |
|    GET /encrypt?text=...&team=...                |
|    GET /log?since=<id>                           |
|    GET /status                                   |
|                                                  |
|  עצור: Ctrl+C                                   |
+--------------------------------------------------+
""")
    server = http.server.HTTPServer(('', port), CipherHandler)
    server.serve_forever()


if __name__ == '__main__':
    run()
