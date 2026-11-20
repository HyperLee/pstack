# Windows 版 pstack：只在指定專案安裝 skills 的完整教學

本教學適用於 **`codex/windows-support` 分支**，以原生 Windows / PowerShell 示範如何將 pstack 安裝到一個新專案。使用實體複製模式，不需要 WSL、Git Bash、符號連結權限或系統管理員權限。

教學範例使用已實際安裝並檢查的 `SkillsTestProj`。下列正式安裝指令供操作參考；2026-11-20 的完整性檢查沒有重新安裝或修改該專案。

建議依目的選擇一條操作路徑，不必把重複的範例全部執行：

- **第一次安裝**：依序閱讀第 2～5 節，接著用第 7 節驗證，再依第 8 節在 Codex 使用。
- **檢查已安裝的 SkillsTestProj**：直接使用第 13 節 B，不必重新正式安裝。
- **只需要指令總表**：使用第 13 節 A，逐段確認後執行，再用 B 驗證。
- **需要額外檢查**：再參考第 14 節補充說明。

## 1. 先確認兩個不同的路徑

| 角色 | 本教學使用的路徑 | 用途 |
| --- | --- | --- |
| 安裝來源 | `C:\GitHubFolder\pstack` | Windows 分支的完整 pstack 原始套件與安裝器 |
| 目標專案 | `C:\GitHubFolder\SkillsTestProj` | 你正在開發、希望使用 skills 的專案 |

安裝器從來源讀取檔案，將副本放入目標專案。完成後，在 Codex 開啟的是 **`SkillsTestProj`**，才能使用這個專案的 skills。

這次使用的設定為：

- `--project`：安裝到指定專案。
- `--mode copy`：建立實體技能副本，不建立符號連結。
- 不使用 `--user`，因此這個操作不建立個人全域技能安裝。
- 不修改全域 Codex 設定。

專案安裝只決定這份 pstack 的放置範圍；Codex 本來就提供的系統技能或其他已安裝的個人技能仍可能出現在選單中。

## 2. 基本需求

準備以下工具：

| 工具 | 需求 |
| --- | --- |
| Python | 3.9 或以上，能從 PowerShell 呼叫 |
| Git | 能從 PowerShell 呼叫，用來確認來源分支與保存專案版本 |
| Codex | 使用支援專案 skills 的桌面 App 或 CLI |

一般 skills 的安裝與載入不要求先安裝 Bun、Java 或 TLC。這些是特定進階工具的相依項目，見第 11 節。

開啟一般 PowerShell 視窗，先執行：

```powershell
python --version
git --version
```

若 Python 是透過 Python Launcher 安裝，可以改為：

```powershell
py -3 --version
```

本教學主要步驟統一使用討論串中的 `python -X utf8`。若你使用 Python Launcher，請統一換成 `py -3 -X utf8`。`-X utf8` 啟用 UTF-8；其他選填參數與防呆檢查集中在第 14 節補充說明。

如果只有 Codex 桌面 App，沒有 CLI，不必為基本安裝特別準備 `codex` 終端機命令。

## 3. 設定來源與目標專案

在同一個 PowerShell 視窗設定變數，後面的步驟會沿用它們：

```powershell
$PstackSource = "C:\GitHubFolder\pstack"
$TargetProject = "C:\GitHubFolder\SkillsTestProj"

Set-Location "$PstackSource"
git branch --show-current
```

來源分支應顯示：

```text
codex/windows-support
```

確認顯示 `codex/windows-support` 後再往下操作。若日後顯示其他分支，先用 `git status --short` 檢查是否有未保存的修改，再決定是否切換；不要為了安裝而強制覆寫修改。

目標應選擇你要開啟的專案根目錄。本範例的 `SkillsTestProj.csproj` 就位於該目錄。不要把安裝目標設成 `bin`、`obj`、`Pages` 等子目錄。

**不用先建立 `.agents/skills` 或 `.codex/pstack`，安裝器會處理。**

## 4. 第一次先做安裝預覽

執行以下 PowerShell 指令。此階段只檢查內容與衝突，不寫入檔案：

```powershell
python -X utf8 "$PstackSource\scripts\install-skills.py" `
    --project "$TargetProject" `
    --mode copy `
    --dry-run
