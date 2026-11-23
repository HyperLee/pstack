# macOS 版 pstack Skills 專案安裝教學

這份教學使用 pstack 的 `main` 分支，在 macOS 終端機示範如何將 skills 安裝到指定專案。安裝範圍是該專案，Codex 選單仍可能顯示既有的個人或系統技能。

- **第一次安裝**依序完成第 1～5 節。
- **檢查已有的安裝**可直接用第 4 節的唯讀指令，再依第 5 節確認 Codex 能選取技能。
- **手上已有安裝好的專案**可依第 6 節把同一版本裝到另一個專案。

## 1. 準備工具與兩個路徑

需要 **Python 3.9 以上**、Git，以及支援 skills 的 Codex 桌面 App 或 CLI。下列安裝指令可在 macOS 的 zsh 或 Bash 執行。目標位置須可用一般使用者權限寫入，並支援符號連結。使用桌面 App 時，第 5 節的 `codex` 命令可以略過。

```bash
python3 --version
git --version
```

以下路徑是範例。將變數換成自己的路徑，並在同一個終端機視窗完成後續步驟。

| 角色 | 範例路徑 | 用途 |
| --- | --- | --- |
| 安裝來源 | `$HOME/Projects/pstack` | pstack 的 `main` checkout，內含完整套件與安裝器 |
| 目標專案 | `$HOME/Projects/SkillsTestProj` | 要在 Codex 開啟的專案根目錄 |

```bash
PSTACK_SOURCE="$HOME/Projects/pstack"
PSTACK_TARGET="$HOME/Projects/SkillsTestProj"
```

第一次取得 pstack 時，將 `main` 分支下載到上述來源路徑。已下載的讀者可以直接執行下一段檢查。

```bash
git clone --branch main https://github.com/HyperLee/pstack.git "$PSTACK_SOURCE"
```

```bash
git -C "$PSTACK_SOURCE" branch --show-current
test -d "$PSTACK_TARGET" && printf '目標專案目錄存在\n'
```

確認第一行為 `main`，且終端機印出「目標專案目錄存在」後再繼續。如果分支不同，先執行 `git -C "$PSTACK_SOURCE" status --short` 確認工作目錄的修改。請將目標指到專案根目錄，例如包含 `.csproj`、`package.json` 或專案 README 的那一層。路徑兩側的引號可以保留空白和中文。

## 2. 先預覽，再正式安裝

先執行預覽。安裝器會檢查目標位置並列出待建立的連結，這個步驟只讀取檔案。

```bash
python3 "$PSTACK_SOURCE/scripts/install-skills.py" --project "$PSTACK_TARGET" --dry-run
```

全新專案的第一行預期為 `Would create 58 skill links`。完整且與來源一致的安裝會顯示 `Would create 0 skill links`。如果顯示 `Existing content differs; nothing changed`，請先檢視列出的路徑，確認是同名技能、舊版本套件，還是專案自己的修改，再決定如何處理。

預覽沒有錯誤後，執行正式安裝。安裝器會建立需要的目錄。

```bash
python3 "$PSTACK_SOURCE/scripts/install-skills.py" --project "$PSTACK_TARGET"
```

全新專案預期顯示 `Created 58 skill links`。完整的同版本安裝重跑時會顯示 `Created 0 skill links`。

## 3. 看懂安裝後的目錄

```text
SkillsTestProj/
├── .agents/
│   └── skills/
│       ├── poteto-mode -> ../../.codex/pstack/skills/poteto-mode
│       ├── poteto-help -> ../../.codex/pstack/skills/poteto-help
│       └── 其他技能連結
├── .codex/
│   └── pstack/
│       ├── LICENSE
│       ├── skills/
│       │   └── poteto-mode/
│       │       └── SKILL.md
│       ├── docs/guide/README.md
│       └── scripts/install-skills.py
└── 專案自己的檔案
```

Codex 從 `.agents/skills/` 探索技能，再沿著連結讀取 `.codex/pstack/skills/` 的內容。指南、共用參考資料與腳本一起保存在 `.codex/pstack/`。連結以所在位置為基準，因此搬移整個專案後，仍會指向該專案內的套件。這份套件是安裝當時的快照，來源 checkout 的後續變動要另外比對。

## 4. 唯讀驗證指定專案

這一節會沿用已設定的 `PSTACK_TARGET`。若從新的終端機開始，會使用下方的範例路徑，請按實際專案根目錄調整。

```bash
: "${PSTACK_TARGET:=$HOME/Projects/SkillsTestProj}"
printf '正在檢查 %s\n' "$PSTACK_TARGET"
readlink "$PSTACK_TARGET/.agents/skills/poteto-mode"
```

預期印出 `../../.codex/pstack/skills/poteto-mode`。接著確認指南、安裝器與所有 pstack 連結。這段只檢查套件內列出的技能，同一專案的其他技能可以共存。

