# Windows 專用版本使用指南

本文件適用於 `codex/windows-support` 分支。這個版本供原生 Windows / PowerShell 使用，與 `main` 分開維護，不要求 WSL、Git Bash、開發人員模式或符號連結權限。實際驗證範圍見 [Windows 驗證紀錄](windows-verification.md)。

## 只在一個新專案使用

先準備 Python 3.9+、Git，以及支援 skills 的 Codex。在下載的 pstack 目錄執行：

```powershell
Set-Location "C:\GitHubFolder\pstack"
git branch --show-current
python -X utf8 scripts/install-skills.py --project "C:\GitHubFolder\MyNewProject" --mode copy --dry-run
python -X utf8 scripts/install-skills.py --project "C:\GitHubFolder\MyNewProject" --mode copy
```

安裝器會建立目錄，不必事先建立 `.agents/skills`。若電腦以 Python Launcher 管理 Python，可以用 `py -3 -X utf8` 取代 `python -X utf8`。

```text
MyNewProject/
├─ .agents/skills/
│  ├─ poteto-mode/
│  │  ├─ SKILL.md
│  │  ├─ .pstack-suite.json
│  │  └─ 其餘技能資源...
│  └─ 其他 57 個技能...
└─ .codex/pstack/
   ├─ README.md
   ├─ LICENSE
   ├─ skills/
   ├─ docs/
   └─ 其餘完整套件內容...
```

`.agents/skills` 中是實體檔案；`.pstack-suite.json` 以相對路徑定位完整套件。將 `.agents/skills` 與 `.codex/pstack` 一起納入版本控制，搬移或重新 checkout 後仍可讀取指南、角色與其他技能。安裝副本包含換行設定，避免 Git 的 Windows 換行轉換改變已安裝文字內容。

在 Codex 開啟 **MyNewProject**，使用技能選擇介面加入 `poteto-help` 或 `poteto-mode`；CLI 可輸入：

```text
$poteto-help 請說明如何在這個專案使用 pstack。
```

此操作不會建立全域技能安裝，也不會修改全域 Codex 設定。若選單尚未更新，開新聊天或重新啟動 Codex，並檢查 `SKILL.md`、定位檔及完整套件是否可讀。

## 複製、連結與更新

| 模式 | 行為 |
| --- | --- |
| `--mode copy` | Windows 預設。保存完整套件及技能副本；不依賴來源 checkout |
| `--mode symlink` | POSIX 預設。Windows 僅供已自行準備連結權限者選用；不屬於免權限驗收路徑 |
| `--dry-run` | 檢查衝突、列出預計建立項目，不寫入檔案 |

相同來源可重跑，既有檔案不會重寫。來源版本不同、套件內容被修改、技能副本被修改，或目的路徑已被占用時，安裝器停止並保留內容；這不是強制更新器。檢視差異後再人工決定遷移方式。中斷後的未完成安裝也會保留供檢查，不遞迴清理。

Windows 複製安裝不會自動跟隨來源更新。修改技能時，完整套件和已註冊副本須保持一致；不要只改其中一份。可以用以下工具確認定位：

```powershell
python .agents/skills/poteto-mode/scripts/locate-suite.py .agents/skills/poteto-help/SKILL.md
```

## 原生工具入口

以下相對路徑以完整套件根目錄為基準；專案安裝的根目錄是 `.codex/pstack`。

```powershell
# 設定檢查：接受 UTF-8 或 UTF-8 BOM JSON
python skills/setup-pstack/scripts/profile.py --project "C:\GitHubFolder\MyNewProject"

# 唯讀 worktree 盤點；不 fetch、不刪除
python skills/poteto-mode/scripts/worktree-audit.py --offline --base HEAD "C:\GitHubFolder\MyNewProject"

# 決策紀錄，UTF-8 TSV；保留換行／tab 清理與試算表公式防護
python skills/show-me-your-work/scripts/log.py decisions.tsv build "完成修正" "原因" "測試紀錄" "通過"
```

沒有 `du` 時，worktree 大小顯示 `unknown`；其他盤點繼續執行。Bash 入口保留供 POSIX 使用。

## PR watcher