```

對尚未安裝的全新專案，預期會顯示：

```text
Would create 58 skill entries (copy)
```

而 `SkillsTestProj` 已經安裝完成，目前相同來源的預覽結果應是：

```text
Would create 0 skill entries (copy)
```

**0 表示沒有缺少或需要新增的技能項目，不是安裝失敗。** 安裝器會檢查完整套件與技能副本；內容相同時不重寫。

若出現 `Existing content differs; nothing changed`，表示同名路徑已被占用或內容不同。先檢視列出的路徑及差異，不要直接覆蓋。

## 5. 正式安裝

只有安裝預覽通過後才執行這一步。下面的命令會寫入目標專案：

```powershell
python -X utf8 "$PstackSource\scripts\install-skills.py" `
    --project "$TargetProject" `
    --mode copy
```

對全新專案，預期顯示：

```text
Created 58 skill entries (copy)
```

對已完成相同安裝的 `SkillsTestProj`，再次執行可能顯示：

```text
Created 0 skill entries (copy)
```

這也是正常結果，表示不必新增技能副本。

| 指令部分 | 用途 |
| --- | --- |
| `"$PstackSource\scripts\install-skills.py"` | 直接呼叫 Windows 分支提供的安裝器，不另設 `$Installer` 變數 |
| `--project "$TargetProject"` | 將套件安裝到指定專案 |
| `--mode copy` | 建立實體檔案，不依賴連結權限 |
| `--dry-run` | 僅預覽；正式安裝時移除此參數 |

PowerShell 中保留路徑兩側的引號，可以處理含空白或中文的路徑。反引號 `` ` `` 表示指令接續到下一行，必須是該行最後一個字元，後面不要再加空白或註解；複製時請一起複製整段。

## 6. 安裝後會有哪些檔案？

本範例的主要結構如下：

```text
C:\GitHubFolder\SkillsTestProj\
├─ .agents\
│  └─ skills\
│     ├─ poteto-mode\
│     │  ├─ SKILL.md
│     │  ├─ .pstack-suite.json
│     │  ├─ .gitattributes
│     │  ├─ references\
│     │  └─ 其他技能資源...
│     ├─ poteto-help\
│     ├─ setup-pstack\
│     └─ 其他技能...
│
├─ .codex\
│  └─ pstack\
│     ├─ README.md
│     ├─ LICENSE
│     ├─ .gitattributes
│     ├─ skills\
│     ├─ docs\
│     ├─ scripts\
│     └─ 其他完整套件內容...
│
├─ SkillsTestProj.csproj
├─ Program.cs
├─ Pages\
└─ 其他專案檔案...
```

兩個安裝目錄各有用途：

| 位置 | 用途 |
| --- | --- |
| `.agents/skills/` | 讓 Codex 探索及選取技能，內含 58 個 pstack 技能副本 |
| `.codex/pstack/` | 保存完整套件，包括指南、共用角色、腳本與其他資源 |
| 技能中的 `.pstack-suite.json` | 以相對路徑，從技能副本定位完整套件 |
| 安裝副本中的 `.gitattributes` | 固定文字換行規範，降低 Git checkout 造成內容差異的機會 |

因此，**不要只把來源的 `skills` 資料夾手動放進 `.agents/skills`**。那可能讓技能出現在選單中，卻缺少完整套件定位或指南等資源。也不要在 `.agents/skills` 下額外包一層 `skills`。

安裝後兩個目錄都應保留。這份副本不依賴來源 checkout 的原始位置；來源更新也不會自動同步過來。

## 7. 用 PowerShell 驗證安裝

以下指令只讀取安裝內容，不重新安裝。

### 7.1 檢查必要檔案

本節沿用第 3 節的 `$PstackSource` 與 `$TargetProject`，不重設目標路徑。若已關閉先前的 PowerShell，請先重新執行第 3 節，並填入你實際安裝的專案路徑；若要獨立檢查範例專案，可直接使用第 13 節 B。

```powershell
Test-Path -LiteralPath "$TargetProject\.agents\skills\poteto-mode\SKILL.md"
Test-Path -LiteralPath "$TargetProject\.agents\skills\poteto-help\.pstack-suite.json"
Test-Path -LiteralPath "$TargetProject\.codex\pstack\docs\guide\README.md"
```

