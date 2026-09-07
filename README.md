# my-skills

**bonsai の全スキル repo の index**（GitHub 連携・構造化クラスタリング済み）

GitHub 上にある全スキルリポジトリ群をドメインクラスタごとに索引化するエントリーポイント。
観測は [github-observatory](https://github.com/bonsai/github-observatory) の全量スキャン
（1444 repos / 2026-09-07）を基にしている。

```text
github-observatory ──report──▶ my-skills (index) ──▶ 各 *-skill repo
```

## install

```bash
# opencode
ln -s ~/repos/<skill>/* ~/.opencode/skills/   # flat 収録分のみ

# pi
ln -s ~/repos/my-skills/* ~/.agents/skills/
```

## スキル index（ドメインクラスタ）

### 1. devops / shell / 環境操作

| Skill | GitHub | 用途 |
|-------|--------|------|
| asus-shutdown-skill | https://github.com/bonsai/asus-shutdown-skill | ASUS シャットダウン制御 |
| wifi-mac-rotate-skill | https://github.com/bonsai/wifi-mac-rotate-skill | MAC アドレスローテーション |
| wakeword-skill | https://github.com/bonsai/wakeword-skill | ウェイクワード |
| winget-skill | https://github.com/bonsai/winget-skill | WinGet パッケージ管理 |
| startup-ahk-skill | https://github.com/bonsai/startup-ahk-skill | AutoHotkey 起動管理 |
| block-qr-skill | https://github.com/bonsai/block-qr-skill | QR ブロック生成 |
| cf-mode-skill | https://github.com/bonsai/cf-mode-skill | Cloudflare モード切替 |
| logging-skill | https://github.com/bonsai/logging-skill | ログ取得 |
| journal-skill | https://github.com/bonsai/journal-skill | ジャーナル記録 |
| git-helper-skill | https://github.com/bonsai/git-helper-skill | git 操作補助 |
| env-consolidate-skill | https://github.com/bonsai/env-consolidate-skill | 環境変数統合 |
| env-report-skill | https://github.com/bonsai/env-report-skill | 環境レポート |
| diff-skills | https://github.com/bonsai/diff-skills | CLI エージェント資産の差分管理 |
| qwen-skills | https://github.com/bonsai/qwen-skills | Qwen CLI スキル集 |
| pi-skills | https://github.com/bonsai/pi-skills | pi 用スキル集 |
| my-skills | https://github.com/bonsai/my-skills | 本リポジトリ（index） |
| skills-crlf-fix | https://github.com/bonsai/skills-crlf-fix | CRLF 修正 |
| skills-mcp-go | https://github.com/bonsai/skills-mcp-go | skills → MCP tool 化 |

### 2. agents / 実行基盤

| Skill | GitHub | 用途 |
|-------|--------|------|
| kimurasan-skill | https://github.com/bonsai/kimurasan-skill | kimura（生成物係）操作 |
| repos-agent-skill | https://github.com/bonsai/repos-agent-skill | repos エージェント |
| deploy-agent-skill | https://github.com/bonsai/deploy-agent-skill | デプロイ実行 |
| model-agent-skill | https://github.com/bonsai/model-agent-skill | Model Manager 連携 |
| inventory-skill | https://github.com/bonsai/inventory-skill | 資産棚卸 |
| inventory-graph-agent-skill | https://github.com/bonsai/inventory-graph-agent-skill | 資産グラフ化 |
| dep-finder-skill | https://github.com/bonsai/dep-finder-skill | 依存発見 |
| mcp-doctor-skill | https://github.com/bonsai/mcp-doctor-skill | MCP 診断 |
| error-log-expert-skill | https://github.com/bonsai/error-log-expert-skill | エラーログ解析 |
| schedule-planner-skill | https://github.com/bonsai/schedule-planner-skill | 行動予定立案 |
| task-crawler-skill | https://github.com/bonsai/task-crawler-skill | Task 収集 |
| task-hub-skill | https://github.com/bonsai/task-hub-skill | Task 集約 |
| event-crawler-skill | https://github.com/bonsai/event-crawler-skill | イベント収集 |
| chrome-tabs-skill | https://github.com/bonsai/chrome-tabs-skill | Chrome タブ操作 |
| devmgmt-hid-skill | https://github.com/bonsai/devmgmt-hid-skill | HID デバイス管理 |
| tab-inference-skill | https://github.com/bonsai/tab-inference-skill | タブ推論 |
| sticky-notes-skill | https://github.com/bonsai/sticky-notes-skill | 付箋管理 |
| bq-monitor-skill | https://github.com/bonsai/bq-monitor-skill | BigQuery 監視 |

### 3. AI / モデル

| Skill | GitHub | 用途 |
|-------|--------|------|
| sakura-model-skill | https://github.com/bonsai/sakura-model-skill | Sakura モデル連携 |
| deepseel-skill | https://github.com/bonsai/deepseel-skill | DeepSeek 連携 |
| ocgo-usage-skill | https://github.com/bonsai/ocgo-usage-skill | ocgo 利用 |
| mp3-tag-skill | https://github.com/bonsai/mp3-tag-skill | MP3 タグ編集 |

### 4. content / 執筆・メディア

| Skill | GitHub | 用途 |
|-------|--------|------|
| article-update-skill | https://github.com/bonsai/article-update-skill | 記事更新 |
| auto-recap-skill | https://github.com/bonsai/auto-recap-skill | 自動レキャップ |
| nippou-skill | https://github.com/bonsai/nippou-skill | 日報生成 |
| qiita-post-skill | https://github.com/bonsai/qiita-post-skill | Qiita 投稿 |
| parent-child-article-skill | https://github.com/bonsai/parent-child-article-skill | 親子記事構成 |
| portfolio-advisor-skill | https://github.com/bonsai/portfolio-advisor-skill | ポートフォリオ助言 |
| receiptline-skill | https://github.com/bonsai/receiptline-skill | レシート読み取り |
| genre-master-skill | https://github.com/bonsai/genre-master-skill | ジャンル分析 |
| music-conductor-skill | https://github.com/bonsai/music-conductor-skill | 音楽生成指揮 |
| music-strategy-skill | https://github.com/bonsai/music-strategy-skill | 音楽戦略 |
| biz-invest-skill | https://github.com/bonsai/biz-invest-skill | 投資調査 |
| life-design-skill | https://github.com/bonsai/life-design-skill | ライフ設計 |

### 5. hermes / その他コレクション

| Skill | GitHub | 用途 |
|-------|--------|------|
| hermes-skills | https://github.com/bonsai/hermes-skills | Hermes スキル集 |
| hermes-agent-skills | https://github.com/bonsai/hermes-agent-skills | Hermes Agent スキル backup |
| ms-skills | https://github.com/bonsai/ms-skills | Microsoft Foundry 移植スキル |
| threejs-skills | https://github.com/bonsai/threejs-skills | three.js スキル |
| andrej-karpathy-skills | https://github.com/bonsai/andrej-karpathy-skills | Karpathy CLAUDE.md 流用 |

## 本リポジトリ内 flat 収録スキル（opencode / pi 直接 install 分）

| Skill | Origin | Purpose |
|-------|--------|---------|
| bbs-manager | opencode | SB-BBS server management |
| bonsai-pruner | opencode | Dead code removal |
| daihon | opencode | 漫才MP3 generation |
| daily-ss | opencode | Daily short stories |
| ext-install | opencode | Browser extension installer |
| geo-factory | opencode | Geometric animation |
| mala | pi | MALA inspection ontology |
| model-match-search | opencode | PC spec → model matching |
| natalie | opencode | Port management (元 port-manager) |
| oshare-uiux | opencode | idol-oshare UI/UX |
| play-mp4 | opencode | MP4 playback |
| repo-theme-conversion | opencode | Project retheme |
| research-by-bookmark | opencode | Bookmark → research |
| sync-repos | opencode | GitHub sync tool |
| ux-guardian | opencode | UX review guard |
| vanilla-web-dev | pi | Vanilla TS web dev |
| vault-manager | opencode | Encrypted backup |

## 関連ツール repo（クラウドリンク）

| Tool | GitHub | 役割 |
|------|--------|------|
| gh-aw | https://github.com/bonsai/gh-aw | Archimedes の GitHub 実行基盤（Issue/PR/workflow/push） |
| archimedes | https://github.com/bonsai/archimedes | Repository Architecture Agent（SCAN→CLUSTER→ADVISE→TASK） |
| sync-repos | https://github.com/bonsai/sync-repos | ローカル repo push / CI workflow |
| github-observatory | https://github.com/bonsai/github-observatory | リポジトリ観測所（DWH + BQML） |
| sorette | https://github.com/bonsai/sorette | 責務ドメインタグ推論・hot/warm/cold |
| repos | https://github.com/bonsai/repos | repos 資産管理（new + observatory 統合） |