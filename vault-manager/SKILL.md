---
name: vault-manager
description: 暗号化バックアップ(vault)と秘密鍵のUSB持ち出し管理。Use ONLY when the user asks to バックアップ/vault/暗号化/復元/USB持ち出し/secrets.env/GPG鍵/vault-backup. Covers bonsai/vault private repo backup, usb-kit creation, restore steps.
---

# vault-manager — 暗号化バックアップ & USB持ち出し管理

GPG(RSA4096 FP: `773210E199F4BDBCED39BEA02B3A7DE536CBDABB` / bons-vault)で
資産と設定を暗号化し、プライベートリポジトリ `bonsai/vault` と USB に退避する。

## 構成

| 対象 | 場所 |
|---|---|
| 統合シークレット | `~/.secrets.env` (600, 平文・ローカルのみ) |
| ローカル資産(鍵/DB/画像) | `~/.repos-local-assets/` (700) |
| クラウド退避先 | `bonsai/vault` private repo ↔ `~/.vault-work/` |
| USB持ち出しセット | `~/usb-kit/` |
| 管理ルール | `~/sync-repos/docs/secret-rules.md` |

## 操作

### 1. バックアップ更新（クラウドへ）
```bash
bash ~/sync-repos/scripts/vault-backup.sh
```
tar.gz → GPG暗号化 → commit&push。node_modules等の再生成物は含まれない。

### 2. USB持ち出しキット作成
```bash
mkdir -p ~/usb-kit && chmod 700 ~/usb-kit && cd ~/usb-kit
gpg -a --export-secret-keys bons-vault > bons-vault-SK.asc
gpg -a --export bons-vault > bons-vault-pub.asc
cp ~/.vault-work/vault-latest.tar.gz.gpg .
```
USB挿入後 `cp -r ~/usb-kit /mnt/<drive>/`。
**SK.asc はパスフレーズ無しで書き出されるため、持ち出す前に
`gpg --edit-key <FP> passwd` で設定して作り直すことを推奨。**

### 3. 復元
```bash
gpg --import bons-vault-SK.asc
gpg -qd vault-latest.tar.gz.gpg | tar xzf -
```

## 鉄則（secret-rules.md 7ヶ条より）
- 秘密の値は**表示しない**（キー名のみ出力可）
- 平文の常設置き場を作らない／クラウドへは暗号化済みアーカイブのみ
- 新規キー入手→24h以内に vault へ