三個結果都應為 `True`。

### 7.2 確認能找到專案內的完整套件

```powershell
python -X utf8 `
    "$TargetProject\.agents\skills\poteto-mode\scripts\locate-suite.py" `
    "$TargetProject\.agents\skills\poteto-help\SKILL.md"
```

預期輸出：

```text
C:\GitHubFolder\SkillsTestProj\.codex\pstack
```

### 7.3 用安裝預覽核對是否與來源一致

沿用第 3 節的來源與目標變數，執行：

```powershell
python -X utf8 "$PstackSource\scripts\install-skills.py" `
    --project "$TargetProject" `
    --mode copy `
    --dry-run
```

相同來源應顯示 `Would create 0 skill entries (copy)`，且沒有衝突錯誤。若日後來源分支已有新版本，出現差異不代表舊版一定損壞，而是需要先評估更新。

### 7.4 確認 Codex 實際能載入

前面幾項確認的是磁碟內容。最後應在 Codex 開啟目標專案，確認技能選單或實際探索結果。

若要請 Codex 協助再次檢查，可在目標專案聊天中貼上：

```text
請以唯讀方式檢查 C:\GitHubFolder\SkillsTestProj 的 pstack 安裝。
確認 58 個技能與定位檔是否完整、完整套件是否可讀，
以及 Codex 是否實際探索到該專案的技能。
不要重新安裝，不要修改專案，也不要啟動多代理實作任務。
```

套件的 `scripts/check-discovery.py` 是建立暫存專案再驗證的開發工具，並不是直接檢查目前 `SkillsTestProj` 安裝的命令；不要將暫存專案結果誤當成這個目標專案的驗收。

## 8. 在 Codex 開始使用

### 桌面 App

1. 在 Codex 開啟 `C:\GitHubFolder\SkillsTestProj`。
2. 在該專案建立新聊天。
3. 透過目前提供的技能選擇介面加入 `poteto-help` 或 `poteto-mode`。
4. 傳送工作目標與完成條件。

### CLI

若已安裝 Codex CLI，可在 PowerShell 切到目標專案後啟動：

```powershell
Set-Location "C:\GitHubFolder\SkillsTestProj"
codex
```

進入 Codex 後，可使用 `/skills` 或輸入 `$` 選取技能。

### 聊天提示範例

**以下內容貼在 Codex 聊天視窗，不是在 PowerShell 執行。**

先了解用法：

```text
$poteto-help 請介紹這個專案可用的 pstack skills，
以及我應該從哪個 skill 開始。
```

先唯讀了解測試專案：

```text
$poteto-mode 請先閱讀 SkillsTestProj，說明主要架構、
執行方式與現有測試。本次只分析，不修改程式碼。
```

需要調整分工預算時才使用專案設定：

```text
$setup-pstack 請使用此專案的設定，繼承目前聊天模型，
最多同時使用兩個 workers，並說明產生的設定。
```

`setup-pstack` 不是使用前的必要步驟。安裝完成也不代表每一句聊天都會自動啟動整套工作流；多數技能需要明確選取或呼叫。

## 9. SkillsTestProj 的實際檢查紀錄

檢查日期：**2026-11-20**。對象：`C:\GitHubFolder\SkillsTestProj`。

| 項目 | 實際結果 |
| --- | --- |
| pstack 技能副本 | 58 個 |
| `.pstack-suite.json` 定位檔 | 58 個 |
| 技能資料夾的連結 | 0 個，使用實體副本 |
| 全部技能的完整套件定位 | 均指向本專案 `.codex\pstack` |
| 相同來源的安裝預覽 | 0 個待建立項目，無衝突 |
| 完整套件靜態驗證 | 無錯誤 |
| Codex app-server 實際探索 | 58 skills、58 interfaces |
| 缺少技能或專案載入錯誤 | 0 個 |

這次 app-server 檢查直接指定 `SkillsTestProj`，沒有重新安裝，也沒有啟動模型工作。診斷產物保留在測試用暫存目錄，未寫入目標專案。

以上確認的是基本安裝與技能載入，不代表已在這個專案完成 PR watcher、Java/TLC 或所有技能工作流的實際驗收。當時 PATH 未找到 Bun、Java 與 GitHub CLI；這不影響已通過的基本安裝結果。

這是當日紀錄。日後新增、修改或搬移檔案後，請依第 7 節重新檢查。

## 10. 換另一個專案、團隊分享與更新

### 換另一個新專案

保留來源路徑，只將第 3 節的 `$TargetProject` 改成另一個實際專案的根目錄，再依序執行第 4 節預覽、第 5 節正式安裝與第 7 節驗證。第 7 節會沿用你設定的路徑，每個專案各有自己的副本。

若改用第 13 節指令總表，則修改 A、B 各自的 `$TargetProject`；總表的 B 是可獨立執行的範例，不會自動沿用 A 的其他專案路徑。補充說明中有自行設定路徑的範例，也應配合實際目標調整。

### 隨 Git 專案一起分享

若目標專案使用 Git，將 `.agents/skills/` 與 `.codex/pstack/` 一起納入版本控制，並確認未被專案的 `.gitignore` 排除。其他人 checkout 後才能取得完整技能與資源。

只分享其中一個目錄，可能造成技能無法探索或定位資源失敗。非 Git 專案搬移時也要一併保留這兩個目錄。

### 更新與修改

複製模式是專案自己的快照，不會自動跟隨來源更新。來源或已安裝內容不同時，安裝器會停止，不會自動合併或強制更新。

更新前先檢視版本與差異，再決定遷移方式。若要修改技能，完整套件和註冊副本須維持一致，不要只改其中一份。發現中斷安裝的產物時保留現場供檢查，不批次刪除資料夾。

## 11. 什麼時候需要額外工具？

| 用途 | 額外需求 |
| --- | --- |
| 安裝、讀取指南、選取一般 skills | 不需要先準備 Bun、Java 或 TLC |
| PR watcher | Bun、GitHub CLI、準備好的 watcher 相依套件，以及實際 GitHub 存取權 |
| Statechart / TLC | 支援的 Node 或 Bun、Java runtime 與 `tla2tools.jar` |
| 完整套件開發測試 | Python 開發相依套件、Bun、支援的 Node、JDK 與 TLC |

進階工具的版本需求、PowerShell 指令與驗證範圍，請參考 [Windows 使用指南](docs/windows.md) 及 [Windows 版本驗證紀錄](docs/windows-verification.md)。不用為了第一次安裝，一次安裝所有進階工具。

## 12. 常見問題

| 現象 | 檢查與處理方式 |
| --- | --- |
| 找不到 `python` | 試用 `py -3 --version`，後續指令統一改用 Python Launcher |
| `python3` 開啟 Microsoft Store | 使用已驗證可執行的 `python` 或 `py -3`，不要只憑別名判定 Python 已安裝 |
| 安裝預覽顯示 0 | 若無衝突，表示相同套件已完整存在，屬於正常結果 |
| 出現 `Existing content differs` | 檢查列出的同名路徑、修改或版本差異；不要強制覆寫 |
| 詢問符號連結權限 | 確認使用 Windows 分支與 `--mode copy`，不是連結模式 |
| Codex 看不到技能 | 確認開啟目標專案、安裝層級正確；開新聊天或重新啟動後再檢查選單 |
| 有技能但找不到指南 | 檢查 `.codex/pstack` 與定位檔是否一起保留，不要只複製 `skills` |
| 來源更新但目標沒變 | 複製模式不自動同步；先比較差異，再規劃更新 |
| 想移除舊版或清理目錄 | 先辨識具體安裝路徑與需保留的修改，再由使用者人工處理，不使用遞迴或批次刪除命令 |

## 13. 指令總表

下面分成兩段。第一段會安裝；第二段只驗證。若只想檢查已安裝的 `SkillsTestProj`，使用第二段即可。

### A. 新專案安裝：先預覽，再正式寫入

在同一個 PowerShell 視窗依序操作。先執行這一段，設定路徑並確認來源分支：

```powershell
# 換其他專案時，主要修改這個目標路徑。
$PstackSource = "C:\GitHubFolder\pstack"
$TargetProject = "C:\GitHubFolder\SkillsTestProj"

