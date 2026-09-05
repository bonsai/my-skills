# voice-bbs (Voice BBS Web 開発スキル・プロジェクト設定)

Voice BBS Web 固有の設定・文書・経緯を保持する薄いスキル。手順は汎用マイクロスキルへ委譲する。

## 発動トリガー
- プロジェクト固有の ID/用語を見たら: 「voice-bbs」「D1/T2/BE/room/声の泡」「進捗(voice-bbs)」
- プロジェクトでの作業一般(汎用手順は各 dev-* が発動)

## 汎用マイクロスキル(委譲先)
| タスク | スキル |
|---|---|
| 文書先行・規約 | dev-docs-driven |
| テスト先行実装 | dev-tdd-vitest |
| 10分スプリント | dev-sprint10 |
| 進捗の色分け確認 | dev-progress-board |
| 意思決定→ADR | dev-decision-adr |
| セッション振り返り | dev-recap |

## プロジェクト設定
- GitHub: https://github.com/bonsai/voice-bbs-web(master直push・作業前に `git pull`)
- 主線: apps/web-vue(preview https://voice-bbs-web-vue.pages.dev、vitest 21)
- 残置・無視: apps/web-next(本番 https://voice-bbs-web.pages.dev)。触らない
- バックエンド: kimura へ委譲(BE1〜7)。フロントは削除APIのみ
- 判断済: D2(並行)/ D4=a(PWA Phase分割)/ D5(自前トークン)。**D1(UX A/B/C)は実機検証待ち**
- wrangler: apps/web-next/node_modules/.bin/wrangler(Linux)・CLOUDFLARE_API_TOKEN
- ID凡例・略号: docs/abb.md / 状況: docs/issue.md・kanban.md・recap.md / 会議: research/DESIGN_MEETING_*

## 注意
- 実機(録音/再生)は人間確認前提(Q1)。本番 deploy は承認必須
- 状態数値は docs を読んで更新(他ストリーム進捗に注意)
