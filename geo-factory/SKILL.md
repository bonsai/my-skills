---
name: geo-factory
description: 幾何学的アニメーション動画を生成して再生する。mediapipe風顔メッシュ、幾何学スイッチング、変顔アニメーション。keywords: 幾何学, geo, facemesh, 顔, 変顔, animation, 動画生成, geometric
---

# Geo Factory

幾何学的アニメーションMP4を生成し、WSLパスを出力する。

## 生成タイプ

### 1. 顔メッシュ変顔 (`facemesh.py`)
- MediaPipe風の468点3D顔メッシュ
- 7表情を補間して変顔アニメーション
- 3D回転付き

### 2. 幾何学スイッチング (`geometric_mystery.py`)
- 6〜12角形がmorphして切り替わる
- パレット4色セットで自動切替
- リング＋パーティクル演出

## 使い方

```bash
# 顔メッシュ
python facemesh.py

# 幾何学スイッチング
python geometric_mystery.py

# カスタム（短縮）
python geometric_mystery.py  # DURATION=10に変更可
```

## 出力

WSLフルパスが出力される:
```
output: /home/bons/wiki/projects/shorts-factory/facemesh.mp4
```

## 再生

```bash
explorer.exe $(wslpath -w <output_path>)
```

## パラメータ（geometric_mystery.py）

ファイル先頭の定数を変更:
- `W, H` — 解像度（デフォルト1080x1920 縦型）
- `FPS` — フレームレート（デフォルト30）
- `DURATION` — 秒数（デフォルト30）

## パラメータ（facemesh.py）

- `FPS` — フレームレート（デフォルト30）
- `DURATION` — 秒数（デフォルト10）
- `EXPRESSIONS` — 表情リスト（7種類）