```bash
python3 - "$PSTACK_TARGET" <<'PY'
import os
from pathlib import Path
import sys

project = Path(sys.argv[1]).resolve()
bundle = project / ".codex/pstack"
if bundle.resolve() != bundle:
    sys.exit(f"套件位置應在專案內：{bundle}")

for required in ("docs/guide/README.md", "scripts/install-skills.py"):
    if not (bundle / required).is_file():
        sys.exit(f"缺少必要檔案：{bundle / required}")

skills = sorted((bundle / "skills").glob("*/SKILL.md"))
if len(skills) != 58:
    sys.exit(f"預期套件內有 58 個技能，實際找到 {len(skills)} 個")

for skill in skills:
    link = project / ".agents/skills" / skill.parent.name
    if not link.is_symlink() or Path(os.readlink(link)).is_absolute():
        sys.exit(f"缺少相對符號連結：{link}")
    if (link / "SKILL.md").resolve() != skill or not skill.is_file():
        sys.exit(f"連結未指向套件內可讀取的技能：{link}")

print(f"已確認 58 個技能連結都指向 {bundle}")
PY
```

若要比對來源版本，再用第 2 節的 `--dry-run`。預期顯示 `Would create 0 skill links`。來源較新時，即使已安裝版本運作正常，套件內容差異仍會被列為衝突。

## 5. 在 Codex 選取技能

- **桌面 App**開啟 `PSTACK_TARGET` 指定的專案根目錄，在該專案建立新聊天，再從技能選擇介面加入 `poteto-help` 或 `poteto-mode`。
- **CLI**從目標專案啟動。進入 Codex 後，可使用 `/skills` 或輸入 `$` 選取技能。參考 [Codex 官方 Skills 文件](https://learn.chatgpt.com/docs/build-skills)。

```bash
(cd "$PSTACK_TARGET" && codex)
```

把下列任一範例貼到 **Codex 聊天**。

```text
$poteto-help 請介紹這個專案可用的 pstack skills，並說明我可以從哪個技能開始。
```

```text
$poteto-mode 請唯讀檢視這個專案，整理主要目錄、如何啟動，以及現有測試的執行方式。
```

若要調整模型繼承或 worker 數，可另外執行 `$setup-pstack`。基本使用可以沿用預設值。若技能未出現在選單，先確認 Codex 開啟的是目標專案，接著開新聊天或重新啟動 Codex。同名技能出現兩份時，請選取專案範圍的那份。

## 6. 從已有的安裝重用同一版本

若手上已有安裝完整的 macOS 專案，可以直接使用其中的安裝器。安裝器會取用該專案的套件快照，並在新專案建立自己的相對連結。

```bash
PSTACK_TEMPLATE="$HOME/Projects/SkillsTestProj"
PSTACK_TARGET="$HOME/Projects/NewProject"
test -f "$PSTACK_TEMPLATE/.codex/pstack/scripts/install-skills.py" &&
  test -d "$PSTACK_TARGET" && printf '範本安裝器與新專案目錄都存在\n'
```

看到「範本安裝器與新專案目錄都存在」後先預覽。

```bash
python3 "$PSTACK_TEMPLATE/.codex/pstack/scripts/install-skills.py" --project "$PSTACK_TARGET" --dry-run
```

預覽通過後再安裝。在同一個終端機執行第 4 節時，驗證會沿用此處的新專案路徑。最後在 Codex 開啟新專案。

```bash
python3 "$PSTACK_TEMPLATE/.codex/pstack/scripts/install-skills.py" --project "$PSTACK_TARGET"
```

如要檢查新專案的連結是否與自己的套件一致，可以使用它內附的安裝器執行預覽。預期顯示 `Would create 0 skill links`。

```bash
python3 "$PSTACK_TARGET/.codex/pstack/scripts/install-skills.py" --project "$PSTACK_TARGET" --dry-run
```

## 7. 團隊分享、版本更新與選用工具

- **隨 Git 專案分享**時，將 `.codex/pstack/` 與本次建立的 `.agents/skills/` 連結一起納入版本控制，並確認未被 `.gitignore` 排除。若要確認 Git 保留了連結型態，執行 `git -C "$PSTACK_TARGET" ls-files -s -- .agents/skills/poteto-mode`，已加入索引的連結應顯示模式 `120000`。同事 checkout 後可從第 4 節開始檢查。
- **更新或處理衝突**時，先比較來源與專案內的套件，確認要保留的專案修改。安裝器遇到不同的既有內容會停止。若途中發生寫入錯誤，先檢查留下的檔案與連結，再決定如何處理。
- **進階工具**依用途準備。PR watcher 需要 Bun、已準備的 watcher 相依套件，以及登入並具備目標 PR 權限的 GitHub CLI。Statechart 需要支援的 TypeScript runtime，執行 TLC 還需要 Java 與 `tla2tools.jar`。詳細命令見 [README 的進階工具](../README.md#進階工具)。

## 8. macOS 實測範圍

2026-11-24 在 macOS arm64、Python 3.9.6 與 Codex CLI 0.170.0 驗證。使用含空白及中文的暫存專案測試安裝，確認 58 個相對連結、重跑預覽為 0、從既有套件重用到新專案，以及 Git checkout 後保留連結。這些是暫存專案的結果，讀者可用第 4 節驗證自己的專案。

套件的 `scripts/check-discovery.py` 另行建立暫存 Git 專案做 CLI 探索，實測找到 58 個 skills、58 份介面資訊、0 個解析錯誤。它用於驗證套件能否被 Codex 探索。自己的專案仍應依第 5 節確認技能選單。進一步的驗證方式見 [套件驗證紀錄](verification.md)。

後續可補做 Linux 安裝與探索驗證、macOS 桌面 App 的手動選取驗證。

安裝完成後，可從 [pstack 使用指南](guide/README.md) 繼續了解各個工作流。
