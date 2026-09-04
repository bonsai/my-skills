---
name: bbs-manager
description: Use ONLY when the user asks to start, stop, restart, check status, or manage the SB-BBS (掲示板) server at /home/bons/SERVER/3001-SB-BBS. Front-load keywords: 掲示板, bbs, board, sb-bbs, 3001-SB-BBS. Covers Java/Spring Boot startup on port 3000, portproxy setup, and health checks.
---

# SB-BBS Manager

This skill manages the Spring Boot bulletin board (掲示板) server located at `/home/bons/SERVER/3001-SB-BBS`.

## Project Info

- **Path**: `/home/bons/SERVER/3001-SB-BBS`
- **Framework**: Spring Boot 3.3.5 (Java 17, Maven, SQLite)
- **Port**: 3000 (both main and Tomcat admin)
- **JAR**: `target/board-0.1.0.jar`
- **DB**: SQLite at `board.db`
- **Windows LAN access**: `http://192.168.56.1:3000` (via netsh portproxy)

## Common Commands

### Status check
```bash
ss -tlnp | grep 3000
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
ps aux | grep board-0.1.0 | grep -v grep
```

### Start (background, survives shell exit)
```bash
setsid nohup java -jar /home/bons/SERVER/3001-SB-BBS/target/board-0.1.0.jar > /tmp/bbs-server.log 2>&1 &
```

### Stop
```bash
lsof -ti:3000 | xargs kill -9 2>/dev/null
```

### Rebuild and restart
```bash
cd /home/bons/SERVER/3001-SB-BBS
lsof -ti:3000 | xargs kill -9 2>/dev/null
sleep 2
mvn clean package -DskipTests -q
setsid nohup java -jar target/board-0.1.0.jar > /tmp/bbs-server.log 2>&1 &
sleep 4
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
```

### View logs
```bash
tail -50 /tmp/bbs-server.log
```

### Portproxy setup (Windows PowerShell admin)
```powershell
netsh interface portproxy add v4tov4 listenport=3000 listenaddress=192.168.56.1 connectport=3000 connectaddress=172.18.249.151
```
Note: WSL2 IP changes on reboot. Update `connectaddress` with current WSL IP (`ip addr show eth0 | grep inet`).

## Workflow

1. Always check status before starting (avoid duplicate instances)
2. Use `setsid nohup` so the process survives shell termination
3. Verify with curl after startup (expect HTTP 200)
4. If rebuilding, stop first, then build, then start
5. Register/release ports in port-manager DB after any change

## Port Manager Integration

Use `port-manager.py` to track all port assignments in `ports.db`.

```bash
# Before starting: check port is free
python3 ~/.opencode/skills/port-manager/port-manager.py scan

# After starting: register port
python3 ~/.opencode/skills/port-manager/port-manager.py register 3000 SB-BBS /home/bons/SERVER/3001-SB-BBS <PID> "掲示板 Spring Boot"

# Before stopping: release port
python3 ~/.opencode/skills/port-manager/port-manager.py release 3000

# Full history
python3 ~/.opencode/skills/port-manager/port-manager.py status
```
