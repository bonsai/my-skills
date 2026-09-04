---
name: repo-theme-conversion
description: Rebrand a codebase by replacing terminology and updating metadata. Use when the user wants to retheme/replace terms in a project (e.g., NEET Quest → Construction Quest). Keywords: retheme, rebrand, リテーマ, テーマ変更, 置換, replace terms, bulk rename, theme conversion.
---

# Repo Theme Conversion

Convert a project's theme by replacing terminology across all text files, updating metadata, and preserving functionality.

## When to Use

- User wants to change a project's theme/setting (e.g., game retheme)
- Transformation is primarily textual (code, config, docs)
- Source repo is available locally

## Steps

### 1. Prepare working copy

```bash
cp -r /path/to/source /path/to/destination
# or clone fresh
```

Exclude `.git`, `node_modules`, `dist`, `build`, `__pycache__`, binaries.

### 2. Define replacement mapping

Create a dictionary of old→new strings. Include case variants if needed.

Example (NEET → Construction):
```
ニート → 見習い監督
ひきこもり → 現場見習い
社会復帰 → 一人前になる
勇者 → 一人前の職人
ゲーム中毒 → 作業に没頭
```

### 3. Apply bulk replacements

Use `grep` to find files containing old terms, then `read` + `write` or `edit` to replace. Use `replaceAll` in `edit` tool for efficiency.

Walk through all text files, skip binaries (check `file` command or extension).

### 4. Update specific files

After bulk replace, manually update:
- `README.md` – project description, header
- `package.json` – name, description
- `public/manifest.json` – name, short_name, description
- `CHANGELOG.md` – add entry for theme change
- Hardcoded URLs/paths referencing old theme

### 5. Version control

```bash
git init
git add .
git commit -m "feat: retheme from <OLD> to <NEW>"
git remote add origin <URL>
git push -u origin main
```

### 6. Verify

```bash
npm install && npm run build
npm run dev  # or equivalent
```

Use browser tools to confirm UI reflects new theme.

### 7. Clean up

Remove temporary scripts. Ensure only intended files remain.

## opencode Tools Mapping

| Task | opencode Tool |
|------|--------------|
| Read files | `read` tool |
| Write files | `write` tool |
| Edit/replace | `edit` (with `replaceAll`) |
| Search for terms | `grep` tool |
| Find files | `glob` tool |
| Commands (git, npm, cp) | `bash` tool |
| Web verification | `playwright_browser_*` tools |

## Pitfalls

- **Binary files**: Check extension or use `file` command before editing
- **Over-replacement**: Short strings may appear inside other words; review changes
- **Missed files**: Search for old terms after replacement (`grep -r "oldterm" .`)
- **History**: Without `.git`, history is lost. Use `git filter-repo` if history matters
- **Line endings**: Ensure consistent LF/CRLF on cross-platform projects

## Example

See `references/nekoconversion-example.md` for the full NEET→Sekokan conversion transcript.
