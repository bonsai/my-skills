---
name: daihon
description: Use ONLY when the user asks to generate a comedy routine (漫才/ネタ) as an MP3 via the daihon pipeline at /home/bons/daihon. Front-load keywords: 漫才, ネタ, お笑い, コメディ, MP3, 音声, 芸人, ボケ, ツッコミ, daihon, comedy, routine. Natural-language requests like 「ラーメンの漫才MP3を作って」 trigger this. Covers ネタ生成 → 予選 → 本戦 → TTS → MP3出力.
---

# daihon — 漫才MP3生成

バーチャルコメディアン制作システム。自然言語のお題から漫才ネタを生成し、
観客エージェントによる予選・本戦を経て、優勝ネタを音声（MP3）にする。

## Project Info

- **Path**: `/home/bons/daihon`
- **Python**: `.venv/bin/python`（LangChain入り / ルールベース評価用）
- **TTS**: edge-tts（`/usr/bin/python3` のグローバルにあり、venv実行時は自動切替）
- **お題素材**: `data/themes/*.txt`
- **出力**: `output/stories/<お題>/`（`tts.txt` / `<お題>-<時刻>.mp3` / `summary.json` / `youtube-meta.json`）
- **設定**: `config/`（芸人5人・観客6人・採点13因子・LLM/進化）

## 実行手順

1. **お題を決める** — ユーザーの自然言語からお題を抽出。不明なら「お題は何ですか？」と聞く。
   既存素材がある場合（`data/themes/*.txt`）はそれを使う。

2. **ネタ本文を作る** — `data/themes/<お題>.txt` を新規作成（無ければ）：
   - 漫才スタイルの話し言葉で書く（ボケ→ツッコミ、オチ付き）
   - 現実の商品名・人名・団体名は使わない（フェイク名に置換）
   - 既にファイルがある場合はそのまま使う

3. **パイプライン実行**:
   ```bash
   cd /home/bons/daihon && .venv/bin/python src/production/pipeline.py \
     --file data/themes/<お題>.txt --topic "<お題>"
   ```

4. **結果を返す** — 以下をユーザーに提示:
   - MP3パス: `output/stories/<お題>/<お題>-<時刻>.mp3`
   - 優勝芸人・得点（`summary.json`）
   - MP3がWindowsから開けるパス: `\\wsl.localhost\Ubuntu\home\bons\daihon\output\stories\<お題>\<お題>-<時刻>.mp3`

## 便利コマンド

```bash
# 最新story一覧
ls -lt /home/bons/daihon/output/stories/

# 特定のお題のサマリ確認
cat "/home/bons/daihon/output/stories/<お題>/summary.json"

# 進化ループ（芸人パラメータ最適化。LLM不可時は--rule）
.venv/bin/python /home/bons/daihon/scripts/evolve.py --topic "<お題>" --generations 5 --rule
```

## 注意

- 実行は必ず `cd /home/bons/daihon` してから（相対importのため）
- パイプライン実行は数十秒〜2分（予選・本戦＋TTS）。タイムアウトに注意
- TTS失敗時はグローバルpythonを明示: `python3 -m edge_tts --voice ja-JP-NanamiNeural --file data/scripts/title-standup-tts.txt --write-media output/stories/<お題>/<お題>.mp3`
- LLMキー失効中はルールベース評価で動作する（`--rule` 不要、自動フォールバック）
