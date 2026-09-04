---
name: bonsai-pruner
description: Use when the user asks to prune, trim, slim down, clean up, or reduce code. Front-load keywords: pruner, 削ぎ落とす, プルーニング, dead code, unused, trim, slim, simplify, 簡素化, 整理, cut, reduce. Covers dead code removal, unused imports cleanup, logic simplification, duplication elimination, and dependency trimming.
---

# bonsai-pruner — コード削ぎ落とし

不要なコードを切り落とし、コードベースを軽量・健全に保つ。

## Phase 0: 現状把握

対象ディレクトリの構造を把握する:
1. `ls` / glob でファイル一覧を取得
2. 各ファイルの行数・サイズを確認
3. 言語・フレームワーク・ビルドツールを特定
4. テスト・lintコマンドを確認（`package.json`, `Makefile`, `pyproject.toml` 等）

## Phase 1: 切除対象の特定

以下の観点で削除候補を洗い出す:

| カテゴリ | 検出手法 |
|---------|---------|
| 未使用import | `grep` でimport文を列挙 → 実使用箇所を検索（0件 = 削除対象） |
| 未使用変数/関数 | 同上。シンボルの定義箇所 vs 参照箇所を比較 |
| コメントアウトコード | 連続コメントブロック（3行以上）を検出 |
| 死コード分岐 | 到達不能な `if/else`、`return` 後のコード |
| 重複コード | 類似関数・コピペパターンを検出 |
| 不要な依存 | `package.json` / `requirements.txt` の各パッケージがインポートされているか確認 |
| 未使用ファイル | どのファイルからもimport/requireされていないファイル |

## Phase 2: 安全な切除

切除は以下の順序で行う:

1. **コメントアウト削除** — 最もリスクが低い。一括削除。
2. **未使用import削除** — ソート済みimportリストから該当行を除去。
3. **未使用変数/関数削除** — 定義と全参照を確認してから除去。
4. **重複コード統合** — 重複関数を共通化し、元の関数を除去。
5. **死コード分岐削除** — 到達不能ブロックを除去し、条件式を簡素化。
6. **未使用ファイル削除** — 他から参照されていないファイルを削除。
7. **依存パッケージ削除** — 削除したimportに伴い、不要になったパッケージを除去。

**各フェーズ後にビルド/テストを実行し、壊れていないことを確認する。**

## Phase 3: 検証

```bash
# ビルド確認
npm run build  # or cargo build, go build 等

# テスト確認
npm test       # or pytest, cargo test 等

# lint確認
npm run lint   # or ruff, golangci-lint 等
```

失敗した場合は Phase 2 の該当ステップをロールバックして再検討。

## Phase 4: レポート

完了後、以下をユーザーに返す:
- **削除ファイル数**・**削除行数**
- **主要な削除内容**（カテゴリ別に箇条書き）
- **変更前後のファイルサイズ比較**（対象ファイルが少ない場合のみ）

## コンパイル型言語の場合（Rust/Go/Java）

- `unused_imports` warning を lint設定から拾う
- コンパイラwarningが出なくなるまで除去を進める
- `cargo fix --allow-dirty` 等の自動修正ツールを活用

## 注意

- 削除前に必ずgit statusを確認し、クリーンな状態にしておく（必要ならWIPコミット）
- 削除は段階的に行う。一括で全部消すのは避ける
- フレームワークの约定に従う（例: Reactの`memo`、Next.jsの`server`/`client`Directive等は残す）
- 型安全性を損なう削除は避ける（`any`への退化、型アノテーション削除等）
- パブリックAPIのシグネチャは削除しない（外部依存がある可能性）
