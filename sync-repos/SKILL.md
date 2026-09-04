---
name: sync-repos
description: "Use when the user asks to sync local projects to GitHub, push repos, scan project directories, create GitHub repos, run CI workflows, or manage the sync-repos tool at ~/sync-repos (private repo bonsai/sync-repos). Keywords: sync-repos, 同期, sync, push, repo create, inventory, GitHub auth proxy, github-auth-proxy, projects dashboard. Use ONLY when the sync-repos tool or its Docker proxy is being used; do not use for general git operations."
license: MIT
---

# sync-repos

ローカルプロジェクトを GitHub に push し、CI ワークフローを自動設定するツール。
ソース: private repo `bonsai/sync-repos`、ローカルクローンは `~/sync-repos`。

## アーキテクチャ

```
scan → (git init) → gh repo create (なければ) → push → .github/workflows/build.yml 生成
```

- Go CLI で `scan / push / status / prune` を実行する計画 (KANBAN.md)
- 現行実装は Docker コンテナ「GitHub Auth Proxy」(スマホ認証のみ・トークン非保存) が中心
  - `entrypoint.sh`: スキャン → 認証確認 → SQLite初期化 → HTTP API (:8888)
  - `inventory.py`: プロジェクト自動スキャン
  - `docker-compose.yml`: 常駐サービス (`github-auth-proxy`)

## 主要ファイル

| ファイル | 役割 |
|---|---|
| `entrypoint.sh` | 初期化 + ダーモン (inventory → auth → DB → proxy API) |
| `inventory.py` | プロジェクトフォルダのスキャン/インベントリ生成 |
| `scan_personal.py` | 個人情報検知スキャン (軽量チェックのみ) |
| `scripts/sync-repos.sh` | ローカル push スクリプト (bash) |
| `scripts/sync-repos.ps1` | ローカル push スクリプト (PowerShell) |
| `scripts/run-sync.ps1` | docker-compose 起動 + ヘルスチェック + 認証確認 |
| `docker-compose.yml` | `github-auth-proxy` コンテナ定義 (port 8888) |
| `docs/PROXY-README.md` | プロキシ運用マニュアル |
| `KANBAN.md` | Go CLI 設計・フェーズ計画 |

## 使い方

### Docker プロキシ起動

```bash
cd ~/sync-repos
docker-compose up -d --build
```

- API: `http://localhost:8888/health`, `/api/auth/status`, `/api/projects`, `/api/inventory`
- 認証 (スマホ): `docker exec -it github-auth-proxy gh auth login -p https`
- コンテナ停止でセッション消去 (再認証必要)

### ローカル push スクリプト (gh CLI 認証済み)

```bash
cd ~/sync-repos
PROJECTS_DIR=/path/to/projects bash scripts/sync-repos.sh
```

前提条件: `gh auth login` 済み、`git` インストール済み。

## 注意点

- **認証**: `gh auth status` を実行してから操作する。未認証ならエラーで終了。
- **トークン非保存**: Docker プロキシはセッション型。再起動で再認証が必要。
- **シークレット漏れ防止**: `.env` やトークンをコミットしない。個人情報スキャンは `scan_personal.py` で実施可能。
- **push 先**: リポジトリ名 = ディレクトリ名。デフォルト可視性は gh のユーザー設定に従う。
