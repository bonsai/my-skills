---
name: natalie
description: "Use ONLY when the user asks about port management, port usage, port history, or wants to register/query/release ports. Keywords: ポート, natalie, ナタリー, port, ports.db, ポート履歴, ポート管理, port assignment. Manages all port allocations via SQLite database."
license: MIT
---

# Natalie (ナタリー) — Port Manager

Port management assistant. Manages all port assignments via SQLite database at `~/.config/opencode/skills/natalie/ports.db`.

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS ports (
  port INTEGER PRIMARY KEY,
  service TEXT NOT NULL,
  path TEXT,
  status TEXT DEFAULT 'active',  -- active / released / reserved
  pid INTEGER,
  started_at TEXT DEFAULT (datetime('now')),
  stopped_at TEXT,
  notes TEXT
);
```

## Commands (all via Python script)

Script: `~/.config/opencode/skills/natalie/natalie.py`

### Status (all active + history)
```bash
python3 ~/.config/opencode/skills/natalie/natalie.py status
```

### Register
```bash
python3 ~/.config/opencode/skills/natalie/natalie.py register <PORT> <SERVICE> [PATH] [PID] [NOTES]
```

### Release
```bash
python3 ~/.config/opencode/skills/natalie/natalie.py release <PORT>
```

### Scan OS & sync DB
```bash
python3 ~/.config/opencode/skills/natalie/natalie.py scan
```

### Direct SQL via Python (no sqlite3 CLI needed)
```python
import sqlite3
conn = sqlite3.connect(os.path.expanduser("~/.config/opencode/skills/natalie/ports.db"))
# query here
```

## Workflow

1. Before assigning a port: query DB to check if already in use
2. After starting a service: register in DB with PID
3. Before stopping: update DB to 'released'
4. Periodically run sync to detect OS-level changes
5. Use history to troubleshoot port conflicts

## Known Ports

| Port | Service | Path |
|------|---------|------|
| 3000 | SB-BBS (掲示板) | /home/bons/SERVER/3001-SB-BBS |
| 3019 | SB-BBS admin | /home/bons/SERVER/3001-SB-BBS |
| 5173 | voice-bbs-web | /home/bons/repos/voice-bbs-web/apps/web-vue |
| — | extreme-norikae (future) | /home/bons/repos/extreme-norikae |
