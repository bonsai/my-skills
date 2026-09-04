---
name: daily-ss
description: |
  Use when the user asks to write short stories, generate SS, or create 星新一風ショートショート.
  Reads random wiki content and generates 3 stories per day.
---

# Daily Short Story Generator

毎日3話の星新一風ショートショートを生成するスキル。

## 使い方

```bash
python3 .opencode/skills/daily-ss/main.py
出力
- db/ss_data.dbに保存
- コンソールに作品番号とスコア表示

### 登録方法

`opencode.json` に追加:
```json
{
  "skills": {
    "paths": [".opencode/skills"]
  }
}
```

### 実行スケジュール（オプション）
HERMESのcronjobで毎日自動実行:
hermes cronjob create \
  --name "daily-ss" \
  --schedule "0 9 * * *" \
  --prompt "opencode run --skill daily-ss"
この計画で問題なければ、実装を開始します。修正点はありますか？