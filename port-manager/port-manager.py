#!/usr/bin/env python3
"""Port Manager - ポート履歴管理ツール"""
import sqlite3, sys, os

DB = os.path.expanduser("~/.opencode/skills/port-manager/ports.db")

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS ports (
        port INTEGER PRIMARY KEY,
        service TEXT NOT NULL,
        path TEXT,
        status TEXT DEFAULT 'active',
        pid INTEGER,
        started_at TEXT DEFAULT (datetime('now','localtime')),
        stopped_at TEXT,
        notes TEXT
    )""")
    conn.commit()
    conn.close()

def register(port, service, path="", pid=None, notes=""):
    conn = get_db()
    conn.execute(
        "INSERT OR REPLACE INTO ports (port, service, path, status, pid, started_at, notes) VALUES (?,?,?,?,?,datetime('now','localtime'),?)",
        (port, service, path, 'active', pid, notes))
    conn.commit()
    conn.close()
    print(f"Registered: {port} -> {service}")

def release(port):
    conn = get_db()
    conn.execute(
        "UPDATE ports SET status='released', stopped_at=datetime('now','localtime') WHERE port=? AND status='active'",
        (port,))
    conn.commit()
    conn.close()
    print(f"Released: {port}")

def status():
    conn = get_db()
    print("=== Active Ports ===")
    for r in conn.execute("SELECT port, service, pid, started_at, notes FROM ports WHERE status='active' ORDER BY port"):
        print(f"  {r['port']:<6} {r['service']:<20} PID:{str(r['pid'] or '-'):<8} {r['started_at']}  {r['notes'] or ''}")
    print("\n=== History ===")
    for r in conn.execute("SELECT port, service, status, started_at, stopped_at FROM ports ORDER BY port, started_at"):
        print(f"  {r['port']:<6} {r['service']:<20} {r['status']:<10} {r['started_at']} -> {r['stopped_at'] or '-'}")
    conn.close()

def scan():
    import subprocess
    result = subprocess.run(['ss', '-tlnp'], capture_output=True, text=True)
    conn = get_db()
    count = 0
    for line in result.stdout.strip().split('\n')[1:]:
        parts = line.split()
        addr = parts[3]
        port = int(addr.rsplit(':', 1)[1])
        existing = conn.execute("SELECT 1 FROM ports WHERE port=? AND status='active'", (port,)).fetchone()
        if not existing:
            svc = parts[5] if len(parts) > 5 else 'unknown'
            conn.execute(
                "INSERT INTO ports (port, service, status, notes) VALUES (?,?,'active','auto-detected')",
                (port, svc))
            count += 1
    conn.commit()
    print(f"Synced: {count} new port(s) detected")
    status()
    conn.close()

if __name__ == '__main__':
    init_db()
    if len(sys.argv) < 2:
        print("Usage: port-manager.py [status|scan|register <port> <service> [path] [pid] [notes]]|release <port>")
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == 'status': status()
    elif cmd == 'scan': scan()
    elif cmd == 'register': register(int(sys.argv[2]), sys.argv[3], *sys.argv[4:6] if len(sys.argv)>5 else ("",), int(sys.argv[6]) if len(sys.argv)>6 else None, sys.argv[7] if len(sys.argv)>7 else "")
    elif cmd == 'release': release(int(sys.argv[2]))
    else: print(f"Unknown command: {cmd}")
