---
name: vanilla-web-dev
description: "フレームワークなし（Vanilla）のTypeScript Web開発スキル。関数型アーキテクチャ（immutable state + reducer + pure render）、Canvas 2D、MediaPipe連携、PWA対応の設計指針。Viteのみでビルド。React/Vue/Svelte不使用。"
license: MIT
---

# Vanilla Web Dev スキル

## いつ使うか

- フレームワーク不要な小規模Webアプリ（< 1000 lines）
- Canvas 2D / WebGL / rAF ループが中心のプロジェクト
- バンドルサイズ < 50KB に収めたい
- 関数型原則（immutable, pure, reducer）で書きたい
- MediaPipe / getUserMedia などブラウザネイティブAPIを直で使う
- PWA（オフライン対応）が必要

## 基本原則

### 禁止
- 状態の直接変更（mutation）
- class / this / prototype
- 描画関数内でのDOM操作
- 描画・還元関数内での乱数・時刻取得
- Side effect を純粋関数内に混入

### 必須
- Immutable update: spread で新規オブジェクト生成
- Pure function: 同じ入力 → 同じ出力
- Discriminated union: Action 型でイベント分岐
- Reducer pattern: `(state, action) => newState`
- Pure render: `draw(context, state) => void`
- Side effect は entry point（main.ts）のみ

## ファイル構成指針

```
project/
├── index.html              # <script type="module">
├── src/
│   ├── main.ts             # entry: init + loop + side effects
│   ├── state.ts            # State type, Action type, reducer, createState
│   ├── camera.ts           # MediaPipe HandLandmarker 初期化・検出
│   ├── ttl.ts              # TTL parser, pure
│   ├── turtle.ts           # Logo engine, pure
│   ├── trace.ts            # Trace buffer 管理, pure
│   ├── render.ts           # Canvas draw, pure
│   ├── export.ts           # G-code / DXF / JSON / TTL string builders, pure
│   └── style.css           # minimal
├── vite.config.ts          # base, build output
├── package.json            # vite, typescript のみ
└── dist/                   # build output
```

## アーキテクチャ指針

### State設計
- 全て Readonly（深い readonly は lib で補助）
- 配列・オブジェクトは spread でコピー
- 履歴がほしいケースは配列に蓄積

### Reducer設計
- Action は `{ type: string }` を持つ discriminated union
- switch/case で分岐。default は state をそのまま返す
- 複数更新は Action 配列を reduce で畳み込む

### Render設計
- Canvas 2D API を直接使用
- 入力は state のみ。グローバル参照禁止
- 毎フレーム clearRect → 全要素再描画（・1000行以下なら問題にならない）

### 副作用の分離
- camera.ts: MediaPipe 初期化・検出のみ
- entry point: requestAnimationFrame, addEventListener, download, localStorage
- それ以外のファイルは pure

### PWA指針
- マニフェスト: standalone, theme-color, viewport fix
- Service Worker: index.html は network-first（常に最新）
- 静的アセット: cache-first

### Vite指針
- base: サブディレクトリ配信用に設定
- assetsDir: ハッシュ付きJS/CSS出力先
- plugin: wasm/react/vue/svelte 不使用

## 依存指針

### 入れるもの
- Vite（ビルド・HMR）
- TypeScript（型チェック）
- MediaPipe tasks-vision（手追跡、CDN読み込み可）

### 入れないもの
- React / Vue / Svelte / Solid / Angular
- State management library（Redux, Pinia, etc.）
- UI component library
- Router（単一ページ想定）
- Animation library（rAF で自前）

## デバッグ指針

- Reducer の結果を JSON 文字列化して比較（prev !== next）
- Canvas に state 概要を描画して可視化
- Chrome DevTools Overrides で Service Worker 無効化
- 履歴配列で time-travel デバッグ

## 拡張指針

### Local storage 永続化
- entry point で load → initialState に反映
- 特定 Action 後に save（debounce）

### Web Worker 移行
- MediaPipe 処理を Worker に移す場合:
  - Worker は副作用許容
  - 結果を Action として main スレッドへ postMessage

### Export module 追加
- 新しいフォーマット追加は pure function を1つ追加するだけ
- 副作用（download）は entry point に委譲

---

*Created for kamera — "カメラ→軌跡→亀→Fab"*