Set-Location "$PstackSource"
git branch --show-current
```

分支應為 `codex/windows-support`；若不是，先停在這一步處理來源分支。確認後執行預覽：

```powershell
python -X utf8 "$PstackSource\scripts\install-skills.py" `
    --project "$TargetProject" `
    --mode copy `
    --dry-run
```

預覽沒有錯誤後，才複製執行正式安裝這一段：

```powershell
python -X utf8 "$PstackSource\scripts\install-skills.py" `
    --project "$TargetProject" `
    --mode copy
```

### B. 已安裝專案驗證：不重新安裝

```powershell
$PstackSource = "C:\GitHubFolder\pstack"
$TargetProject = "C:\GitHubFolder\SkillsTestProj"

Test-Path -LiteralPath "$TargetProject\.agents\skills\poteto-mode\SKILL.md"
Test-Path -LiteralPath "$TargetProject\.agents\skills\poteto-help\.pstack-suite.json"
Test-Path -LiteralPath "$TargetProject\.codex\pstack\docs\guide\README.md"

python -X utf8 `
    "$TargetProject\.agents\skills\poteto-mode\scripts\locate-suite.py" `
    "$TargetProject\.agents\skills\poteto-help\SKILL.md"

python -X utf8 "$PstackSource\scripts\install-skills.py" `
    --project "$TargetProject" `
    --mode copy `
    --dry-run
