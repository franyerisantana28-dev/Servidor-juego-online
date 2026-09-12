import urllib.request, json, time, subprocess, sys

proc = subprocess.Popen([sys.executable, "Server/server.py"])
time.sleep(1.5)

try:
    req = urllib.request.urlopen("http://127.0.0.1:8080/api/classes")
    data = json.loads(req.read().decode("utf-8"))
    print("SERVER API SUCCESS: Found", len(data["classes"]), "classes.")
    for c in data["classes"]:
        print(f" - {c['display_name']}: STR={c['str_stat']}, DEX={c['dex_stat']}, Passive={c['passive_name']}")
    
    req_char = urllib.request.urlopen("http://127.0.0.1:8080/api/characters/list?account_id=1")
    char_data = json.loads(req_char.read().decode("utf-8"))
    print("CHARACTERS IN DB:", len(char_data["characters"]))
    for ch in char_data["characters"]:
        print(f" * ID={ch['character_id']}, Name={ch['name']}, Class={ch['class_name']}, Lvl={ch['level']}")
finally:
    proc.terminate()