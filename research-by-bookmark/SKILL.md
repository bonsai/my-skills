---
name: research-by-bookmark
description: Use when the user asks to analyze bookmarks, extract research interests, organize bookmarks, find research directions from bookmarks, ブックマーク分析, ブックマーク整理, リサーチ方向, bookmark research, or wants to understand their interests from saved links. Covers Edge bookmark export → HTML parse → categorization → research direction proposal.
license: MIT
---

# research-by-bookmark — ブックマークからリサーチ方向を導く

ブラウザのブックマークを解析し、ユーザーの関心領域名を可視化して
リサーチの方向性を提案するスキル。

## Path

- **リポジトリ**: `/home/bons/repos/bookmark-parser`
- **ブックマーク保存先**: `~/wiki/bookmarks/`
- **エクスポートスクリプト**: `~/bin/fav.ps1`（PowerShell / Windows側で実行）

## コマンド

```bash
cd /home/bons/repos/bookmark-parser

# パース（ブックマークHTML → JSON）
npx tsx src/index.ts [input.html] [output_dir]

# 関心空間マップ生成（レコメンド付き）
npx tsx src/recommend.ts [--query "テーマ"] [--dir ~/wiki/bookmarks]

# テーマフィルタ
npx tsx src/recommend.ts --query "AI"
```

## 実行手順

### 1. ブックマークの入手

既存のブックマークHTMLがあれば `~/wiki/bookmarks/` から探す。
無ければエクスポートを案内する：

```powershell
# Windows PowerShell で実行
powershell -ExecutionPolicy Bypass -File \\wsl.localhost\Ubuntu\home\bons\bin\fav.ps1 -Output \\wsl.localhost\Ubuntu\home\bons\wiki\bookmarks\edge-bookmarks.html
```

### 2. パース + レコメンド

```bash
cd /home/bons/repos/bookmark-parser

# Step 1: パース
npx tsx src/index.ts ~/wiki/bookmarks/edge-bookmarks.html ~/wiki/bookmarks/

# Step 2: 関心空間マップ生成
npx tsx src/recommend.ts --dir ~/wiki/bookmarks/
```

### 3. 特定テーマに焦点を当てる

```bash
npx tsx src/recommend.ts --query "AI" --dir ~/wiki/bookmarks/
```

## 出力ファイル

| ファイル | 内容 |
|---------|------|
| `~/wiki/bookmarks/bookmarks.json` | 全ブックマーク（URL+タイトル+フォルダ） |
| `~/wiki/bookmarks/domains.json` | ドメイン別件数ランキング |
| `~/wiki/bookmarks/keywords.json` | キーワード頻度ランキング |
| `~/wiki/bookmarks/research-analysis.md` | 関心空間マップ＋レコメンド |

## 関心クラスタテーマ

- AI / ML / LLM
- Programming Languages
- Web Development
- Data & Infrastructure
- Game Development
- Music & Audio
- Design & UX
- Academic & Research
- Developer Tools
- Mobile Development

## 注意事項

- ブックマークHTMLはNetscape Bookmark File形式（Edgeエクスポート）
- レコメンドはキーワードベースの決定論的クラスタリング（LLM不要）
- Mastra版（`src/mastra/`）はAPIキーがあればLLM深掘り分析が可能