另外安裝 Bun 與 GitHub CLI，並由使用者登入 GitHub CLI。先在可寫入的完整套件內準備相依套件：

```powershell
Push-Location skills/poteto-mode/scripts
bun install --frozen-lockfile
bun watch-pr/watch-pr --help
Pop-Location
```

watcher 不會自行安裝相依套件。實際監看仍需要有效的 GitHub 連線與存取權；單元測試通過不代表已驗收特定遠端 PR。

## Statechart / TLC

準備 Node 22.18–22.x / 23.6+，或 Bun 1.1.5+。Java 11+ 與 `tla2tools.jar` 需事先準備；此版以 TLC 1.7.4 驗證。Windows 不自動使用 mise 安裝 Java/TLC。

```powershell
$env:JAVA = "C:\Tools\Java\bin\java.exe"
$env:TLA2TOOLS = "C:\Tools\tla2tools.jar"
python skills/statechart/scripts/statechart.py "C:\MyProject\Spec.tla" --out "C:\MyProject\Spec-chart" --timeout-ms 60000
```

`JAVA` 是執行檔路徑，不要加入引號字元或命令參數。`--timeout-ms` 為選填，範圍 1–2147483647；省略則無內建期限。Node 可直接執行 `statechart.ts`；Python 入口會解析 Windows `node.cmd`，找出真實 Node 執行檔。

Job Object 以先暫停、加入 job、再啟動的方式管理 worker；其 Java 子程序繼承 job。取消、逾時、主 Node 程序結束或 supervisor 被終止時，所屬程序停止，未完成結果不發佈。使用 Ctrl+C 可取消；暫存檔保留供人工檢查。

退出碼 0 表示規則通過，1 表示找到違反規則的案例，2 表示工具錯誤或逾時；Ctrl+C 正常處理時為 130。0 和 1 才會發佈結果。輸出資料夾須符合工具的新建／空目錄要求，既有內容不得覆寫。

`PSTACK_PYTHON` 可指定 supervisor 的 Python `.exe`。Windows 透過 Python/JNI 載入 Java runtime 的 `jvm.dll`，以 UTF-16 傳遞來源、JAR 與設定路徑，避免繁中 Windows 的 Java launcher 改變字元。以 Temurin HotSpot 驗證；Java 路徑須對應包含 `jvm.dll` 的完整 Windows runtime。

`STATECHART_JAVA_ARGS` 可選擇傳入 JSON 字串陣列作為 JVM 前置參數，例如 `["-Xmx1g"]`；不是 Shell 命令。一般執行仍走 Unicode bridge。`STATECHART_JAVA_MODE=direct` 僅供回放或自訂工具 wrapper，明確繞過 bridge，需由 wrapper 自行處理 Unicode。

## 開發驗證

```powershell
python -m pip install -r requirements-dev.txt
Push-Location skills/poteto-mode/scripts
bun install --frozen-lockfile
Pop-Location
Push-Location skills/statechart/scripts
bun install --frozen-lockfile
Pop-Location

$env:JAVA = "C:\Tools\Java\bin\java.exe"
$env:TLA2TOOLS = "C:\Tools\tla2tools.jar"
python -X utf8 -B scripts/run-checks.py --full --discovery
```

完整開發測試需要 JDK（含 `jdk.compiler`），只有執行 statechart 才能使用 JRE。`--full` 要求 Bun、支援的 Node、JDK 與真實 TLC JAR；缺少必要工具視為失敗。未加 `--full` 時，缺少工具會明確顯示 `NOT RUN`。`--discovery` 使用 Codex app-server 驗證技能探索，不啟動模型工作。

測試入口會選擇 Windows CLI／程序測試，取代依賴 POSIX Shell、FIFO、signals 的 CLI 測試；其餘共用測試照常執行。渲染測試會在測試快取準備 npm 相依套件；若 Node 安裝未附 npm，可用 `PSTACK_NPM_CLI` 指定 `npm-cli.js`。可用 `PSTACK_BUN` 指定 Bun 執行檔，用 `PSTACK_TEST_ROOT` 指定證據與快取目錄。所有測試產物均保留，不批次刪除。
