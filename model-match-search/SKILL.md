---
name: model-match-search
description: このPCのスペックに合うAIモデル（動画生成/画像生成/LLM）を探す。PCの統計を収集し、モデルの要求スペックと照合して「このPCで動く/動かない」を判定する。Use when the user asks to find models their PC can run, このPCでもできるモデル, モデルマッチ, スペックに合うモデル, can this PC run X, model match search.
license: MIT
---

# Model Match Search

このPCのスペックを収集し、ローカル実行可能なAIモデルを判定するスキル。

## Step 1: PC統計の収集

以下を実行してスペックを集める。

```bash
nvidia-smi 2>/dev/null || echo "GPU_NONE"
free -h
df -h / | tail -1
nproc
grep -E "^(model name)" /proc/cpuinfo | sort -u
ls /dev/dri 2>/dev/null || echo "no_dri"
grep -i microsoft /proc/version 2>/dev/null && echo "(WSL2)"
```

判定ポイント:
- GPU: `nvidia-smi` あり → VRAM確認 / `no_dri`+`GPU_NONE` → **CPUのみ推論**
- RAM: `MemTotal` が実質メモリ上限
- WSL2の場合はWindows側GPUパススルーなし→CPU扱い

## Step 2: モデル要求スペックとの照合

| モデル | 種別 | 必要VRAM | 必要RAM | 備考 |
|---|---|---|---|---|
| LTX-2.3 (動画+音声) | 動画生成 | 12GB+ | 32GB | GPU必須。GGUF量子化でもRAMが足りない |
| Wan2.2 (動画) | 動画生成 | 12GB+ | 32GB | GPU必須 |
| MiniMax H3 (動画+音声) | 動画生成 | 16GB+ | 32GB | GPU必須 |
| Stable Diffusion 1.5 | 画像生成 | 4GB | 8GB | CPUのみは実用不可 |
| SDXL | 画像生成 | 8GB | 16GB | CPUのみは実用不可 |
| Flux (schnell/dev) | 画像生成 | 8GB+ (fp8) | 16GB | CPUのみは実用不可 |
| Z-Image-Turbo / ERNIE-Image | 画像生成 | 8GB+ | 16GB | GPU必須 |
| Anima | 画像生成 | 8GB+ | 16GB | GPU必須 |
| Qwen3-4B Q4_K_M | LLM | なし(CPU可) | 4GB | **CPU推論OK** |
| Qwen3-8B Q4_K_M | LLM | なし(CPU可) | 7GB | RAM6GBでは厳しい |
| Gemma3-4B Q4 | LLM | なし(CPU可) | 4GB | **CPU推論OK** |
| Phi-4-mini | LLM | なし(CPU可) | 4GB | **CPU推論OK** |
| Qwen2.5-VL-3B | マルチモーダル | なし(CPU可) | 5GB | **CPU推論OK** |

## Step 3: 判定と出力

以下の優先順位で判定する。

1. **GPUなし・RAM<8GB の場合**
   - 動画/画像生成系(上記表の全GPUモデル) → 「不可」と明記
   - 代替として小規模LLM (4B以下Q4量子化, llama.cpp/Ollama) を提示
2. **GPUあり・VRAM/RAM満たす場合**
   - 表の要求を満たすモデルを「可」と明記
3. **クラウド代替を提示**
   - ローカル不可の場合は Azure/クラウドGPU や、GPU搭載PCでの実行を案内

## Step 4: 出力フォーマット

```
### PC統計
- CPU: <model name> (<cores>/<threads>)
- RAM: <MemTotal>
- GPU: <VRAM or なし(CPUのみ)>
- ストレージ空き: <avail>

### 判定
- <モデル名>: 可 / 不可 (理由)
- おすすめ実行可能モデル: <model> (llama.cpp/Ollama)
```

## 注意
- ユーザーの質問が特定モデル(例: LTX-2.3)のときは、そのモデルが中心になるよう照合すること。
- 実測が信頼第一。表の値は目安であり、量子化バージョンや設定により変動する。
- 必要に応じて websearch で最新モデルの要求スペックを確認すること。
