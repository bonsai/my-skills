---
name: oshare-uiux
description: "idol-oshare の UI/UX 改修作業用リファレンス。ホワイトボードSPA (index.html) と BBSページ (bbs.html) のデザインシステム・カラーパレット7テーマ。Use when editing idol-oshare UI/UX or its design system. Keywords: idol-oshare, UI, UX, デザイン, ホワイトボード, oshare."
license: MIT
---

# Skill: oshare-uiux

idol-oshare の UI/UX 改修作業用リファレンス。

## 対象
- `/home/bons/repos/idol-oshare/site/index.html` — ホワイトボード SPA
- `/home/bons/repos/idol-oshare/site/bbs.html` — BBSページ

## デザインシステム

### カラーパレット（7テーマ）
| テーマ | 色 | 用途 |
|--------|------|------|
| コンセプト | #fff59d | プロジェクト全体像 |
| キャラクター | #f8bbd0 | キャラ設定 |
| 技術 | #b3e5fc | 技術スタック |
| 配信・コンテンツ | #c8e6c9 | 配信企画 |
| 楽曲・パフォ | #ffe0b2 | 楽曲/パフォーマンス |
| 広報・SNS | #d1c4e9 | マーケティング |
| 運営・予算 | #ffccbc | 運営/ファイナンス |

### アクセントカラー
- `var(--accent)` = purple — ツールバー背景、選択リング、primary ボタン

### ボタン系統
- ghost: `#fff` + box-shadow（補助操作）
- primary: accent purple（主要アクション）
- danger: `#e74c3c`（注意・更新通知）
- 共通: height 34px / border-radius 999px / font 13px bold

### deck 構造
```
#deck (fixed, top:10px)
├── #deck-desc (タイトル・ズーム%・syncstate)
└── #deck-cmd
    ├── #deck-menu (DECK_MENU配列から描画)
    ├── #legend.deck-pop (🎨 popover)
    │   └── .pop-body: chips + sizeslider + themeslider + ambient
    └── #updatepill.btn-danger (他デバイス更新通知)
```

## 既知の修正待ち課題

### 🔴 必須修正
1. **pop-body 全幅問題**: `.deck-pop .pop-body` に `max-width: min(92vw, 400px)` 追加
2. **updatepill 初期表示**: `style="display:none"` に変更（checkRemote で heデバイス更新検知時のみ表示）

### 🟡 推奨改善
3. `.item` に `cursor:grab` 追加
4. fitView 復活（「全体表示」ボタンを popover 内に）
5. テーマバーステータス表示（未選択時の themeIdx ドット）

### 🟢 任意改善
6. スマホで desc 区画を折りたたみ可能に
7. ホバー時のフィードバック強化（画像アイテム）

## 操作フロー
1. index.html を編集
2. `sed -n '/^<script>/,/^<\/script>/p' index.html | sed '1d;$d' > /tmp/opencode/boardN.js && node --check` で構文確認
3. `cd ~/repos/idol-oshare/site && npx -y vercel deploy --prod --yes` でデプロイ
4. Playwright で検証（ページエラーなし、UI動作確認）
5. `git add -A && git commit && git push` でコミット

## 注意点
- デプロイは **Vercel のみ**（surge は更新しない）
- API (`/api/board`) に `Cache-Control: no-store` 設定済み（Edge キャッシュ対策）
- always-auto sync: `flushSave()` → 1.5秒後に `cloudPush(false)` 自動実行
- スライダー: 未選択時は新規メモのデフォルト値（size:190, theme:themeIdx）
- 選択モデル: `sel` 変数 + `.item.selected` クラス + `syncSliders()`