```

預期看到三個 `True`、專案內的完整套件路徑，以及 `Would create 0 skill entries (copy)`，且沒有錯誤。再在 Codex 開啟目標專案並選取技能，就能開始使用。若要另外計算技能數量，可使用第 14 節的補充檢查。

## 14. 補充說明：選用參數與額外檢查

以下內容供需要額外確認時使用，不是另一套安裝流程。主要步驟與第 13 節總表均沿用討論串的寫法。

### 14.1 選用的 `-B` 參數

先前文件曾使用 `python -X utf8 -B`，其中 `-B` 只是避免 Python 產生 bytecode 快取，不會改變 `--project` 的安裝範圍或 `--mode copy` 的複製方式。

為了讓主要指令與討論串一致，本文統一使用 `python -X utf8`。一般操作不必額外加上 `-B`。

### 14.2 確認來源與目標路徑存在

需要額外確認時，先設定變數，再執行以下唯讀檢查：

```powershell
$PstackSource = "C:\GitHubFolder\pstack"
$TargetProject = "C:\GitHubFolder\SkillsTestProj"

Test-Path -LiteralPath $PstackSource -PathType Container
Test-Path -LiteralPath $TargetProject -PathType Container
```

兩個結果都應為 `True`。安裝器本身可以建立不存在的目錄；先確認目標專案存在，是為了避免把輸入錯誤的路徑當成新目錄建立，不是安裝器的額外限制。

### 14.3 額外計算 pstack 技能副本數量

只計算同時具有 `SKILL.md` 與 pstack 定位檔的資料夾，避免將其他套件的技能算進來：

```powershell
$TargetProject = "C:\GitHubFolder\SkillsTestProj"
$SkillRoot = Join-Path $TargetProject ".agents\skills"

