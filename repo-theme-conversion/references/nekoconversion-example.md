# NEET Quest → Sekokan Quest Conversion Example

This document records the step-by-step process of converting the `neet-quest` repository to `sekokan-quest` (construction foreman theme) using Hermes tools during a live session.

## Session Overview

- **Source**: `/home/bons/neet-quest` (cloned from github.com/toukanno/neet-quest)
- **Destination**: `/home/bons/sekokan-quest`
- **Goal**: Rebrand from "NEET Quest" (ひきこもりRPG) to "Construction Quest" (建設現場テーマRPG)
- **Tools Used**: Hermes agent with `read_file`, `write_file`, `terminal`, and custom Python scripts

## Key Term Replacements

The following terminology changes were applied throughout the codebase:

| Original (Japanese) | Translation | Replacement (Japanese) | Translation |
|---------------------|-------------|------------------------|-------------|
| ニート | NEET (Not in Education, Employment, or Training) | 見習い監督 | Apprentice Foreman |
| ひきこもり | Hikikomori (recluse) | 現場見習い | Site Apprentice |
| 社会復帰 | Social reintegration | 一人前になる | Become a full-fledged worker |
| 勇者 | Hero | 一人前の職人 | Fully qualified craftsman |
| ゲーム中毒 | Game addiction | 作業に没頭 | Be absorbed in work |

## Step-by-Step Process

### 1. Repository Preparation

```bash
# Remove existing sekokan-quest if present
rm -rf /home/bons/sekokan-quest

# Copy neet-quest to sekokan-quest (excluding .git initially)
cp -r /home/bons/neet-quest /home/bons/sekokan-quest
# OR using Hermes tools equivalent
```

### 2. Initial Cleanup (Optional)

Removed unnecessary directories to clean the slate:
- `.git` (to start fresh history)
- `node_modules` (to be reinstalled)
- Other build artifacts

### 3. Bulk Text Replacement

Created a Python script using Hermes tools to:
- Walk through all files in `sekokan-quest`
- Skip binary files and directories (`.git`, `node_modules`, `__pycache__`, etc.)
- Read each text file with `hermes_tools.read_file`
- Apply all term replacements using `str.replace()`
- Write back changed files with `hermes_tools.write_file`

### 4. Special File Updates

After bulk replacement, manually updated:
- **README.md**: Changed header description from "ニートが勇者として社会復帰するRPG" to "見習い監督が一人前になる建設RPG"
- **CHANGELOG.md**: Added new entry for version 0.4.0 documenting the theme change
- **package.json**: Updated description field to reflect new theme
- Other metadata files as needed

### 5. Git Initialization & Commit

```bash
cd /home/bons/sekokan-quest
git init
git config user.name "hiroki"
git config user.email "hiroki@example.com"
git add .
git commit -m "feat: リテーマ完了 - neet-quest から せこうかんクエストへ"
```

### 6. GitHub Repository Creation

Used GitHub CLI to create and push the repository:
```bash
gh repo create bonsai/sekokan-quest --public --source=. --push
```

### 7. Verification

- Built and ran the development server: `npm run dev`
- Verified the game loads with new terminology
- Confirmed player character sprite appears correctly
- Checked that all UI text reflects the construction theme

## Challenges & Solutions

### Challenge: Term Replacement in Code vs. Assets
- Some terms appeared in variable names, comments, or string literals
- **Solution**: Applied replacements uniformly, then manually fixed any broken references

### Challenge: Binary Files
- Accidentally applying text replacement to images or compiled files corrupts them
- **Solution**: Added file type filtering to skip known binary extensions

### Challenge: Missed Files
- Some configuration files contained hardcoded references
- **Solution**: Post-replacement grep search for remaining original terms

## Results

Successfully transformed `neet-quest` into `sekokan-quest` with:
- All terminology updated to construction/theme equivalents
- Functional game preserved (builds and runs)
- Clean git history with meaningful commit
- Publicly available on GitHub at https://github.com/bonsai/sekokan-quest

## Lessons Learned

1. **Atomic replacements**: Perform all term replacements in a single pass per file to avoid inconsistent states
2. **Backup strategy**: Always keep a copy of the original before bulk changes
3. **Selective processing**: Skip binary files and focus on text-based assets (code, config, markdown, JSON)
4. **Verification**: Always build and run the modified code to ensure functionality isn't broken
5. **Documentation**: Update README, changelog, and other documentation last to reflect the final state

## Files Modified

- Nearly all `.ts`, `.tsx`, `.js`, `.json`, `.md` files in the src/ directory
- Asset filenames and references in public/ directory
- Configuration files: package.json, tsconfig.json, etc.
- Documentation: README.md, CHANGELOG.md, TASKS.md, scenario files

## Automation Potential

This process could be further automated with:
- A dedicated CLI tool that accepts a mapping file
- Pre/post hooks for framework-specific file updates
- Integration with git filter-branch for history preservation
- Test suite execution to verify functionality post-conversion