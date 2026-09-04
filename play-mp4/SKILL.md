---
name: play-mp4
description: "MP4ファイルを探して再生する。動画ファイルの再生、起動。keywords: mp4, 再生, play, 動画, video, start, open"
license: MIT
---

# Play MP4

指定パスまたはカレント以下のMP4を再生する。

## 使い方

```
/play-mp4
/play-mp4 /home/bons/wiki/projects/shorts-factory/facemesh.mp4
```

## 処理

1. パスが指定されていればそのファイルを再生
2. なければカレント以下から最新のmp4を探して再生
3. WSLパス → Windowsパスに変換 → `explorer.exe` で開く

## コマンド

```bash
# 指定ファイル再生
explorer.exe "$(wslpath -w <path>)"

# 最新mp4を検索して再生
find . -name '*.mp4' -printf '%T@ %p\n' | sort -rn | head -1 | cut -d' ' -f2-
```