$PstackSkills = @(
    Get-ChildItem -LiteralPath $SkillRoot -Directory | Where-Object {
        (Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")) -and
        (Test-Path -LiteralPath (Join-Path $_.FullName ".pstack-suite.json"))
    }
)

$PstackSkills.Count
```

此版本預期為 **58**。數量符合只是基本檢查，仍須確認第 7 節的定位與 Codex 載入結果。

### 14.4 額外檢查命令退出碼

執行 `python` 或 `git` 命令後，可以立刻查看：

```powershell
$LASTEXITCODE
```

一般成功時為 `0`，失敗時為非 `0`。它代表最近一個外部程式的退出碼，所以應緊接在要檢查的命令後使用，不要先執行另一個外部程式。

如果你是在編寫自動化腳本，也可以在每一個要檢查的命令後加上以下防呆邏輯：

```powershell
if ($LASTEXITCODE -ne 0) {
    throw "上一個命令未成功，停止後續操作，請檢查錯誤。"
}
```

這是選用的自動停止方式。主要教學採逐段操作、查看預期輸出；若有錯誤，先停止，不要繼續正式安裝。

延伸閱讀：[Windows 使用指南](docs/windows.md)、[完整操作指南](docs/guide/README.md)、[套件 README](README.md)。

## 15. 補充：直接複製的懶人方法

如果你已經有一份安裝完整、可正常載入的 Windows 版 pstack，例如本教學的 `SkillsTestProj`，下次可以直接把它的 **`.agents` 與 `.codex` 兩個資料夾一起複製到新專案根目錄**，不必再次執行正式安裝。

這是另一種取得現有套件副本的方法，前面原有的安裝流程仍可照常使用。此方法適用於本教學的 Windows **實體複製模式**；若來源採用符號連結，不要直接套用這個流程。

### 15.1 操作前先確認範本與新專案

| 角色 | 本節使用的路徑 |
| --- | --- |
| 已安裝好的範本專案 | `C:\GitHubFolder\SkillsTestProj` |
| 新專案根目錄 | `C:\GitHubFolder\NewProject` |

`NewProject` 是示範名稱，請先建立你真正要開發的專案，再換成它的實際根目錄。本節不會替你建立應用程式專案。

目前已確認 `SkillsTestProj` 的 `.agents` 內只有 `skills`，`.codex` 內只有 `pstack`，可以整組作為這次的複製範本。技能定位檔使用相對路徑，沒有綁定 `SkillsTestProj` 這個專案名稱。

日後若範本的這兩個目錄加入了其他技能、專案設定或紀錄，複製前應重新檢視內容，不要把只適用於舊專案的內容一起帶入。

### 15.2 方法一：使用檔案總管複製

1. 開啟 `C:\GitHubFolder\SkillsTestProj`。
2. 同時選取 `.agents` 與 `.codex`，使用「複製」。
3. 開啟新專案根目錄，例如 `C:\GitHubFolder\NewProject`。
4. 確認新專案尚未有 `.agents` 或 `.codex`。若已存在其中任何一個，先停止、比對內容，不要選擇合併或取代。
5. 使用「貼上」，等待兩個資料夾都複製完成。若看不到這些目錄，可開啟檔案總管顯示隱藏項目的選項。
6. 保留所有內部檔案，包括 `.pstack-suite.json` 與 `.gitattributes`，不要只挑選 `SKILL.md`。

完成後應是：

```text
C:\GitHubFolder\NewProject\
├─ .agents\
│  └─ skills\
│     ├─ poteto-mode\
│     ├─ poteto-help\
│     └─ 其他技能...
├─ .codex\
│  └─ pstack\
│     ├─ skills\
│     ├─ docs\
│     └─ 其他完整套件內容...
└─ 新專案自己的程式碼...
```

不要多包一層 `SkillsTestProj`，也不要把兩個目錄放進新專案的 `bin`、`obj` 或其他子目錄。只需要複製這兩個目錄，不必複製範本專案的 `Program.cs`、`.csproj`、`bin` 或 `obj`。

### 15.3 方法二：使用 PowerShell 複製

這與檔案總管方法擇一即可。**若已完成方法一，直接前往第 15.4 節，不要再次執行複製指令。**

先修改 `$NewProject` 為新專案的實際根目錄，再複製執行以下整段。這段會寫入新專案；路徑或目的目錄檢查未通過時會停止。

```powershell
$TemplateProject = "C:\GitHubFolder\SkillsTestProj"
$NewProject = "C:\GitHubFolder\NewProject"

& {
    if (-not (Test-Path -LiteralPath "$TemplateProject\.agents\skills" -PathType Container)) {
        throw "範本缺少 .agents\skills，停止複製。"
    }
    if (-not (Test-Path -LiteralPath "$TemplateProject\.codex\pstack" -PathType Container)) {
        throw "範本缺少 .codex\pstack，停止複製。"
    }
    if (-not (Test-Path -LiteralPath $NewProject -PathType Container)) {
        throw "新專案目錄不存在，請先確認實際專案路徑。"
    }
    if ((Test-Path -LiteralPath "$NewProject\.agents") -or
        (Test-Path -LiteralPath "$NewProject\.codex")) {
        throw "新專案已有 .agents 或 .codex，停止複製，請先比對內容。"
    }

    Copy-Item -LiteralPath "$TemplateProject\.agents" `
        -Destination "$NewProject\.agents" `
        -Recurse -Force -ErrorAction Stop

    Copy-Item -LiteralPath "$TemplateProject\.codex" `
        -Destination "$NewProject\.codex" `
        -Recurse -Force -ErrorAction Stop
}
```

這裡的 `& { ... }` 將檢查與兩次複製放在同一個執行區塊；遇到檢查失敗或複製錯誤時停止後續動作。`-Recurse` 複製子目錄，`-Force` 用於一併處理隱藏項目；它搭配前面的「目的目錄不存在」檢查使用，不是用來覆蓋既有安裝。

這不是交易式安裝：若第二個資料夾複製失敗，第一個可能已經存在。請保留現場、確認錯誤與缺少內容，不要移除檢查後強制重跑，也不要批次刪除目錄。

### 15.4 複製後的唯讀驗證

不論採用方法一或方法二，都應執行本節。這些指令只讀取與預覽，不會再次正式安裝。

**驗證段的 `$NewProject` 必須與剛才實際貼上或複製的目標一致。**

#### A. 確認必要檔案存在

```powershell
$NewProject = "C:\GitHubFolder\NewProject"

Test-Path -LiteralPath "$NewProject\.agents\skills\poteto-mode\SKILL.md"
Test-Path -LiteralPath "$NewProject\.agents\skills\poteto-help\.pstack-suite.json"
Test-Path -LiteralPath "$NewProject\.codex\pstack\docs\guide\README.md"
```

三個結果都應為 `True`。若不是，先檢查複製是否完成及目錄層級是否正確。

#### B. 確認技能能定位新專案自己的套件

沿用上面的 `$NewProject`：

```powershell
python -X utf8 `
    "$NewProject\.agents\skills\poteto-mode\scripts\locate-suite.py" `
    "$NewProject\.agents\skills\poteto-help\SKILL.md"
```

本節範例預期輸出：

```text
C:\GitHubFolder\NewProject\.codex\pstack
```

重點是輸出必須指向**新專案內部**，不是 `SkillsTestProj` 或原始 `pstack` 來源。若你使用其他專案名稱，輸出路徑也應對應改變。

#### C. 確認技能副本數量

```powershell
$SkillRoot = Join-Path $NewProject ".agents\skills"

$CopiedSkills = @(
    Get-ChildItem -LiteralPath $SkillRoot -Directory | Where-Object {
        (Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")) -and
        (Test-Path -LiteralPath (Join-Path $_.FullName ".pstack-suite.json"))
    }
)

$CopiedSkills.Count
```

依本教學目前的範本版本，預期為 **58**。數量正確仍需搭配必要檔案與定位檢查。

#### D. 選用：預覽套件與技能副本的一致性

可以使用**新專案內附的安裝器**做預覽，不必回到原始來源目錄：

```powershell
python -X utf8 "$NewProject\.codex\pstack\scripts\install-skills.py" `
    --project "$NewProject" `
    --mode copy `
    --dry-run
```

預期為 `Would create 0 skill entries (copy)`，且沒有衝突錯誤。這是檢查新專案內套件與技能副本是否一致，不是與網路或原始來源比較最新版；請保留 `--dry-run`，不必再次正式安裝。

### 15.5 在 Codex 開啟新專案

驗證通過後，在 Codex 開啟 `C:\GitHubFolder\NewProject`，建立該專案的新聊天，再選取 `poteto-help` 或 `poteto-mode`。若技能尚未顯示，先開新聊天或重新啟動 Codex，再檢查目錄與定位檔。

以下提示貼在 **Codex 聊天視窗**，不是 PowerShell：

```text
$poteto-help 請介紹這個新專案可以使用的 pstack skills，
並說明適合從哪個工作流開始。
```

這種方式仍然只是專案層級的技能副本，不會建立全域安裝。它保留範本當下的版本，不會自動更新；Bun、GitHub CLI、Java / TLC 等進階工具仍須另外準備。若日後要分享新專案，請一併保留 `.agents/skills` 與 `.codex/pstack`。
