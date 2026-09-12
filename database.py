import sqlite3
import os
import json
import time

DB_PATH = os.path.join(os.path.dirname(__file__), "IslaSalvaje_World.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        device_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        character_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER NOT NULL,
        name TEXT UNIQUE NOT NULL,
        class_name TEXT NOT NULL,
        level INTEGER DEFAULT 1,
        experience INTEGER DEFAULT 0,
        health REAL DEFAULT 100.0,
        hunger REAL DEFAULT 100.0,
        thirst REAL DEFAULT 100.0,
        stamina REAL DEFAULT 100.0,
        mana REAL DEFAULT 100.0,
        pos_x REAL DEFAULT 0.0,
        pos_y REAL DEFAULT 0.0,
        pos_z REAL DEFAULT 100.0,
        rot_yaw REAL DEFAULT 0.0,
        is_sleeping INTEGER DEFAULT 0,
        last_online REAL DEFAULT 0.0,
        FOREIGN KEY (account_id) REFERENCES accounts(account_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS class_definitions (
        class_name TEXT PRIMARY KEY,
        display_name TEXT NOT NULL,
        description TEXT,
        str_stat INTEGER NOT NULL,
        dex_stat INTEGER NOT NULL,
        con_stat INTEGER NOT NULL,
        int_stat INTEGER NOT NULL,
        wis_stat INTEGER NOT NULL,
        cha_stat INTEGER NOT NULL,
        passive_name TEXT NOT NULL,
        passive_desc TEXT NOT NULL,
        active_name TEXT NOT NULL,
        active_desc TEXT NOT NULL,
        primary_weapon TEXT NOT NULL
    );
    """)

    classes_data = [
        ("Warrior", "Guerrero (Bárbaro de las Estepas)", "Tanque demoledor de primera línea con hachas de guerra y control de masas.", 
         17, 13, 15, 8, 12, 10, 
         "Piel de Hierro", "Inmunidad al primer aturdimiento y 25% reducción de daño físico.", 
         "Carga Sísmica", "Embestida arrolladora que derriba enemigos y debilita estructuras de madera.", "Hacha Doble"),
        
        ("Assassin", "Asesino (Sombra Letal)", "Maestro del sigilo, crítico devastador y movilidad vertical con dagas.", 
         10, 18, 12, 10, 14, 12, 
         "Pasos de Pluma", "Silencio total al caminar/agacharse y 30% bonus de daño por la espalda.", 
         "Paso Sombrío", "Teletransporte instantáneo tras la espalda del objetivo con golpe cegador.", "Dagas Gemelas"),
        
        ("Mage", "Mago (Archimago del Vacío)", "Hechicero de alto rango con control elemental, asedio destructivo y runas.", 
         8, 12, 10, 18, 14, 14, 
         "Visión Astral", "Permite detectar siluetas de jugadores y cofres a través de paredes delgadas.", 
         "Runa de Asedio / Meteoro", "Invoca un proyectil ígneo de alto impacto que inflige gran daño a estructuras y áreas.", "Bastón Arcano"),
        
        ("Hunter", "Cazador (Rastreador Salvaje)", "Tirador experto a larga distancia, domesticador de bestias y rastreador.", 
         12, 17, 14, 9, 16, 10, 
         "Rastro de Sangre", "Resalta pisadas y rastros de presas y jugadores con salud menor al 50%.", 
         "Lluvia de Flechas", "Descarga de proyectiles perforantes en abanico que ralentizan a los objetivos alcanzados.", "Arco Largo"),
        
        ("Shaman", "Chamán (Guardián Primordial)", "Conjurador espiritual que canaliza totems, sanación grupal y control de tierra.", 
         12, 10, 16, 12, 18, 12, 
         "Vínculo Vital", "Aura regenerativa que restaura salud a aliados cercanos y repara construcciones lentas.", 
         "Prisión de Raíces", "Raíces emergen del suelo inmovilizando a enemigos por 4 segundos.", "Tótem / Maza")
    ]

    for c in classes_data:
        cursor.execute("""
        INSERT OR REPLACE INTO class_definitions 
        (class_name, display_name, description, str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat, passive_name, passive_desc, active_name, active_desc, primary_weapon)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, c)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventories (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        character_id INTEGER NOT NULL,
        slot_type TEXT NOT NULL,
        slot_index INTEGER NOT NULL,
        item_id TEXT NOT NULL,
        quantity INTEGER DEFAULT 1,
        durability REAL DEFAULT 100.0,
        FOREIGN KEY (character_id) REFERENCES characters(character_id),
        UNIQUE(character_id, slot_type, slot_index)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buildings (
        structure_id TEXT PRIMARY KEY,
        owner_character_id INTEGER NOT NULL,
        part_type TEXT NOT NULL,
        tier INTEGER DEFAULT 1,
        health REAL DEFAULT 500.0,
        pos_x REAL NOT NULL,
        pos_y REAL NOT NULL,
        pos_z REAL NOT NULL,
        rot_pitch REAL DEFAULT 0.0,
        rot_yaw REAL DEFAULT 0.0,
        rot_roll REAL DEFAULT 0.0,
        decay_time REAL NOT NULL,
        FOREIGN KEY (owner_character_id) REFERENCES characters(character_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tool_cupboards (
        tc_id TEXT PRIMARY KEY,
        owner_character_id INTEGER NOT NULL,
        authorized_players_json TEXT DEFAULT '[]',
        wood_upkeep INTEGER DEFAULT 0,
        stone_upkeep INTEGER DEFAULT 0,
        metal_upkeep INTEGER DEFAULT 0,
        pos_x REAL NOT NULL,
        pos_y REAL NOT NULL,
        pos_z REAL NOT NULL,
        protected_until REAL NOT NULL,
        FOREIGN KEY (owner_character_id) REFERENCES characters(character_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS code_locks (
        lock_id TEXT PRIMARY KEY,
        structure_id TEXT NOT NULL,
        pin_code TEXT NOT NULL,
        owner_character_id INTEGER NOT NULL,
        authorized_players_json TEXT DEFAULT '[]',
        FOREIGN KEY (structure_id) REFERENCES buildings(structure_id),
        FOREIGN KEY (owner_character_id) REFERENCES characters(character_id)
    );
    """)

    # Seed an initial test character
    cursor.execute("INSERT OR IGNORE INTO accounts (account_id, username, password_hash, device_id) VALUES (1, 'Admin', 'admin_hash', 'MOBILE_DEVICE_01');")
    cursor.execute("""
    INSERT OR IGNORE INTO characters (character_id, account_id, name, class_name, level, experience, health, hunger, thirst, stamina, mana, pos_x, pos_y, pos_z)
    VALUES (1, 1, 'Thabbela', 'Warrior', 25, 14200, 100.0, 85.0, 90.0, 100.0, 60.0, 1500.0, -2300.0, 120.0);
    """)

    conn.commit()
    conn.close()
    print("[Database] SQLite Database successfully initialized at:", DB_PATH)

if __name__ == "__main__":
    init_db()