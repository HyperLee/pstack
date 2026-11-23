# pstack for Codex

將「先理解、再分工、以證據驗收」帶進 Codex 的工程工作流套件。

本專案改寫自 [Lauren Tan（poteto）的 pstack](https://github.com/cursor/plugins/tree/main/pstack)，相關演講為 [All Code Is Slop (Except Mine) — Lauren Tan, SpaceXSI](https://www.youtube.com/watch?v=O_zcc6Xl12g)。來源快照的套件版本為 **0.15.43**；這個分支維護 Codex 原生版本，保留原作者與 MIT 授權。

截至 **2026-11-24**，已比對上游 **0.15.46**，並移植 `statechart` 的 TLC 換行解析與 Windows 程序控制修正。Codex 的模型選擇沿用現有的繼承與工具能力檢查。[上游更新比對紀錄](docs/codex-migration.md#上游更新比對紀錄)

原版的重點是讓每個代理都能理解問題、寫出較少而可靠的程式碼，再放心地平行處理獨立工作。這個版本保留 **58 個 skills、22 個 playbooks、24 個工程原則**，將執行工具、模型設定、安裝與協作方式改為適用於 Codex 桌面 App 與 CLI。

## 先理解它如何運作

`poteto-mode` 是主要入口。你提供目標、限制與完成條件；主代理選擇 playbook，必要時分派獨立工作，最後核對實際成果。

```mermaid
flowchart LR
    A[目標與完成條件] --> B[主代理選擇 playbook]
    B --> C[隔離的工作與驗證代理]
    C --> D[測試與實際產品證據]
    D --> E[主代理整合與交付]
```

平行處理適合互不相依的探索、測試與設計比較。多個代理同時修改同一份工作目錄，並不會因為有一份指示文件就變得安全；寫入工作會使用獨立 worktree 或輸出目錄。

## 安裝

基本安裝需要 **Python 3.9+**、Git 與支援 skills 的 Codex。套件安裝與工作流主要支援 macOS／Linux。`statechart` 的原生 Windows 指令見[進階工具](#進階工具)，原生 Windows 實機驗證仍待補充。

### 個人使用

在下載的本專案目錄執行：

```bash
python3 scripts/install-skills.py --user --dry-run
python3 scripts/install-skills.py --user
```

這會在 `~/.agents/skills/` 建立指向本 checkout 的連結。請保留來源目錄與位置；來源內容更新後，連結會讀到更新版本。安裝程式不會修改 Codex 的全域設定或其他 skills。

### 指定專案使用

第一次在 macOS 安裝，請參考 [macOS 版 Skills 專案安裝教學](docs/macOS版Skills_專案安裝教學.md)。

```bash
python3 scripts/install-skills.py --project "/path/to/your/repo" --dry-run
python3 scripts/install-skills.py --project "/path/to/your/repo"
```

專案安裝會將完整套件放入目標專案的 `.codex/pstack/`，並在 `.agents/skills/` 建立相對連結。團隊分享時將兩者一併納入版本控制；搬移 checkout 後仍能解析 skills、指南與參考文件。Benny 不會成為一般可探索的 skill。

相同安裝可重跑；同名路徑或套件內容與來源不同時，安裝程式會在寫入前停止。先檢視衝突再決定要保留或合併的內容，不會覆蓋既有修改。個人與專案層級若同時提供同名 skills，Codex 可能同時顯示兩份；請選定明確來源，不依賴同名自動合併。

安裝後在 Codex 選擇 skill。CLI 可使用 `/skills` 或輸入 `$` 選取，例如 `$poteto-mode`；桌面 App 使用其 skill 選擇介面。若未顯示，開啟新聊天或重新啟動 Codex，再檢查連結是否可讀。

## 第一次使用

不需要先設定模型，就可以開始：

```text
$poteto-mode 匯出功能在重試後會產生重複資料。先重現問題，再修復根因，提供修復前後的筆數與驗證結果。
```

需要調整成本與分工時使用：

```text
$setup-pstack 請以專案設定為主，保留目前模型，最多同時使用兩個 workers。
```

沒有設定檔時，預設繼承目前聊天的模型與推理設定，最多同時使用 3 個 workers，並受當前環境容量限制。多數 skills 保留原版的手動呼叫政策；單純安裝不會讓整套工作流套用到每一句聊天。

## 常用 skills

| 需求 | Skill |
| --- | --- |
| 一般嚴謹工程任務 | [`poteto-mode`](skills/poteto-mode/SKILL.md) |
| 解釋現有行為／歷史原因／教學 | [`how`](skills/how/SKILL.md)、[`why`](skills/why/SKILL.md)、[`teach`](skills/teach/SKILL.md) |
| 平行覆蓋不同範圍 | [`swarm`](skills/swarm/SKILL.md) |
| 比較獨立方案並整合 | [`arena`](skills/arena/SKILL.md) |
| 對變更提出可重現的反例 | [`interrogate`](skills/interrogate/SKILL.md) |
| 設計型別與模組邊界 | [`architect`](skills/architect/SKILL.md) |
| 測試先行與實際應用程式驗證 | [`tdd`](skills/tdd/SKILL.md)、[`create-verification-skill`](skills/create-verification-skill/SKILL.md) |
| 形式驗證與狀態圖 | [`statechart`](skills/statechart/SKILL.md) |
| 效能數據可信度 | [`benchmark-checklist`](skills/benchmark-checklist/SKILL.md) |
| 決策紀錄與進度說明 | [`show-me-your-work`](skills/show-me-your-work/SKILL.md)、[`ketchup`](skills/ketchup/SKILL.md) |
| 個人工作習慣與經驗回饋 | [`automate-me`](skills/automate-me/SKILL.md)、[`reflect`](skills/reflect/SKILL.md)、[`correct`](skills/correct/SKILL.md) |
| 不確定如何使用 | [`poteto-help`](skills/poteto-help/SKILL.md) |

完整操作請從 [繁體中文使用指南](docs/guide/README.md) 開始；工作流路由見 [poteto-mode](skills/poteto-mode/SKILL.md)。

## 多代理的三種用途

```text
$swarm 平行檢查三個互不相依的套件。每個 worker 記錄範圍、基準版本與檢查結果，最後交付一份整合報告。
```

```text
$arena 為這個資料模型提出兩個獨立方案，依可維護性與狀態一致性評分，再整合最有價值的部分。
```

```text
$interrogate 審查目前分支。只保留能用執行結果證明的錯誤，不修改產品程式碼。
```

`swarm` 重視覆蓋範圍；`arena` 比較同一題的不同解法；`interrogate` 尋找可證明的失敗。代理缺席、檢查失敗與無法驗證都會保留為缺口，不算通過。

## 模型、推理預算與設定檔

設定優先順序為專案 `.codex/pstack.json`、個人 `~/.codex/pstack.json`、套件預設。專案設定整份優先，未填欄位使用預設，不混入個人設定。這不是 Codex 自動載入的全域規則，由 pstack 開始工作時讀取。

```json
{
  "schema_version": 1,
  "budget": "inherit",
  "max_workers": 3,
  "roles": {}
}
```

`budget` 可選 `inherit`、`small`、`medium`、`large`。後三者分別建議 medium、high、xhigh 推理；實際仍以當前工具與模型支援為準。角色可另設 `model`、`reasoning_effort`，panel 角色使用清單。`auto` 與 `inherit-parent` 都代表繼承，不是模型代號。

只有確認可用的模型與欄位才會傳給工具；不可用時回報限制並繼承，不嘗試猜測另一個模型名稱。同模型的不同代理可以各自探索，但不會被描述為跨廠商評審。角色與格式詳見 [執行規約](skills/poteto-mode/references/codex-runtime.md)。

平行代理與獨立評審會增加 token 用量。降低 worker 數、縮小任務範圍、減少候選方案，比盲目增加代理更容易控制成本。

## 能力與限制

| 能力 | Codex 版本行為 |
| --- | --- |
| Skills、playbooks、工程原則 | 原生指示與本機參考文件 |
| 多代理 | 使用當前可呼叫工具；容量不足分批執行 |
| 沒有 subagent 工具 | 循序處理並標示失去獨立性；需要獨立驗證的交付不以自我檢查冒充 |
| 多模型／跨廠商 | 視實際環境而定，不保證可用 |
| 聊天紀錄 | 桌面聊天工具或指定匯出檔；CLI 不掃描猜測的私人紀錄路徑 |
| PR 監看 | 目前任務內的前景 watcher；進階工具需要 Bun、相依套件與已登入的 `gh` |
| statechart | 需要可執行 TypeScript 的 runtime、Java 與 TLC；圖形轉檔另需相應 renderer |
| Bugbot | 可讀取已存在的評論，不將它視為必要產品能力 |
| Benny／bot UI | 可攜工作流與整合範本；Slack、tracker、webhook 與事件來源需另行連接 |
| 長時間工作 | 依目前環境持續執行；不保證關機或休眠後繼續 |
| 清理目錄 | 唯讀盤點後交由使用者手動處理，不執行遞迴刪除 |

外部訊息、tracker 寫入、PR、merge 與部署遵循實際任務授權；安裝 skill 本身不授權這些動作。

## 進階工具

一般 skills 不需要 Java、TLC 或 Bun。需要 PR watcher 時，在可寫入的來源套件內先準備相依套件：

```bash
cd skills/poteto-mode/scripts
bun install --frozen-lockfile
bun watch-pr/watch-pr --help
```

執行 watcher 不會自動安裝套件或修改來源。若來源唯讀且尚未準備相依套件，先由擁有者準備，或使用目前可用的 `gh`／forge 工具監看。

在 macOS 或 Linux 使用 statechart 的 shell 啟動器。

```bash
sh skills/statechart/scripts/statechart /path/to/Spec.tla --out /path/to/new-output
```

在原生 Windows，使用 Node 22.18 至 22.x，或 Node 23.6 以上，並將 `--out` 指定為尚不存在的路徑。

```powershell
$env:TLA2TOOLS = 'C:\tools\tla2tools.jar'
$env:JAVA = 'C:\tools\jdk-25\bin\java.exe'
node --disable-warning=ExperimentalWarning ".\skills\statechart\scripts\statechart.ts" .\Spec.tla --out .\new-output
```

依實際安裝位置設定上述路徑。若 Windows 的 mise 只透過 `.cmd` shim 提供，請使用這種方式直接指定 Java 和 TLC。其他環境可用 mise 準備相依環境。執行器會保留暫存工作檔並回報位置。[statechart 技能](skills/statechart/SKILL.md)

## 驗證與開發

Python 檢查需要 [requirements-dev.txt](requirements-dev.txt) 的 PyYAML。先執行套件與行為測試，再依需要執行進階測試：

```bash
python3 scripts/validate.py
python3 -B -m unittest discover -s tests -v
```

PR watcher 在其 scripts 目錄執行 `bun test watch-pr` 與 `bun run typecheck`。statechart 在其 scripts 目錄執行 `node --test test/*.test.ts`；完整 TLC 測試需設定有效的 Java／TLC。詳細檢查方式與此次驗證範圍見 [移植說明](docs/codex-migration.md)。

測試與執行器不批次刪除目錄。請保留輸出中列出的暫存路徑，確認不再需要後自行手動清理。不要將證據已被刪除的測試當成完整驗證。

## 來源與授權

- [原始 Cursor pstack](https://github.com/cursor/plugins/tree/main/pstack)
- [原始演講](https://www.youtube.com/watch?v=O_zcc6Xl12g)
- [Codex skills 文件](https://learn.chatgpt.com/docs/build-skills)
- [Codex subagents 文件](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [MIT License](LICENSE)

這個版本是以原始專案為基礎的 Codex 移植，不代表原作者已驗證或維護本分支。
