# tdd-vitest — テスト先行実装(vitest)

リファクタ・修正・新機能を red→green→refactor で進める。

## 発動
- 「テスト先行で」「vitestで」「TDDで」「リファクタして」

## 手順
1. テスト可能な境界を確認: 純関数(ロジック)を分離し、DOM/Network/Audio等はモック or ラッパー化
2. 期待値をテストに書く(red)→ 最小実装(green)→ リファクタ
3. 実行: `npm run test` / `npm run typecheck` / `npm run build`
4. 既存データ互換は fixture 回帰(同一入力→同一出力)で担保

## 規約
- テスト対象優先: 純関数 > 状態遷移 > コンポーネント > 実環境スモーク
- 完了宣言にはテスト緑+型検査+build OK の証拠
