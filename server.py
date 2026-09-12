"""
Isla Salvaje - High Performance Multiplayer REST & State Sync Server
Provides online persistence for Unreal Engine mobile clients.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import os
import urllib.parse

DB_PATH = os.path.join(os.path.dirname(__file__), "IslaSalvaje_World.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class IslaSalvajeServer(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        conn = get_db()
        cursor = conn.cursor()

        if path == "/api/status":
            self._send_json({"status": "ONLINE", "server_name": "Isla Salvaje 01", "max_players": 100, "region": "SA-Brazil"})
        
        elif path == "/api/classes":
            cursor.execute("SELECT * FROM class_definitions;")
            rows = [dict(r) for r in cursor.fetchall()]
            self._send_json({"classes": rows})
        
        elif path == "/api/characters/list":
            account_id = query.get("account_id", [1])[0]
            cursor.execute("SELECT * FROM characters WHERE account_id = ?;", (account_id,))
            rows = [dict(r) for r in cursor.fetchall()]
            self._send_json({"characters": rows, "count": len(rows), "max_slots": 10})
        
        elif path == "/api/world/structures":
            cursor.execute("SELECT * FROM buildings;")
            rows = [dict(r) for r in cursor.fetchall()]
            self._send_json({"structures": rows})
            
        else:
            self._send_json({"error": "Endpoint not found"}, status=404)
        
        conn.close()

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(content_len).decode('utf-8')) if content_len > 0 else {}
        path = self.path

        conn = get_db()
        cursor = conn.cursor()

        if path == "/api/characters/create":
            account_id = body.get("account_id", 1)
            name = body.get("name", "Nómada")
            class_name = body.get("class_name", "Warrior")
            try:
                cursor.execute("""
                INSERT INTO characters (account_id, name, class_name, level, experience, health, hunger, thirst, stamina, mana, pos_x, pos_y, pos_z)
                VALUES (?, ?, ?, 1, 0, 100.0, 100.0, 100.0, 100.0, 100.0, 0.0, 0.0, 100.0);
                """, (account_id, name, class_name))
                char_id = cursor.lastrowid
                conn.commit()
                self._send_json({"success": True, "character_id": char_id, "name": name, "class_name": class_name})
            except sqlite3.IntegrityError:
                self._send_json({"success": False, "error": "Character name already exists"}, status=400)

        elif path == "/api/characters/sync":
            char_id = body.get("character_id")
            cursor.execute("""
            UPDATE characters SET health = ?, hunger = ?, thirst = ?, stamina = ?, mana = ?, pos_x = ?, pos_y = ?, pos_z = ?, is_sleeping = ?
            WHERE character_id = ?;
            """, (body.get("health", 100), body.get("hunger", 100), body.get("thirst", 100), body.get("stamina", 100),
                  body.get("mana", 100), body.get("pos_x", 0), body.get("pos_y", 0), body.get("pos_z", 0), body.get("is_sleeping", 0), char_id))
            conn.commit()
            self._send_json({"success": True, "synced": True})

        elif path == "/api/world/build":
            s_id = body.get("structure_id")
            cursor.execute("""
            INSERT OR REPLACE INTO buildings (structure_id, owner_character_id, part_type, tier, health, pos_x, pos_y, pos_z, rot_yaw, decay_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (s_id, body.get("owner_id", 1), body.get("part_type", "Foundation"), body.get("tier", 1),
                  body.get("health", 500.0), body.get("pos_x", 0), body.get("pos_y", 0), body.get("pos_z", 0), body.get("rot_yaw", 0), body.get("decay_time", 86400)))
            conn.commit()
            self._send_json({"success": True, "structure_id": s_id})
            
        else:
            self._send_json({"error": "Endpoint not found"}, status=404)

        conn.close()

def run(port=8080):
    server = HTTPServer(('0.0.0.0', port), IslaSalvajeServer)
    print(f"[IslaSalvajeServer] Multiplayer Server running on port {port}...")
    server.serve_forever()

if __name__ == "__main__":
    run()